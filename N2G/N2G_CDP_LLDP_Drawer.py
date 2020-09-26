import logging
from ttp import ttp
import pprint
import os

# initiate logging
log = logging.getLogger(__name__)
LOG_LEVEL = "ERROR"

def logging_config(LOG_LEVEL):
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL.upper() in valid_log_levels:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [N2G_CDP_Drawer %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=LOG_LEVEL.upper()
        )

logging_config(LOG_LEVEL)


#=============================================================================
# TTP PARSER TEMPLATES:                                           
#=============================================================================

Cisco_IOS = """
<template name="Cisco_IOS" results="per_template">
<vars>local_hostname="gethostname"</vars>

<input>url = "./Cisco_IOS/"</input>

<group name="interfaces**.{{ local_hostname }}{{ interface }}">
interface {{ interface }}
</group>

<group name="cdp_peers*" expand="">
Device ID: {{ target.id }}
  IP address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }},  Capabilities: {{ ignore(ORPHRASE) }}
Interface: {{ src_label | resuball(IfsNormalize) }},  Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
{{ source | set("local_hostname") }}
</group>
</template>
"""

Cisco_NXOS = """
<template name="Cisco_NXOS" results="per_template">

<vars name="vars">
local_hostname="gethostname"
</vars>

<input name="Cisco_NX-OS" load="yaml">
url: "./Cisco NXOS/"
</input>

<g name="interfaces**.{{ Interface }}.cdp" input="Cisco_NX-OS">
##===================-CDP-===================

## Cisco new NX-OS:
Device ID: {{ peer_hostname | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}
Device ID:{{ peer_hostname | _start_ | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}
  IP address: {{ peer_ip | default }}
##with space at the end:
  IP address: {{ peer_ip | default }}    
Platform: {{ peer_platform | ORPHRASE | exclude("-VM-") }},  Capabilities: {{ peer_capabilities | ORPHRASE | truncate(2) }}
##with space at the end:
Platform: {{ peer_platform | ORPHRASE | exclude("-VM-") }},  Capabilities: {{ peer_capabilities | ORPHRASE | truncate(2) }} 
Interface: {{ Interface | resuball(IfsNormalize) }},  Port ID (outgoing port): {{ peer_interface | ORPHRASE | resuball(IfsNormalize) }}

##old Cisco N7K:
    IPv4 Address: {{ peer_ip | default }}
{{ peer_platform | ORPHRASE | exclude("-VM-") }}, Capabilities: {{ peer_capabilities | ORPHRASE | truncate(2) }}
{{ Interface | resuball(IfsNormalize) }}, Port ID (outgoing port): {{ peer_interface | resuball(IfsNormalize) | ORPHRASE }}
</g >

<g name="interfaces**.{{ Interface }}.lldp" input="Cisco_NX-OS">
##===================-LLDP-===================
Chassis id: {{ ignore }}
Port id: {{ peer_interface | ORPHRASE | resuball(IfsNormalize) | exclude(vmnic) | default }}
Local Port id: {{ Interface | resuball(IfsNormalize) }}
System Name: {{ peer_hostname | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}
System Description: {{ peer_platform | ORPHRASE | exclude("-VM-") | truncate(2) }}
Management Address: {{ peer_ip | default }}
</g>

<g name="interfaces**.{{ Interface }}.cfg" input="Cisco_NX-OS">
##===================-CFG-===================
interface {{ Interface | resuball(IfsNormalize) }}
  description {{ description | ORPHRASE }}
  switchport mode trunk {{ mode | set(trunk) }}
  switchport trunk native vlan {{ accessVlan }}
  switchport access vlan {{ accessVlan }}
  switchport trunk allowed vlan {{ trunkVlans | joinmatches() | unrange('-',',') }}
  switchport trunk allowed vlan add {{ trunkVlans | joinmatches() | unrange('-',',') }}
  channel-group {{ lag }} mode {{ lag_mode }}
  vpc {{ vPC_ID }}
  mpls ip {{ mpls | set(Enabled) }}
  mtu {{ mtu }}
  ip address {{ ipv4 }}/{{ maskv4 }}
  ipv6 address {{ ipv6 }}/{{ maskv6 }}
  ip ospf cost {{ ospf_cost}}
  ip ospf network point-to-point {{ ospf_link_type | set(ptp) }}
  ip router ospf {{ ospf_pid }} area {{ ospf_area }}
  vrf member {{ vrf }}
!{{ _end_ }}
</g>
</template>
"""

Cisco_IOSXR = """
<vars name="vars">
local_hostname="gethostname"
</vars>

<input name="Cisco_IOS-XR" load="yaml">
url: "./Cisco/IOS-XR/"
</input>

<g name="interfaces**.{{ Interface }}.cdp" input="Cisco_IOS-XR">
##===================-CDP-===================
-------------------------{{ _start_ }}
Device ID: {{ peer_hostname | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}
  IPv4 address: {{ peer_ip | default }}
Platform: {{ peer_platform | ORPHRASE | exclude("-VM-") }},  Capabilities: {{ peer_capabilities | ORPHRASE | truncate(2) }}
##with space at the end:
Platform: {{ peer_platform | ORPHRASE | exclude("-VM-") }},  Capabilities: {{ peer_capabilities | ORPHRASE | truncate(2) }}  
Interface: {{ Interface | resuball(IfsNormalize) }}
Port ID (outgoing port): {{ peer_interface | resuball(IfsNormalize) | ORPHRASE }}
</g>

<g name="interfaces**.{{ Interface }}.cfg" input="Cisco_IOS-XR">
##===================-CFG-===================
interface {{ Interface | resuball(IfsNormalize) }}
 description {{ description | ORPHRASE }}
 mtu {{ mtu }}
 ipv4 address {{ ipv4 | exclude(":") }} {{ maskv4 }}
 ipv6 address {{ ipv6 | contains(":") }}/{{ maskv6 }}
## to match " ipv6 address bla/64 eui-64" v6 ips:
 ipv6 address {{ ipv6 | contains(":") }} {{ maskv6 | contains(eui) }}
 vrf {{ vrf }}
 bundle id {{ lag }} mode {{ lag_mode }}
!{{ _end_ }}
</g>
"""

Huawei = """
<vars name="vars">
local_hostname="gethostname"
</vars>

<input name="Huawei" load="yaml">
url: "./Huawei/"
</input>

<g name="interfaces**.{{ Interface }}.lldp" input="Huawei">
##===================-LLDP-===================
{{ Interface | resuball(IfsNormalize) }}  has 1 neighbor(s):
Port ID                            :{{ peer_interface | ORPHRASE | resuball(IfsNormalize) | exclude(vmnic)}}
System name                        :{{ peer_hostname | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}    
##no spaces at the end:  
System name                        :{{ peer_hostname | replaceall(domainsToStrip) | resub(r"\\(\\S+\\)", "") }}
System description                 :{{ peer_platform | ORPHRASE | exclude("-VM-") | truncate(2) }}
Management address                 :{{ peer_ip | default }}
</g>

<g name="interfaces**.{{ Interface }}.cfg" input="Huawei">
##===================-CFG-===================
interface {{ Interface | resuball(IfsNormalize) }}
 description {{ description | ORPHRASE }}
 port link-type trunk {{ mode | set(trunk) }}
 port trunk pvid vlan {{ accessVlan }}
 port trunk allow-pass vlan {{ trunkVlans | ORPHRASE | unrange('to',' ') | replace(' ', ',') | joinmatches() }}
 port trunk allow-pass vlan all {{ trunkVlans | set(ALL) }}
 dfs-group 1 m-lag {{ mLAG_ID }}
 eth-trunk {{ lag }}
 peer-link 1 {{ peer_link | set(True) }}
 ip address {{ ipv4 }} {{ maskv4 }}
 ospf cost {{ ospf_cost}}
 ospf network-type p2p {{ ospf_link_type | set(ptp) }}
 ospf enable {{ ospf_pid }} area {{ ospf_area }}
 mpls {{ mpls | set(Enabled) }}
 ip binding vpn-instance {{ vrf }}
##with spaces at the end:
 eth-trunk {{ lag }}   
#{{ _end_ }}
</g>
"""


#=============================================================================
# COMMON TTP PARSER Variables:                                           
#=============================================================================

ttp_vars = {
    "IfsNormalize": {
        'Lo': ['^Loopback'], 
        'Ge':['^GigabitEthernet'], 
        'Po': ['^Eth-Trunk', '^port-channel', '^Port-channel', '^Bundle-Ether'], 
        'Te':['^TenGigabitEthernet', '^TenGe', '^10GE', '^TenGigE', '^XGigabitEthernet'], 
        'Fe':['^FastEthernet'], 
        'Eth':['^Ethernet'], 
        'Pt':['^Port[^-]'], 
        '100G':['^HundredGigE']
    }
}    



#=============================================================================
# Main class:                                           
#=============================================================================

class cdp_lldp_drawer():
    """
    Class to process CDP and LLDP neighbors together with
    running configuration and state to produce diagram out of it.
    
    **Supported platforms**

    +---------------+------------+-----------+-----------+-----------+
    | Platform      |    CDP     |   LLDP    |   config  |   state   |
    +===============+============+===========+===========+===========+
    | Cisco_IOS     |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+
    | Cisco_IOSXR   |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+
    | Cisco_NXOS    |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+
    | Cisco_ASA     |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+
    | Huawei        |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+  
    | Juniper       |    ---     |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+ 
    
    **Cisco Commands**
    
    * CDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show cdp neighbor details``
    * LLDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show lldp neighbor details``
    * config for Cisco IOS, IOS-XR, NXOS, ASA - ``show running-configuration``
    * state for Cisco IOS, IOS-XR, NXOS - ``show interface``
    
    ** Huawei Commands**
    
    * LLDP - ``display lldp neighbor details``
    * config - ``display current-configuration``
    * state - ``display interface``
                       
    **cdp_lldp_drawer attributes**    
    
    * ``data`` dictionary or OS path string to directory with text files
    * ``drawing`` N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    * ``config`` dictionary of configuration options to define processing behavior 
    
    If data is dictionary, keys must correspond to "Platform" column in 
    *Supported platforms* table, values are lists of text items to
    process.
    
    Data dictionary sample::
    
        data = {
            "Cisco_IOS" : ["h1", "h2"],
            "Cisco_IOS-XR": ["h3", "h4"],
            "Cisco_NXOS": ["h5", "h6"],
            ...etc...
        }
        
    Where ``hX`` devices show commands output.   
    
    If data is a string with OS path to directory, child directories names 
    must correspond to "Platform" column in *Supported platforms* table.
    Each child directory should contain text files with show commands output
    for each device.
    
    Directories structure sample::
    
        /data/
             |_/Cisco_IOS/<text files>
             |_/Cisco_IOS-XR/<text files>
             |_/Huawei/<text files>
             |_/...etc...
    """
    def __init__(self, drawing, data, config={}):
        # init attributes
        self.config = config
        self.drawing = drawing
        self.drawing.node_duplicates="update"
        self.parsed_data = []
        
        # work:
        self._parse(data)
        self._populate_drawing()


    def _parse(self, data):
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=ttp_vars)
            for platform_name, text_list in data.items():
                try:
                    ttp_template = globals()[platform_name]
                except KeyError:
                    log.error("Cannot find template for '{}' platform".format(
                            platform_name
                        )
                    )
                    continue
                parser.add_template(template=ttp_template, template_name=platform_name)
                for item in text_list:
                    parser.add_input(item, template_name=platform_name)
        # process directories at OS path 
        elif isinstance(data, str):
            parser = ttp(vars=ttp_vars, base_path=data)
            # get all sub-folders and load respective templates
            with os.scandir(data) as it:
                for entry in it:
                    if entry.is_dir():
                        try:
                            ttp_template = globals()[entry.name]
                        except KeyError:
                            log.error("Cannot find template for '{}' platform".format(
                                    entry.name
                                )
                            )
                            continue
                        parser.add_template(template=ttp_template, template_name=entry.name)
        else:
            log.error("Expecting dictionary or string, but '{}' given".format(
                    type(data)
                )
            )
            return
        parser.parse(one=True)
        self.parsed_data = parser.result(structure="flat_list")


    def _populate_drawing(self):
        for item in self.parsed_data:
            self.drawing.from_list(item.get("cdp_peers", [{}]))
            self.drawing.from_list(item.get("lldp_peers", [{}]))