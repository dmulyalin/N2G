import logging
from ttp import ttp
import pprint
import os
import json

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

<group name="{{ local_hostname }}.interfaces**.{{ interface }}">
interface {{ interface | resuball(IfsNormalize) }}
 description {{ description | re(".+") }}
 switchport {{ is_l2 | set(True) }}
 switchport access vlan {{ access_vlan }}
 switchport mode {{ l2_mode }}
 vrf forwarding {{ vrf }}
 ip address {{ ip | PHRASE | joinmatches(",") }}
 ip address {{ ip | PHRASE | joinmatches(",") }} secondary
 switchport trunk allowed vlan {{ trunk_vlans | unrange("-", ",") | joinmatches(",") }}
 mtu {{ mtu }}
</group>

<group name="{{ local_hostname }}.cdp_peers*" expand="">
Device ID: {{ target.id }}
  IP address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }},  Capabilities: {{ ignore(ORPHRASE) }}
Interface: {{ src_label | resuball(IfsNormalize) }},  Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
{{ source | set("local_hostname") }}
</group>
</template>
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
    def __init__(self, drawing, config={}):
        # init attributes
        self.config = {
            "add_interfaces_data": True
        }
        self.config.update(config)
        self.drawing = drawing
        self.drawing.node_duplicates="update"
        self.parsed_data = {}
        self.graph_dict = {}

    def work(self, data):
        self._parse(data)
        pprint.pprint(self.parsed_data, width=150)
        self._form_base_graph_dict()
        if self.config.get("add_interfaces_data"):
            self._add_interfaces_data()
        if self.config.get("group_links"):
            self._group_links()

        self._update_drawing()
        

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
        self.parsed_data = parser.result(structure="dictionary")

    def _make_hash_tuple(self, item):
        return tuple(sorted([
                        item["source"],
                        item["target"]["id"],
                        item["src_label"],
                        item["trgt_label"]
                    ]))
                    
    def _form_base_graph_dict(self):
        for platform, hosts in self.parsed_data.items():
            for hostname, host_data in hosts.items():
                for item in host_data.get("cdp_peers", []):
                    self.graph_dict[self._make_hash_tuple(item)] = item.copy()
                for item in host_data.get("lldp_peers", []):
                    self.graph_dict[self._make_hash_tuple(item)] = item.copy()


    def _add_interfaces_data(self):
        """
        Method to add description metadata to links containing information about
        interface configuration and state.
        """
        for platform, hosts in self.parsed_data.items():
            for hostname, host_data in hosts.items():
                for item in host_data.get("cdp_peers", []):                
                    src = item["source"]
                    tgt = item["target"]["id"]
                    src_if = "{}:{}".format(src, item["src_label"])
                    tgt_if = "{}:{}".format(tgt, item["trgt_label"])
                    # form description data for link
                    description = {
                        src_if: host_data.get("interfaces", {}).get(item["src_label"], {}),
                        tgt_if: host_data.get("interfaces", {}).get(item["trgt_label"], {})
                    }
                    # update item in graph data 
                    hash = self._make_hash_tuple(item)
                    self.graph_dict[hash]["description"] = json.dumps(description, sort_keys=True, indent=4, separators=(',', ': ')) 
                    
    def _group_links(self):
        pass
        
    def _update_drawing(self):
        self.drawing.from_list(list(self.graph_dict.values()))