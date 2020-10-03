import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cdp_lldp_drawer

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
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                                                            'src_label': 'Ge4/6',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                                                            'trgt_label': 'Ge1/5'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'Ge1/1',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                                                            'trgt_label': 'Ge0/1'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'Ge1/2',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                                                            'trgt_label': 'Ge0/10'}],
                                                             'interfaces': {'Ge1/1': {'description': 'switch-3:Gi0/1',
                                                                                      'is_l2': True,
                                                                                      'l2_mode': 'trunk',
                                                                                      'mtu': '9216',
                                                                                      'trunk_vlans': '1771,1887'},
                                                                                'Ge1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                                                                'Ge4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
                                                'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                                                            'src_label': 'Ge1/5',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                                                            'trgt_label': 'Ge4/6'}],
                                                             'interfaces': {'Ge1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_base.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_cdp_drawing_yed_data_dict()


def test_cdp_drawing_yed_data_path():
    data = "./Data/SAMPLE_CDP_LLDP/"
    config = {}
    drawing = create_yed_diagram()
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                                                            'src_label': 'Ge4/6',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                                                            'trgt_label': 'Ge1/5'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'Ge1/1',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                                                            'trgt_label': 'Ge0/1'},
                                                                           {'source': 'switch-1',
                                                                            'src_label': 'Ge1/2',
                                                                            'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                                                            'trgt_label': 'Ge0/10'}],
                                                             'interfaces': {'Ge1/1': {'description': 'switch-3:Gi0/1',
                                                                                      'is_l2': True,
                                                                                      'l2_mode': 'trunk',
                                                                                      'mtu': '9216',
                                                                                      'trunk_vlans': '1771,1887'},
                                                                                'Ge1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                                                                'Ge4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
                                                'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                                                            'src_label': 'Ge1/5',
                                                                            'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                                                            'trgt_label': 'Ge4/6'}],
                                                             'interfaces': {'Ge1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
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
    drawer = cdp_lldp_drawer(drawing, config)
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
    drawer = cdp_lldp_drawer(drawing, config)
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
    drawer = cdp_lldp_drawer(drawing, config)
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
    drawer = cdp_lldp_drawer(drawing, config)
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
    drawer = cdp_lldp_drawer(drawing, config)
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
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict_interfaces_state.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict_interfaces_state.graphml") as produced:
        with open("./Output/should_be_test_cdp_drawing_yed_data_dict_interfaces_state.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_cdp_drawing_yed_data_dict_interfaces_state()