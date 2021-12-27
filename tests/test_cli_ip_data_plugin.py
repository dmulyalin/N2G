import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cli_ip_data

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
    drawer = cli_ip_data(drawing, **config)
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
    drawer = cli_ip_data(drawing, **config)
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
    drawer = cli_ip_data(drawing, **config)
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
    drawer = cli_ip_data(drawing, **config)
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
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_interface_vrf_link_label.graphml") as should_be:
            assert produced.read() == should_be.read()
            
def test_ip_drawing_yed_data_dict_add_arp():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
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

switch_1# show ip arp
Internet  10.123.111.1            -   d094.6643.1111  ARPA   Vlan123
Internet  10.123.111.3            0   0008.e3ff.1333  ARPA   Vlan123
Internet  10.123.111.4          106   d867.d9b7.1444  ARPA   Vlan123
Internet  10.123.111.5          106   d867.d9b7.1555  ARPA   Vlan123
Internet  10.123.233.1            -   0008.e3ff.2111  ARPA   Vlan123
Internet  10.123.233.3          166   d867.d9b7.2333  ARPA   Vlan123
Internet  10.123.233.4           31   0008.e3ff.2444  ARPA   Vlan123
Internet  10.123.233.6           31   0008.e3ff.2666  ARPA   Vlan123
Internet  10.1.234.1              -   d867.d9b7.1111  ARPA   TenGigabitEthernet1/1/7
Internet  10.1.234.2             31   0008.e3ff.1234  ARPA   TenGigabitEthernet1/1/7
Internet  10.1.234.3             31   0008.e3ff.4321  ARPA   TenGigabitEthernet1/1/7
    """,
    """
switch_2# show run interfaces
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
 
switch_2# show ip arp
Internet  10.22.22.1              -   d094.7890.1111  ARPA   Vlan22
Internet  10.22.22.3              0   0008.7890.1333  ARPA   Vlan22
Internet  10.22.22.4            106   d867.7890.1444  ARPA   Vlan22
Internet  10.1.234.1              5   d867.d9b7.1111  ARPA   TenGigabitEthernet1/1/71
Internet  10.1.234.2              -   0008.e3ff.1234  ARPA   TenGigabitEthernet1/1/71
Internet  10.1.234.3             78   0008.e3ff.4321  ARPA   TenGigabitEthernet1/1/71
    """]
    }
    config = {
        "add_arp": True
    }
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_arp.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_arp.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_arp.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ip_drawing_yed_data_dict_add_arp()

def test_ip_drawing_yed_data_dict_add_arp_and_fhrp():
    data = {"Cisco_IOS": ["""
switch_1# show run interfaces
interface TenGigabitEthernet1/1/5
 description to SWITCH_3
 ip address 10.1.33.1 255.255.255.0
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
interface TenGigabitEthernet1/1/7
 description to SWITCH_2 shared subnet
 ip address 10.1.234.1 255.255.255.0
 standby 1 10.1.234.99
!
interface Vlan123
 description Workstations Vlan
 vrf forwarding CORP
 ip address 10.123.111.1 255.255.255.0
 ip address 10.123.222.1 255.255.255.0 secondary
 ip address 10.123.233.1 255.255.255.0 secondary

switch_1# show ip arp
Internet  10.123.111.1            -   d094.6643.1111  ARPA   Vlan123
Internet  10.123.111.3            0   0008.e3ff.1333  ARPA   Vlan123
Internet  10.123.111.4          106   d867.d9b7.1444  ARPA   Vlan123
Internet  10.123.111.5          106   d867.d9b7.1555  ARPA   Vlan123
Internet  10.123.233.1            -   0008.e3ff.2111  ARPA   Vlan123
Internet  10.123.233.3          166   d867.d9b7.2333  ARPA   Vlan123
Internet  10.123.233.4           31   0008.e3ff.2444  ARPA   Vlan123
Internet  10.123.233.6           31   0008.e3ff.2666  ARPA   Vlan123
Internet  10.1.234.1              -   d867.d9b7.1111  ARPA   TenGigabitEthernet1/1/7
Internet  10.1.234.2             31   0008.e3ff.1234  ARPA   TenGigabitEthernet1/1/7
Internet  10.1.234.3             31   0008.e3ff.4321  ARPA   TenGigabitEthernet1/1/7
Internet  10.1.234.99             -   00ac.0007.001a  ARPA   TenGigabitEthernet1/1/7
    """,
    """
switch_2# show run interfaces
interface TenGigabitEthernet1/1/71
 description to SWITCH_2 shared subnet
 ip address 10.1.234.2 255.255.255.0
 standby 1 10.1.234.99
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
interface Vlan11
 description Workstations Vlan
 vrf forwarding Staff Workstations
 ip address 10.11.11.1 255.255.255.0
!
interface Vlan22
 description Workstations Vlan
 vrf forwarding Staff Phones
 ip address 10.22.22.1 255.255.255.0
 
switch_2# show ip arp
Internet  10.22.22.1              -   d094.7890.1111  ARPA   Vlan22
Internet  10.22.22.3              0   0008.7890.1333  ARPA   Vlan22
Internet  10.22.22.4            106   d867.7890.1444  ARPA   Vlan22
Internet  10.1.234.1              5   d867.d9b7.1111  ARPA   TenGigabitEthernet1/1/71
Internet  10.1.234.2              -   0008.e3ff.1234  ARPA   TenGigabitEthernet1/1/71
Internet  10.1.234.3             78   0008.e3ff.4321  ARPA   TenGigabitEthernet1/1/71
Internet  10.1.234.99             5   00ac.0007.001a  ARPA   TenGigabitEthernet1/1/71
    """]
    }
    config = {
        "add_arp": True,
        "add_fhrp": True,
        # "collapse_ptp": True
    }
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_add_arp_and_fhrp.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_add_arp_and_fhrp.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_add_arp_and_fhrp.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_ip_drawing_yed_data_dict_add_arp_and_fhrp()

def test_ip_drawing_yed_data_dict_nxos():
    data = {"Cisco_NXOS": ["""
switch_1# show run | sec interface
interface Vlan133
  description OOB
  vrf member MGMT_OOB
  ip address 10.133.137.2/24
  hsrp 133
    preempt 
    ip 10.133.137.1
!
interface Vlan134
  description OOB-2
  vrf member MGMT_OOB
  ip address 10.134.137.2/24
  vrrpv3 1334 address-family ipv4
    address 10.134.137.1 primary
!
interface Vlan222
  description PTP OSPF Routing pat to  siwtch2
  ip address 10.222.137.1/30
!
interface Vlan223
  description PTP OSPF Routing pat to siwtch3
  ip address 10.223.137.1/30
 
switch_1# show ip arp vrf all 
10.133.137.2    -  d094.7890.1111  Vlan133
10.133.137.1    -  d094.7890.1111  Vlan133
10.133.137.30   -  d094.7890.1234  Vlan133
10.133.137.91   -  d094.7890.4321  Vlan133
10.134.137.1    -  d094.7890.1111  Vlan134
10.134.137.2    -  d094.7890.1111  Vlan134
10.134.137.3   90  d094.7890.2222  Vlan134
10.134.137.31  91  d094.7890.beef  Vlan134
10.134.137.81  81  d094.7890.feeb  Vlan134
10.222.137.2   21  d094.7890.2222  Vlan222
    """,
    """
switch_2# show run | sec interface
interface Vlan134
  description OOB-2
  vrf member MGMT_OOB
  ip address 10.134.137.3/24
  vrrpv3 1334 address-family ipv4
    address 10.134.137.1 primary
!
interface Vlan222
  description PTP OSPF Routing pat to  siwtch1
  ip address 10.222.137.2/30
    """,
    """
switch_3# show run | sec interface
interface Vlan223
  description PTP OSPF Routing pat to siwtch1
  ip address 10.223.137.2/30
    """]
    }
    config = {
        "add_arp": True,
        "add_fhrp": True
    }
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_nxos.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_nxos.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_nxos.graphml") as should_be:
            assert produced.read() == should_be.read()
            
def test_ip_drawing_yed_data_dict_huawei():
    data = {"Huawei": ["""
<hua_sw1>dis current-configuration interface
#
interface Vlanif140
 ip binding vpn-instance VRF_MGMT
 ip address 10.1.1.2 255.255.255.0
 vrrp vrid 200 virtual-ip 10.1.1.1
#
interface Eth-Trunk5.123
 vlan-type dot1q 123
 description hua_sw2 BGP  peering
 ip binding vpn-instance VRF_MGMT
 ip address 10.0.0.1 255.255.255.252
 ipv6 address FD00:1::1/126
#
interface Eth-Trunk5.200
 vlan-type dot1q 200
 description hua_sw3 OSPF  peering
 ip address 192.168.2.2 255.255.255.252
 
<hua_sw1>dis arp all
10.1.1.2        a008-6fc1-1101        I         Vlanif140       VRF_MGMT
10.1.1.1        a008-6fc1-1102   0    D         Vlanif140       VRF_MGMT
10.1.1.3        a008-6fc1-1103   10   D/200     Vlanif140       VRF_MGMT
10.1.1.9        a008-6fc1-1104   10   D/200     Vlanif140       VRF_MGMT
10.0.0.2        a008-6fc1-1105   10   D/200     Eth-Trunk5.123  VRF_MGMT
    """,
    """
<hua_sw2>dis current-configuration interface
#
interface Vlanif140
 ip binding vpn-instance VRF_MGMT
 ip address 10.1.1.3 255.255.255.0
 vrrp vrid 200 virtual-ip 10.1.1.1
#
interface Eth-Trunk5.123
 vlan-type dot1q 123
 description hua_sw1 BGP  peering
 ip binding vpn-instance VRF_MGMT
 ip address 10.0.0.2 255.255.255.252
 ipv6 address FD00:1::2/126
    """,
    """
<hua_sw3>dis current-configuration interface
#
interface Vlanif200
 ip binding vpn-instance VRF_CUST1
 ip address 192.168.1.1 255.255.255.0
#
interface Eth-Trunk5.200
 vlan-type dot1q 200
 description hua_sw1 OSPF  peering
 ip address 192.168.2.1 255.255.255.252
 
<hua_sw3>dis arp
192.168.1.1         a008-6fc1-1111       I      Vlanif200 
192.168.1.10        a008-6fc1-1110   30  D/300  Vlanif200 
    """]
    }
    config = {
        "add_arp": True,
        "add_fhrp": True
    }
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_huawei.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_huawei.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_huawei.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_ip_drawing_yed_data_dict_huawei()

def test_ip_drawing_yed_data_dict_fortigate():
    data = {"Fortigate": ["""
forti-fw-01 (Corporate) # get system config 
config system interface
    edit "vms_vlan"
        set vdom "root"
        set ip 1.1.1.1 255.255.255.0
        set allowaccess ping https ssh snmp
        set description "VMs data vlan"
        set alias "vms_vlan"
        config secondaryip
            edit 1
                set ip 10.38.1.152 255.255.255.0
                set allowaccess ping
            next
        end
    next
    edit "NMS_mgmt"
        set vdom "root"
        set ip 10.0.0.1 255.255.255.0
        set allowaccess ping https ssh snmp
        set description "NMS management access"
        set alias "NMS_mgmt"
    next
    edit "uplink_1"
        set vdom "root"
        set ip 10.1.0.1 255.255.255.252
        set description "bgp to upstream FW"
    next
	
forti-fw-01 (Corporate) # get system arp 
Address           Age(min)   Hardware Addr      Interface
1.1.1.10          0          22:31:5e:00:34:d1  vms_vlan
10.0.0.10         0          22:31:5e:00:34:c2  NMS_mgmt
10.0.0.31         0          22:31:5e:00:34:31  NMS_mgmt
	""",
	"""
forti-fw-02 (Corporate) # get system config 
config system interface
    edit "fw_1"
        set vdom "root"
        set ip 10.1.0.2 255.255.255.252
        set description "bgp to forti-fw-01"
    next	
	"""]
	}
    config = {
        "add_arp": True
    }
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, **config)
    drawer.work(data)
    drawer.drawing.dump_file(filename="test_ip_drawing_yed_data_dict_fortigate.graphml", folder="./Output/")
    with open ("./Output/test_ip_drawing_yed_data_dict_fortigate.graphml") as produced:
        with open("./Output/should_be_test_ip_drawing_yed_data_dict_fortigate.graphml") as should_be:
            assert produced.read() == should_be.read()

# test_ip_drawing_yed_data_dict_fortigate()
	