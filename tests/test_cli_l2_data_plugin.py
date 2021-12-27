import sys
import pprint

sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cli_l2_data

def test_cdp_drawing_yed_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface GigabitEthernet4/6
 description switch-2: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 1771,1887
 switchport mode trunk
 mtu 9216
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

switch-2#show run
interface GigabitEthernet1/5
 description switch-1: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    # pprint.pprint(drawer.parsed_data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                                                            'src_label': 'GE4/6',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                                                            'trgt_label': 'GE1/5'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'GE1/1',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                                                            'trgt_label': 'GE0/1'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'GE1/2',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                                                            'trgt_label': 'GE0/10'}],
                                                             'interfaces': {'GE1/1': {'description': 'switch-3:Gi0/1',
                                                                                      'is_l2': True,
                                                                                      'l2_mode': 'trunk',
                                                                                      'mtu': '9216',
                                                                                      'trunk_vlans': '1771,1887'},
                                                                                'GE1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                                                                'GE4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
                                                'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                                                            'src_label': 'GE1/5',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                                                            'trgt_label': 'GE4/6'}],
                                                             'interfaces': {'GE1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_base.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict()


def test_cdp_drawing_yed_data_path():
    data = "./Data/SAMPLE_CDP_LLDP/"
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                                                            'src_label': 'GE4/6',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                                                            'trgt_label': 'GE1/5'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'GE1/1',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                                                            'trgt_label': 'GE0/1'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'GE1/2',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                                                            'trgt_label': 'GE0/10'}],
                                                             'interfaces': {'GE1/1': {'description': 'switch-3:Gi0/1',
                                                                                      'is_l2': True,
                                                                                      'l2_mode': 'trunk',
                                                                                      'mtu': '9216',
                                                                                      'trunk_vlans': '1771,1887'},
                                                                                'GE1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                                                                'GE4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
                                                'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                                                            'src_label': 'GE1/5',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                                                            'trgt_label': 'GE4/6'}],
                                                             'interfaces': {'GE1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_base.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_path()

def test_cdp_drawing_yed_data_dict_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {
        "add_lag": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_add_lag.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_add_lag.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_add_lag.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_add_lag()

def test_cdp_drawing_yed_data_dict_group_links():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {
        "group_links": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_group_links.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_group_links.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_group_links.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_group_links()

def test_cdp_drawing_yed_data_dict_group_links_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/8,  Port ID (outgoing port): GigabitEthernet1/8

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/24,  Port ID (outgoing port): GigabitEthernet0/14

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-2: trunk standalone
 switchport
 switchport trunk allowed vlan 300-305
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
interface GigabitEthernet1/24
 description SW4 Routing Peering VRF2
 vrf forwarding VRF2
 ip address 10.0.1.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/8,  Port ID (outgoing port): GigabitEthernet4/8

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/8
 description switch-1: trunk standalone
 switchport
 switchport trunk allowed vlan 300-305
 switchport mode trunk
    """
        ]
    }
    config = {
        "group_links": True,
        "add_lag": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_group_links_add_lag.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_group_links_add_lag.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_group_links_add_lag.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_group_links_add_lag()

def test_lldp_drawing_yed_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
------------------------------------------------
Local Intf: GigabitEthernet4/6
Port id: GigabitEthernet1/5
System Name: switch-2.com

System Capabilities: B,R
Management Addresses:
    IP: 10.2.2.2

------------------------------------------------
Local Intf: GigabitEthernet1/1
Port id: GigabitEthernet0/1
System Name: switch-3.com

System Capabilities: B,R
Management Addresses:
    IP: 10.3.3.3

------------------------------------------------
Local Intf: GigabitEthernet1/2
Port id: GigabitEthernet0/10
System Name: switch-4.com

System Capabilities: B,R
Management Addresses:
    IP: 10.4.4.4

switch-1#show run
interface GigabitEthernet4/6
 description switch-2: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 1771,1887
 switchport mode trunk
 mtu 9216
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
------------------------------------------------
Local Intf: GigabitEthernet1/5
Port id: GigabitEthernet4/6
System Name: switch-1.com

System Capabilities: B,R
Management Addresses:
    IP: 10.1.1.1

switch-2#show run
interface GigabitEthernet1/5
 description switch-1: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_lldp_drawing_yed_data_dict.graphml", folder="./Output/")
    with open ("./Output/test_lldp_drawing_yed_data_dict.graphml") as produced:
        with open("./Output/should_be_test_lldp_drawing_yed_data_dict.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_lldp_drawing_yed_data_dict()

def test_cdp_drawing_yed_data_dict_add_vlans_to_nodes():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_add_vlans_to_nodes.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_add_vlans_to_nodes.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_add_vlans_to_nodes.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_add_vlans_to_nodes()

def test_cdp_drawing_yed_data_dict_interfaces_state():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_interfaces_state.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_interfaces_state.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_interfaces_state.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_interfaces_state()

def test_cdp_drawing_yed_data_dict_lag_interfaces_state():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {"add_lag": True}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_lag_interfaces_state.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_lag_interfaces_state.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_lag_interfaces_state.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_lag_interfaces_state()

def test_cdp_drawing_yed_data_dict_add_all_connected():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
!
interface GigabitEthernet4/9
 switchport
 switchport trunk allowed vlan 230
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
!
GigabitEthernet4/8 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4848 (bia a89d.2163.4848)
  Description: switch-22: trunk
  MTU 5000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
GigabitEthernet4/9 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {"add_all_connected": True}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_add_all_connected.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_add_all_connected.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_add_all_connected.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_add_all_connected()

def test_cdp_drawing_yed_data_dict_add_all_connected_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface Port-channel48
 description switch-22:LAG trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
 channel-group 48 mode active
!
interface GigabitEthernet5/1
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
 channel-group 48 mode active
!
interface GigabitEthernet4/9
 switchport
 switchport trunk allowed vlan 230
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
!
GigabitEthernet4/8 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4848 (bia a89d.2163.4848)
  Description: switch-22: trunk
  MTU 5000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel48 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-22:LAG trunk
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/8
!
GigabitEthernet4/9 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
GigabitEthernet5/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {"add_all_connected": True, "add_lag": True}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_add_all_connected_add_lag.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_add_all_connected_add_lag.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_add_all_connected_add_lag.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_dict_add_all_connected_add_lag()

def test_cdp_drawing_drawio_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface GigabitEthernet4/6
 description switch-2: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 1771,1887
 switchport mode trunk
 mtu 9216
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

switch-2#show run
interface GigabitEthernet1/5
 description switch-1: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
    """
        ]
    }
    config = {}
    lldp_drawing = create_drawio_diagram()
    drawer = cli_l2_data(lldp_drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_or_path.drawio") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_drawio_data_dict()

def test_cdp_drawing_drawio_data_path():
    data = "./Data/SAMPLE_CDP_LLDP/"
    config = {}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_path.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_path.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_or_path.drawio") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_drawio_data_path()

def test_cdp_drawing_drawio_data_dict_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {
        "add_lag": True
    }
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_add_lag.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_add_lag.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_add_lag.drawio") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_drawio_data_dict_add_lag()

def test_cdp_drawing_drawio_data_dict_group_links():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {
        "group_links": True
    }
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_group_links.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_group_links.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_group_links.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_drawio_data_dict_group_links_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/8,  Port ID (outgoing port): GigabitEthernet1/8

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/24,  Port ID (outgoing port): GigabitEthernet0/14

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-2: trunk standalone
 switchport
 switchport trunk allowed vlan 300-305
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
interface GigabitEthernet1/24
 description SW4 Routing Peering VRF2
 vrf forwarding VRF2
 ip address 10.0.1.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/8,  Port ID (outgoing port): GigabitEthernet4/8

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/8
 description switch-1: trunk standalone
 switchport
 switchport trunk allowed vlan 300-305
 switchport mode trunk
    """
        ]
    }
    config = {
        "group_links": True,
        "add_lag": True
    }
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_group_links_add_lag.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_group_links_add_lag.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_group_links_add_lag.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_lldp_drawing_drawio_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
------------------------------------------------
Local Intf: GigabitEthernet4/6
Port id: GigabitEthernet1/5
System Name: switch-2.com

System Capabilities: B,R
Management Addresses:
    IP: 10.2.2.2

------------------------------------------------
Local Intf: GigabitEthernet1/1
Port id: GigabitEthernet0/1
System Name: switch-3.com

System Capabilities: B,R
Management Addresses:
    IP: 10.3.3.3

------------------------------------------------
Local Intf: GigabitEthernet1/2
Port id: GigabitEthernet0/10
System Name: switch-4.com

System Capabilities: B,R
Management Addresses:
    IP: 10.4.4.4

switch-1#show run
interface GigabitEthernet4/6
 description switch-2: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 1771,1887
 switchport mode trunk
 mtu 9216
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail
------------------------------------------------
Local Intf: GigabitEthernet1/5
Port id: GigabitEthernet4/6
System Name: switch-1.com

System Capabilities: B,R
Management Addresses:
    IP: 10.1.1.1

switch-2#show run
interface GigabitEthernet1/5
 description switch-1: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
    """
        ]
    }
    config = {}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_lldp_drawing_drawio_data_dict.drawio", folder="./Output/")
    with open ("./Output/test_lldp_drawing_drawio_data_dict.drawio") as produced:
        with open("./Output/should_be_test_lldp_drawing_drawio_data_dict.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_drawio_data_dict_add_vlans_to_nodes():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_add_vlans_to_nodes.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_add_vlans_to_nodes.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_add_vlans_to_nodes.drawio") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_drawio_data_dict_add_vlans_to_nodes()

def test_cdp_drawing_drawio_data_dict_interfaces_state():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
vlan 200
 name ProdVMS
!
vlan 101
 name test_vlan
    """
        ]
    }
    config = {}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_interfaces_state.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_interfaces_state.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_interfaces_state.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_drawio_data_dict_add_all_connected():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
!
interface GigabitEthernet4/9
 switchport
 switchport trunk allowed vlan 230
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
!
GigabitEthernet4/8 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4848 (bia a89d.2163.4848)
  Description: switch-22: trunk
  MTU 5000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
GigabitEthernet4/9 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {"add_all_connected": True}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_add_all_connected.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_add_all_connected.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_add_all_connected.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_drawio_data_dict_add_all_connected_add_lag():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail
-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-2
Entry address(es):
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet4/7,  Port ID (outgoing port): GigabitEthernet1/6

-------------------------
Device ID: switch-3
Entry address(es):
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es):
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface Port-channel3
 description switch-2: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface Port-channel11
 description switch-3: trunk LAG
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
!
interface Port-channel48
 description switch-22:LAG trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
!
interface GigabitEthernet4/6
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/7
 description switch-2: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet4/8
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
 channel-group 48 mode active
!
interface GigabitEthernet5/1
 description switch-22: trunk
 switchport
 switchport trunk allowed vlan 209
 switchport mode trunk
 channel-group 48 mode active
!
interface GigabitEthernet4/9
 switchport
 switchport trunk allowed vlan 230
 switchport mode trunk
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 101
 switchport mode trunk
 mtu 9216
 channel-group 11 mode active
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
!
switch-1#show interface
GigabitEthernet1/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.1111 (bia a89d.2163.1111)
  Description: switch-3:Gi0/1
  MTU 9216 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, link type is auto, media type is 10GBase-LR
!
GigabitEthernet1/2 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.2222 (bia a89d.2163.2222)
  Description: SW4 Routing Peering
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel3 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-2: trunk LAG
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/6 Ge4/7
!
GigabitEthernet4/8 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4848 (bia a89d.2163.4848)
  Description: switch-22: trunk
  MTU 5000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
Port-channel48 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is a89d.2163.3333 (bia a89d.2163.333)
  Description: switch-22:LAG trunk
  MTU 1500 bytes, BW 20000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 10Gb/s, media type is N/A
  Members in this channel: Ge4/8 Gi5/1
!
GigabitEthernet4/9 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
!
GigabitEthernet5/1 is up, line protocol is up (connected)
  Hardware is Ten Gigabit Ethernet Port, address is a89d.2163.4949 (bia a89d.2163.4949)
  MTU 7000 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
  Full-duplex, 1000Mb/s, link type is auto, media type is 1000BaseT
    """,
    """
switch-2#show cdp neighbors detail
-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6

-------------------------
Device ID: switch-1
Entry address(es):
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet4/7

switch-2#show run
interface Port-channel3
 description switch-1: trunk LAG
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
!
interface GigabitEthernet1/5
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
!
interface GigabitEthernet1/6
 description switch-1: trunk
 switchport
 switchport trunk allowed vlan 200-205
 switchport mode trunk
 channel-group 3 mode active
    """
        ]
    }
    config = {"add_all_connected": True, "add_lag": True}
    drawing = create_drawio_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_drawio_data_dict_add_all_connected_add_lag.drawio", folder="./Output/")
    with open ("./Output/test_cdp_drawing_drawio_data_dict_add_all_connected_add_lag.drawio") as produced:
        with open("./Output/should_be_test_cdp_drawing_drawio_data_dict_add_all_connected_add_lag.drawio") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_dict_cisco_nxos_base():
    data = { "Cisco_NXOS": [
    """
nxos_switch_1# show cdp nei det
----------------------------------------
Device ID:nxos_switch_2(JPG2212345)
System Name: nxos_switch_2

Interface address(es):
    IPv4 Address: 10.2.2.2
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet2/29
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

nxos_switch_1# show lldp nei det
Chassis id: 501c.b09b.1111
Port id: Eth2/29
Local Port id: Eth5/15
Port Description: uplink to ISP via nxos_switch_1
System Name: cust_sw_1
System Description: Cisco NX-OS(tm) n7700, Software (n7700-s3-dk9), Version 91.3(1), RELEASE SOFTWARE Copyright (c) 2002-2003 by Cisco Systems, Inc. Compiled 7/30/2003 12:00:00
Time remaining: 95 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.151.1.1
Vlan ID: not advertised

nxos_switch_1# show run int
interface Ethernet5/1
  description nxos_switch_2:eth2/29 [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.1/30
  vrf member VRF1
  ip address 2.2.2.2/32 secondary
!
interface Ethernet5/15
  description cust_sw_1 Eth2/29
  switchport
  switchport mode trunk
  switchport trunk allowed vlan 2122
  mtu 9216

nxos_switch_1# show interface
Ethernet5/1 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.1234 (bia 00b0.1111.4444)
  Description: nxos_switch_2:eth2/29
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

Ethernet5/15 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.1592 (bia 00b0.1111.9999)
  Description: cust_sw_1 Eth2/29
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is trunk
  full-duplex, 10 Gb/s, media type is 10G
    """,
    """
nxos_switch_2# show cdp nei det
----------------------------------------
Device ID:nxos_switch_1(JPG2212345)
System Name: nxos_switch_1

Interface address(es):
    IPv4 Address: 10.1.1.1
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet2/29, Port ID (outgoing port): Ethernet5/1
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.1.1.1

nxos_switch_1# show lldp nei det
Chassis id: 1409.dcaf.5555
Port id: 10GE1/17/21
Local Port id: Eth5/31
Port Description: cust_sw_3
System Name: cust_sw_3
System Description: Huawei Versatile Routing Platform Software
VRP (R) software, Version 8.120 (OSCA V100R005C60)
Copyright (C) 2012-2016 Huawei Technologies Co., Ltd.
HUAWEI OSCA

Time remaining: 113 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.152.3.4
Vlan ID: 1

nxos_switch_1# show interface
Ethernet2/29 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.4321 (bia 00b0.1111.3333)
  Description: nxos_switch_1:eth5/1
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

Ethernet5/31 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.3131 (bia 00b0.1111.3131)
  Description: cust_sw_3 10GE1/17/21
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

nxos_switch_1# show run int
interface Ethernet2/29
  description nxos_switch_1:eth5/1 [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.2/30
  vrf member VRF1
  ip address 2.2.2.3/32 secondary
!
interface Ethernet5/31
  description cust_sw_3 10GE1/17/21
  switchport
  switchport mode trunk
  switchport trunk native vlan 777
  switchport trunk allowed vlan 777,1,2,3,4
    """]
    }
    config = {
        "platforms": ["Cisco_NXOS", "Cisco_IOS"]
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_nxos_base.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_nxos_base.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_nxos_base.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_cdp_drawing_yed_data_path_cisco_nxos()

def test_cdp_drawing_yed_data_path_cisco_ios_nxos_all():
    data = "./Data/SAMPLE_CDP_LLDP_2/"
    config = {
        "platforms": ["Cisco_NXOS", "Cisco_IOS"],
        "add_all_connected": True,
        "add_lag": True,
        "group_links": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path_cisco_ios_nxos_all.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path_cisco_ios_nxos_all.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_path_cisco_ios_nxos_all.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_path_cisco_nxos_base():
    data = "./Data/SAMPLE_CDP_LLDP_2/"
    config = {
        "platforms": ["Cisco_NXOS"]
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path_cisco_nxos_base.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path_cisco_nxos_base.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_path_cisco_nxos_base.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_path_cisco_nxos_combine_peers():
    data = "./Data/SAMPLE_CDP_LLDP_2/"
    config = {
        "platforms": ["Cisco_NXOS"],
        "combine_peers": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path_cisco_nxos_combine_peers.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path_cisco_nxos_combine_peers.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_path_cisco_nxos_combine_peers.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_has_data():
    data = { "Cisco_NXOS": [
    """
nxos_switch_1# show cdp nei det
----------------------------------------
Device ID:nxos_switch_2(JPG2212345)
System Name: nxos_switch_2

Interface address(es):
    IPv4 Address: 10.2.2.2
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet2/29
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

----------------------------------------
Device ID:nxos_switch_3(JPG2212343)
System Name: nxos_switch_3

Interface address(es):
    IPv4 Address: 10.3.3.3
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet1/33
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

nxos_switch_1# show run int
interface Ethernet5/1
  description nxos_switch_2/3: [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.1/30
  vrf member VRF1
  ip address 2.2.2.2/32 secondary

nxos_switch_1# show interface
Ethernet5/1 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.1234 (bia 00b0.1111.4444)
  Description: nxos_switch_2/3: [L3]
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G
    """,
    """
nxos_switch_2# show cdp nei det
----------------------------------------
Device ID:nxos_switch_1(JPG2212345)
System Name: nxos_switch_1

Interface address(es):
    IPv4 Address: 10.1.1.1
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet2/29, Port ID (outgoing port): Ethernet5/1
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.1.1.1

Time remaining: 113 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.152.3.4
Vlan ID: 1

nxos_switch_1# show interface
Ethernet2/29 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.4321 (bia 00b0.1111.3333)
  Description: nxos_switch_1:eth5/1
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

nxos_switch_1# show run int
interface Ethernet2/29
  description nxos_switch_1:eth5/1 [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.2/30
  vrf member VRF1
  ip address 2.2.2.3/32 secondary
    """]
    }
    config = {
        "combine_peers": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_has_data.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_has_data.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_has_data.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_two_links():
    data = { "Cisco_NXOS": [
    """
nxos_switch_1# show cdp nei det
----------------------------------------
Device ID:nxos_switch_2(JPG2212345)
System Name: nxos_switch_2

Interface address(es):
    IPv4 Address: 10.2.2.2
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet2/29
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

----------------------------------------
Device ID:nxos_switch_3(JPG2212343)
System Name: nxos_switch_3

Interface address(es):
    IPv4 Address: 10.3.3.3
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet1/33
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

----------------------------------------
Device ID:nxos_switch_2(JPG2212345)
System Name: nxos_switch_2

Interface address(es):
    IPv4 Address: 10.2.2.2
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/11, Port ID (outgoing port): Ethernet2/30
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

----------------------------------------
Device ID:nxos_switch_3(JPG2212343)
System Name: nxos_switch_3

Interface address(es):
    IPv4 Address: 10.3.3.3
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/11, Port ID (outgoing port): Ethernet1/34
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

nxos_switch_1# show run int
interface Ethernet5/1
  description nxos_switch_2/3: [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.1/30
  vrf member VRF1
  ip address 2.2.2.2/32 secondary

nxos_switch_1# show interface
Ethernet5/1 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.1234 (bia 00b0.1111.4444)
  Description: nxos_switch_2/3: [L3]
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G
    """,
    """
nxos_switch_2# show cdp nei det
----------------------------------------
Device ID:nxos_switch_1(JPG2212345)
System Name: nxos_switch_1

Interface address(es):
    IPv4 Address: 10.1.1.1
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet2/29, Port ID (outgoing port): Ethernet5/1
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.1.1.1

Time remaining: 113 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.152.3.4
Vlan ID: 1

nxos_switch_1# show interface
Ethernet2/29 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.4321 (bia 00b0.1111.3333)
  Description: nxos_switch_1:eth5/1
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

nxos_switch_1# show run int
interface Ethernet2/29
  description nxos_switch_1:eth5/1 [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.2/30
  vrf member VRF1
  ip address 2.2.2.3/32 secondary
    """]
    }
    config = {
        "combine_peers": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_two_links.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_two_links.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_two_links.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_behind_lag():
    data = { "Cisco_NXOS": [
    """
nxos_switch_1# show cdp nei det
----------------------------------------
Device ID:nxos_switch_2(JPG2212345)
System Name: nxos_switch_2

Interface address(es):
    IPv4 Address: 10.2.2.2
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet2/29
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

----------------------------------------
Device ID:nxos_switch_3(JPG2212343)
System Name: nxos_switch_3

Interface address(es):
    IPv4 Address: 10.3.3.3
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet5/1, Port ID (outgoing port): Ethernet1/33
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.2.2.2

nxos_switch_1# show run int
interface Port-channel51
  description nxos_switch_2/3: [L2]
  switchport
  switchport trunk allowed vlan 209
  switchport mode trunk
!
interface Ethernet5/1
  description nxos_switch_2/3: [L2, LAG 51]
  switchport
  switchport trunk allowed vlan 209
  switchport mode trunk
  channel-group 51 mode active

nxos_switch_1# show interface
Port-channel51 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.1234 (bia 00b0.1111.4444)
  Description: nxos_switch_2/3: [L2]
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is trunk
  full-duplex, 10 Gb/s, media type is 10G
    """,
    """
nxos_switch_2# show cdp nei det
----------------------------------------
Device ID:nxos_switch_1(JPG2212345)
System Name: nxos_switch_1

Interface address(es):
    IPv4 Address: 10.1.1.1
Platform: N77-C7711, Capabilities: Router Switch Supports-STP-Dispute
Interface: Ethernet2/29, Port ID (outgoing port): Ethernet5/1
Holdtime: 152 sec

Version:
Cisco Nexus Operating System (NX-OS) Software, Version 18.5(1 )

Advertisement Version: 2
Duplex: full

MTU: 9216
Physical Location: rack, street address
Mgmt address(es):
    IPv4 Address: 10.1.1.1

Time remaining: 113 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.152.3.4
Vlan ID: 1

nxos_switch_1# show interface
Ethernet2/29 is up
admin state is up, Dedicated Interface
  Hardware: 1000/10000 Ethernet, address: 8c60.4f53.4321 (bia 00b0.1111.3333)
  Description: nxos_switch_1:eth5/1
  MTU 9216 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, medium is broadcast
  Port mode is routed
  full-duplex, 10 Gb/s, media type is 10G

nxos_switch_1# show run int
interface Ethernet2/29
  description nxos_switch_1:eth5/1 [L3]
  mpls ip
  mtu 9216
  ip address 1.1.1.2/30
  vrf member VRF1
  ip address 2.2.2.3/32 secondary
    """]
    }
    config = {
        "combine_peers": True,
        "add_lag": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_behind_lag.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_behind_lag.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_nxos_combine_peer_behind_lag.graphml") as should_be:
            assert produced.read() == should_be.read()

def test_cdp_drawing_yed_data_dict_cisco_iosxr():
    data = { "Cisco_IOSXR": [
    """
RP/0/RSP0/CPU0:router_XR_01#show run
interface GigabitEthernet0/0/0/19
 description To cust_rt_1  Gi1/1
 mtu 4484
 ipv4 address 10.0.0.1 255.255.255.192
!
interface TenGigE0/0/2/0
 description To cust_rt_2 Gi1/2
 mtu 4484
 ipv4 address 10.1.0.1 255.255.255.192
 ipv6 address 2001::4321/64 eui-64

RP/0/RSP0/CPU0:router_XR_01#show lldp neighbors detail
------------------------------------------------
Local Interface: GigabitEthernet0/0/0/8
Chassis id: 0026.9815.c3e6
Port id: Gi0/0/0/8
Port Description: GigabitEthernet0/0/0/8 peer
System Name: asr9k-5

System Description: 
Cisco IOS XR Software, Version 4.1.0.32I[Default]
Copyright (c) 2011 by Cisco Systems, Inc.

Time remaining: 102 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 10.5.173.110
  
RP/0/RSP0/CPU0:router_XR_01#show cdp neighbors detail
-------------------------
Device ID: cust_rt_1(FGE1234567)
SysName :
Entry address(es):
  IPv4 address: 10.0.0.2
Platform: Cisco CISCO3945-CHASSIS,  Capabilities: Router Source-Route-Bridge Switch IGMP
Interface:  GigabitEthernet0/0/0/19
Port ID (outgoing port): GigabitEthernet1/1
Holdtime : 147 sec

Version :
Cisco IOS Software, C3900 Software (C3900-UNIVERSALK9-M), Version 15.4(3)M1, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Sat 25-Oct-14 07:15 by prod_rel_team

advertisement version: 2
Duplex: full

-------------------------
Device ID: cust_rt_2
SysName :
Entry address(es):
  IPv4 address: 10.1.0.1
  IPv6 address: fe80::5e5a:feed:1234:1234
Platform: cisco ASR1001-X,  Capabilities: Router IGMP
Interface: TenGigE0/0/2/0
Port ID (outgoing port): GigabitEthernet1/2
Holdtime : 139 sec

Version :
Cisco IOS Software [Fuji], ASR1000 Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.2, RELEASE SOFTWARE (fc4)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2018 by Cisco Systems, Inc.
Compiled Mon 05-Nov-18 19:31 by mcpre

advertisement version: 2
Duplex: full

RP/0/RSP0/CPU0:router_XR_01#show interfaces
GigabitEthernet0/0/0/19 is up, line protocol is up
  Interface state transitions: 1
  Hardware is GigabitEthernet, address is 4321.f54f.1234 (bia 4321.f54f.1234)
  Description: To cust_rt_1  Gi1/1
  Internet address is 10.0.0.1/26
  MTU 4484 bytes, BW 1000000 Kbit (Max: 1000000 Kbit)
  Full-duplex, 1000Mb/s, TFD, link type is force-up

TenGigE0/0/2/0 is up, line protocol is up
  Interface state transitions: 1
  Hardware is TenGigE, address is 08ec.6789.68e9 (bia 08ec.6789.68e9)
  Layer 1 Transport Mode is LAN
  Description: To cust_rt_2 Gi1/2
  Internet address is 10.1.0.1/26
  MTU 4484 bytes, BW 10000000 Kbit (Max: 10000000 Kbit)
  Full-duplex, 10000Mb/s, LR, link type is force-up
    """,
    """
RP/0/RSP0/CPU0:cust_rt_1#show run
interface GigabitEthernet1/1
 description To cust_rt_1  Gi0/0/19
 mtu 4484
 ipv4 address 10.0.0.2 255.255.255.192
 vrf UPSTREAM

RP/0/RSP0/CPU0:cust_rt_1#show cdp neighbors detail
-------------------------
Device ID: router_XR_01
SysName :
Entry address(es):
  IPv4 address: 10.0.0.1
Platform: Cisco ASR9001,  Capabilities: Router Source-Route-Bridge Switch IGMP
Interface:  GigabitEthernet1/1
Port ID (outgoing port): GigabitEthernet0/0/0/19
Holdtime : 147 sec
    """]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_iosxr.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_iosxr.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_iosxr.graphml") as should_be:
            assert produced.read() == should_be.read()
            
def test_cdp_drawing_yed_data_dict_huawei_base():
    data = { "Huawei": [
    """
<HUAWEI-CSW-01>disp cur interface
interface 10GE4/0/17
 description TO-SLB-FF_21  Eth9
 ip binding vpn-instance SLB-F
 ip address 10.123.0.5 255.255.255.252
 dot1q termination vid 619
#
interface 10GE4/0/9
 description LINK:R-RR1-TOR-581:10GE2/0/5
 eth-trunk 11
#
interface Eth-Trunk11
 description LINK:R-RR1-TOR-581:LAG
 port link-type trunk
 port trunk allow-pass vlan 200 210 220 230 240 280 290 300 310 320
 port trunk allow-pass vlan 330 340 1201 to 1223
 mode lacp-static
 dfs-group 1 m-lag 11
 
<HUAWEI-CSW-01>disp lldp neighbor
10GE4/0/17 has 1 neighbor(s):

Port ID                            :Ethernet9
Port description                   :UPLINK to CSW  10GE4/0/17
System name                        :SLB-FF_21           
System description                 :SLB Vendor BLA
System capabilities supported      :bridge router
Management address                 :10.132.77.91
Maximum frame Size                 :9123

10GE4/0/9 has 1 neighbor(s):

Port ID                            :10GE2/0/5
Port description                   :UPLINK to CSW 10GE4/0/9
System name                        :R-RR1-TOR-581      
System description                 :Huawei Versatile Routing Platform Software
VRP (R) software, Version 8.150 (NE40E V800R009C10SPC200)
Copyright (C) 2012-2017 Huawei Technologies Co., Ltd.
HUAWEI NE40E-X8A
System capabilities supported      :bridge router
Management address                 :10.1.1.2
Maximum frame Size                 :9216

<HUAWEI-CSW-01>disp cur vlan
vlan 1201
 name Servers_vlan
vlan 1223 
 name SEC_staff
    """,
    """
<HUAWEI-CSW-02>disp cur interface
interface 10GE4/0/19
 description TO-SLB-FF_22  Eth99
 ip binding vpn-instance SLB-F
 ip address 10.123.0.3 255.255.255.252
#
interface 10GE4/0/9
 description LINK:R-RR1-TOR-581:10GE2/0/6
 eth-trunk 11
#
interface Eth-Trunk11
 description LINK:R-RR1-TOR-581:LAG
 port link-type trunk
 port trunk allow-pass vlan 200 210 220 230 240 280 290 300 310 320
 port trunk allow-pass vlan 330 340 1201 to 1223
 mode lacp-static
 dfs-group 1 m-lag 11
 
<HUAWEI-CSW-01>disp lldp neighbor
10GE4/0/19 has 1 neighbor(s):

Port ID                            :Ethernet99
Port description                   :UPLINK to CSW2  10GE4/0/19
System name                        :SLB-FF_22          
System description                 :SLB Vendor BLA
System capabilities supported      :bridge router
Management address                 :10.132.77.92
Maximum frame Size                 :9123

10GE4/0/9 has 1 neighbor(s):

Port ID                            :10GE2/0/6
Port description                   :UPLINK to CSW2 10GE4/0/9
System name                        :R-RR1-TOR-581      
System description                 :Huawei Versatile Routing Platform Software
VRP (R) software, Version 8.150 (NE40E V800R009C10SPC200)
Copyright (C) 2012-2017 Huawei Technologies Co., Ltd.
HUAWEI NE40E-X8A
System capabilities supported      :bridge router
Management address                 :10.1.1.2
Maximum frame Size                 :9216
    """    
        ]
    }
    config = {
        # "add_lag": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_huawei_base.graphml", folder="./Output/")    
    
def test_cdp_drawing_yed_data_dict_cisco_iosxr_lldp_behind_lag():
    data = { "Cisco_IOSXR": [
    """
RP/0/RSP0/CPU0:router_XR_01#show run
interface GigabitEthernet0/0/0/19
 description To cust_rt_1  Gi0/0/0/8
 bundle id 100 mode active
!
interface Bundle-Ether100
 description To router_XR_01  Gi0/0/19 LAG 200
 
RP/0/RSP0/CPU0:router_XR_01#show lldp neighbors detail
------------------------------------------------
Local Interface: GigabitEthernet0/0/0/19
Chassis id: 0026.9815.c3e6
Port id: GigabitEthernet0/0/0/8
Port Description: To router_XR_01  Gi0/0/19
System Name: cust_rt_1

System Description: 
Cisco IOS XR Software, Version 4.1.0.32I[Default]
Copyright (c) 2011 by Cisco Systems, Inc.

Time remaining: 102 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 10.5.173.110

------------------------------------------------
Local Interface: GigabitEthernet0/0/0/19
Chassis id: 0026.9815.c3e6
Port id: Bundle-Ether200
Port Description: To router_XR_01  Gi0/0/19 LAG 100
System Name: cust_rt_1

System Description: 
Cisco IOS XR Software, Version 4.1.0.32I[Default]
Copyright (c) 2011 by Cisco Systems, Inc.

Time remaining: 102 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 10.5.173.110
    """,
    """
RP/0/RSP0/CPU0:cust_rt_1#show run
interface GigabitEthernet0/0/0/8
 description To router_XR_01  Gi0/0/19
 bundle id 200 mode active
!
interface Bundle-Ether200
 description To router_XR_01  Gi0/0/19 LAG 100
 
RP/0/RSP0/CPU0:cust_rt_1#show lldp neighbors detail
------------------------------------------------
Local Interface: GigabitEthernet0/0/0/8
Chassis id: 0026.9815.c3e6
Port id: GigabitEthernet0/0/0/19
Port Description: To cust_rt_1  Gi0/0/0/8
System Name: router_XR_01

System Description: 
Cisco IOS XR Software, Version 4.1.0.32I[Default]
Copyright (c) 2011 by Cisco Systems, Inc.

Time remaining: 102 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 10.5.173.111
    """]
    }
    config = {
        "add_lag": True
    }
    drawing = create_yed_diagram()
    drawer = cli_l2_data(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_cisco_iosxr_lldp_behind_lag.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_cisco_iosxr_lldp_behind_lag.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_cisco_iosxr_lldp_behind_lag.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_cdp_drawing_yed_data_dict_cisco_iosxr_lldp_behind_lag()