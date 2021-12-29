import sys
sys.path.insert(0,'..')

import pprint

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import v3d_diagramm as create_v3d_diagram
from N2G import cli_ospf_data

mock_data_xr = {"Cisco_IOSXR": ["""
RP/0/RP0/CPU0:router-1#show ospf database router 

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 0.0.0.0)

  LS age: 406
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 8000010c
  Checksum: 0x24dd
  Length: 132
   Number of Links: 9

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 0.0.0.12
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 0.0.0.10
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.3
     (Link Data) Router Interface address: 0.0.0.11
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.3
     (Link Data) Router Interface address: 10.1.0.1
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.0
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 10.1.0.5
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.4
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.1
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1


  Routing Bit Set on this LSA
  LS age: 1604
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.2
  Advertising Router: 10.0.1.2
  LS Seq Number: 8000010b
  Checksum: 0xdc96
  Length: 132
   Number of Links: 9

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.3
     (Link Data) Router Interface address: 0.0.0.52
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 0.0.0.53
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 0.0.0.51
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 10.1.0.9
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.8
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 10.1.0.6
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.4
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.2
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.2
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1


  Routing Bit Set on this LSA
  LS age: 746
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.3
  Advertising Router: 10.0.1.3
  LS Seq Number: 80000107
  Checksum: 0x4838
  Length: 132
   Number of Links: 9

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 0.0.0.48
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 0.0.0.47
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 0.0.0.49
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 10.1.0.2
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.0
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 10.1.0.13
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.12
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.3
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.3
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1


  Routing Bit Set on this LSA
  LS age: 1425
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.4
  Advertising Router: 10.0.1.4
  LS Seq Number: 80000108
  Checksum: 0x8ae0
  Length: 132
   Number of Links: 9

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 0.0.0.47
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 0.0.0.48
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.3
     (Link Data) Router Interface address: 0.0.0.49
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 10.1.0.10
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.8
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.3
     (Link Data) Router Interface address: 10.1.0.14
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.0.12
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.4
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.4
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1
       
RP/0/RP0/CPU0:router-1#show ospf database summary 

            OSPF Router with ID (10.1.2.2) (Process ID 1)

                Summary Net Link States (Area 0.0.0.0)

  LS age: 1639
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.1
  LS Seq Number: 800030eb
  Checksum: 0x899d
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 2312 

  LS age: 427
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.2
  LS Seq Number: 800030eb
  Checksum: 0xad74
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1806 

  LS age: 1695
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.192
  LS Seq Number: 800030eb
  Checksum: 0xd081
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1312 

  Routing Bit Set on this LSA
  LS age: 581
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.193
  LS Seq Number: 800030eb
  Checksum: 0xf458
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 806 

                Summary Net Link States (Area 0.0.0.32)

  LS age: 1639
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.1
  LS Seq Number: 800030eb
  Checksum: 0x899d
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 2312 
        
RP/0/RSP0/CPU0:router-1#show ospf database external 

            OSPF Router with ID (10.3.22.75) (Process ID 1)

                Type-5 AS External Link States

  Routing Bit Set on this LSA
  LS age: 1009
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.0.1.2
  LS Seq Number: 80000519
  Checksum: 0x9009
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  LS age: 520
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.0.1.1
  LS Seq Number: 80001b96
  Checksum: 0x3279
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  Routing Bit Set on this LSA
  LS age: 90
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.0.0 (External Network Number)
  Advertising Router: 10.0.1.1
  LS Seq Number: 8003494f
  Checksum: 0x1d4d
  Length: 36
  Network Mask: /8
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 0.0.0.0
        External Route Tag: 0

  Routing Bit Set on this LSA
  LS age: 1251
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.2.0 (External Network Number)
  Advertising Router: 10.0.1.1
  LS Seq Number: 800079c3
  Checksum: 0x5d2e
  Length: 36
  Network Mask: /24
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 10.4.209.161
        External Route Tag: 0
    """]
}
    
def test_ospf_drawer_yed_data_dict_base():
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_ospf_data(drawing, **config)
    drawer.work(mock_data_xr)
    drawer.drawing.dump_file(filename="test_ospf_drawer_yed_data_dict_base.graphml", folder="./Output/")
    with open ("./Output/test_ospf_drawer_yed_data_dict_base.graphml") as produced:
        with open("./Output/should_be_test_ospf_drawer_yed_data_dict_base.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ospf_drawer_yed_data_dict_base()

def test_ospf_drawer_yed_data_dict_add_connected():
    drawing = create_yed_diagram()
    drawer = cli_ospf_data(drawing, add_connected=True)
    drawer.work(mock_data_xr)
    drawer.drawing.dump_file(filename="test_ospf_drawer_yed_data_dict_add_connected.graphml", folder="./Output/")
    with open ("./Output/test_ospf_drawer_yed_data_dict_add_connected.graphml") as produced:
        with open("./Output/should_be_test_ospf_drawer_yed_data_dict_add_connected.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ospf_drawer_yed_data_dict_add_connected()

def test_ospf_drawer_yed_data_dict_no_add_data():
    drawing = create_yed_diagram()
    drawer = cli_ospf_data(drawing, add_data=False)
    drawer.work(mock_data_xr)
    drawer.drawing.dump_file(filename="test_ospf_drawer_yed_data_dict_no_add_data.graphml", folder="./Output/")
    with open ("./Output/test_ospf_drawer_yed_data_dict_no_add_data.graphml") as produced:
        with open("./Output/should_be_test_ospf_drawer_yed_data_dict_no_add_data.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ospf_drawer_yed_data_dict_no_add_data()

def test_ospf_drawer_yed_cisco_ios_lsdb():
    with open("./Data/SAMPLE_CISCO_IOS_OSPFv2_LSDB/cisco_ios_show_ip_ospf_database_router_external_summary_IOL4_ABR.txt") as f:
        data = f.read()
    drawing = create_yed_diagram()
    drawer = cli_ospf_data(drawing)
    drawer.work({"Cisco_IOS": [data]})    
    drawer.drawing.dump_file(filename="test_ospf_drawer_yed_cisco_ios_lsdb.graphml", folder="./Output/")
    with open ("./Output/test_ospf_drawer_yed_cisco_ios_lsdb.graphml") as produced:
        with open("./Output/should_be_test_ospf_drawer_yed_cisco_ios_lsdb.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_ospf_drawer_yed_cisco_ios_lsdb()


def test_ospf_drawer_v3d_data_dict_base():
    drawing = create_v3d_diagram()
    drawer = cli_ospf_data(drawing)
    drawer.work(mock_data_xr)
    # drawer.drawing.run()
    result = drawer.drawing.dump_dict()
    # pprint.pprint(result)
    assert len(result["links"]) == 4
    assert len(result["nodes"]) == 4
    
# test_ospf_drawer_v3d_data_dict_base()