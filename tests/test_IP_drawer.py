import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G.N2G_IP_Drawer import ip_drawer

def test_ip_drawing_yed_data_dict_base():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.4 255.255.255.255
!
interface TenGigabitEthernet1/1/3
 description to SWITCH_2 vrf VRF1 link 1
 vrf forwarding VRF2
 ip address 10.123.2.3 255.255.255.254
!
interface TenGigabitEthernet1/1/4
 description to SWITCH_2 vrf VRF1 link 2
 vrf forwarding VRF2
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
!
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary
    """,
    """
switch_2# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.5 255.255.255.255
!
interface GigabitEthernet1/3
 description to SWITCH_1 link 1
 vrf forwarding VRF1
 ip address 10.123.2.2 255.255.255.254
!
interface GigabitEthernet1/4
 description to SWITCH_1 links 2
 vrf forwarding VRF1
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
!
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
    """]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = ip_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_base.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_base.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_base.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ip_drawing_yed_data_dict_base()

def test_ip_drawing_yed_data_dict_group_links():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.4 255.255.255.255
!
interface TenGigabitEthernet1/1/3
 description to SWITCH_2 vrf VRF1 link 1
 vrf forwarding VRF2
 ip address 10.123.2.3 255.255.255.254
!
interface TenGigabitEthernet1/1/4
 description to SWITCH_2 vrf VRF1 link 2
 vrf forwarding VRF2
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
!
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary
    """,
    """
switch_2# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.5 255.255.255.255
!
interface GigabitEthernet1/3
 description to SWITCH_1 link 1
 vrf forwarding VRF1
 ip address 10.123.2.2 255.255.255.254
!
interface GigabitEthernet1/4
 description to SWITCH_1 links 2
 vrf forwarding VRF1
 ip address 10.123.2.5 255.255.255.254
!
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
!
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
    """]
    }
    config = {
        "group_links": True
    }
    drawing = create_yed_diagram()
    drawer = ip_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_group_links.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_group_links.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_group_links.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_ip_drawing_yed_data_dict_group_links()

def test_ip_drawing_yed_data_dict_add_vrf_link_label():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.4 255.255.255.255
!
interface TenGigabitEthernet1/1/3
 description to SWITCH_2 vrf VRF1 link 1
 vrf forwarding VRF2
 ip address 10.123.2.3 255.255.255.254
!
interface TenGigabitEthernet1/1/4
 description to SWITCH_2 vrf VRF1 link 2
 vrf forwarding VRF2
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
!
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary
    """,
    """
switch_2# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.5 255.255.255.255
!
interface GigabitEthernet1/3
 description to SWITCH_1 link 1
 vrf forwarding VRF1
 ip address 10.123.2.2 255.255.255.254
!
interface GigabitEthernet1/4
 description to SWITCH_1 links 2
 vrf forwarding VRF1
 ip address 10.123.2.5 255.255.255.254
!
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
!
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
    """]
    }
    config = {
        "label_vrf": True
    }
    drawing = create_yed_diagram()
    drawer = ip_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_vrf_link_label.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_vrf_link_label.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_vrf_link_label.graphml") as should_be:
            assert produced.read() == should_be.read()
            
def test_ip_drawing_yed_data_dict_add_interface_link_label():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.4 255.255.255.255
!
interface TenGigabitEthernet1/1/3
 description to SWITCH_2 vrf VRF1 link 1
 vrf forwarding VRF2
 ip address 10.123.2.3 255.255.255.254
!
interface TenGigabitEthernet1/1/4
 description to SWITCH_2 vrf VRF1 link 2
 vrf forwarding VRF2
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
!
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary
    """,
    """
switch_2# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.5 255.255.255.255
!
interface GigabitEthernet1/3
 description to SWITCH_1 link 1
 vrf forwarding VRF1
 ip address 10.123.2.2 255.255.255.254
!
interface GigabitEthernet1/4
 description to SWITCH_1 links 2
 vrf forwarding VRF1
 ip address 10.123.2.5 255.255.255.254
!
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
!
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
    """]
    }
    config = {
        "label_interface": True
    }
    drawing = create_yed_diagram()
    drawer = ip_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_interface_link_label.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_interface_link_label.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_interface_link_label.graphml") as should_be:
            assert produced.read() == should_be.read()
            
def test_ip_drawing_yed_data_dict_add_interface_vrf_link_label():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.4 255.255.255.255
!
interface TenGigabitEthernet1/1/3
 description to SWITCH_2 vrf VRF1 link 1
 vrf forwarding VRF2
 ip address 10.123.2.3 255.255.255.254
!
interface TenGigabitEthernet1/1/4
 description to SWITCH_2 vrf VRF1 link 2
 vrf forwarding VRF2
 ip address 10.123.2.4 255.255.255.254
!
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
!
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary
    """,
    """
switch_2# show run interfaces
interface Loopback0
 description Routing Loopback
 ip address 10.123.0.5 255.255.255.255
!
interface GigabitEthernet1/3
 description to SWITCH_1 link 1
 vrf forwarding VRF1
 ip address 10.123.2.2 255.255.255.254
!
interface GigabitEthernet1/4
 description to SWITCH_1 links 2
 vrf forwarding VRF1
 ip address 10.123.2.5 255.255.255.254
!
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
!
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
    """]
    }
    config = {
        "label_interface": True,
        "label_vrf": True
    }
    drawing = create_yed_diagram()
    drawer = ip_drawer(drawing, config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml") as should_be:
            assert produced.read() == should_be.read()