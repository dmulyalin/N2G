import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir
from N2G import yed_diagram as create_yed_diagram
from utils_tests import normalize_xml

def test_1_add_elements_one_by_one():
    ###########################################
    # Test adding elements one by one
    ###########################################
    with open("./Output/should_be_yed.test_1_add_elements.graphml", "r") as f:
        expected_output = f.read()
    yed_diagram = create_yed_diagram()
    yed_diagram.add_node('a', top_label = 'top', bottom_label = 'bot')
    yed_diagram.add_node('b', label = 'somelabel', top_label = 'top', bottom_label = 'bot')
    yed_diagram.add_link('a', 'b', label = 'DF', src_label = 'Gi0/1', trgt_label = 'Fas1/2')
    yed_diagram.add_node('XR12', pic = 'router_3.svg')
    yed_diagram.add_node('XR13', pic = 'router_2.svg')
    yed_diagram.add_node('XR14', pic = 'router_1')
    yed_diagram.add_link('XR12', 'a', description = """
vlans_trunked: 1,22,33,44,55
state: up
""")
    yed_diagram.add_link('XR14', 'XR12')
    yed_diagram.add_link('a', 'XR13', label = 'LLDP', src_label = 'Gi0/21', trgt_label = 'Fas1/22')
    yed_diagram.layout()
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output)
    
def test_2_from_dict():
    ###########################################
    # Test from dict method
    ###########################################
    with open("./Output/should_be_yed.test_2_from_dict.graphml", "r") as f:
        expected_output = f.read()    
    yed_diagram = create_yed_diagram()
    sample_graph={
    'nodes': [
    {'id': 'a', 'pic': 'router_2', 'label': 'R1' }, 
    {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
    {'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
    {'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'},
    {'id': 'e', 'pic': 'router_1', 'label': 'R1' }], 
    'edges': [
    {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
    {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
    {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
    {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'}
    ]}
    yed_diagram.from_dict(sample_graph)
    yed_diagram.layout()
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output)
    
def test_3_graph_compare():
    ###########################################
    # Test graph compare
    ###########################################  
    with open("./Output/should_be_yed.test_3_graph_compare.graphml", "r") as f:
        expected_output = f.read()  
    yed_diagram = create_yed_diagram()
    compare_graph = {
    'nodes': [
        {'id': 'a', 'pic': 'router_round', 'label': 'R1' }, 
        {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
        {'id': 'f', 'bottom_label':'new_node', 'top_label':'new_node_f'},
        {'id': 'e', 'pic': 'router_angles', 'label': 'R1' }], 
    'edges': [
        {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
        {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
        {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
        {'source': 'e', 'src_label': 'Gig0/11', 'label': 'ed', 'target': 'b', 'trgt_label': 'Gig0/8'},
        {'source': 'f', 'src_label': 'Gig0/21', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/18'}
    ]}
    yed_diagram.from_file("./Data/test_load.graphml")
    yed_diagram.compare(compare_graph)
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output)
    
def test_4_dups_handling():
    ###########################################
    # Test graph compare
    ###########################################  
    with open("./Output/should_be_yed.test_4_dups_handling.graphml", "r") as f:
        expected_output = f.read()  
    sample_graph={
    'nodes': [
        {'id': 'a', 'pic': 'router_1', 'label': 'R1' }, 
        {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
        {'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
        {'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'},
        {'id': 'e', 'pic': 'router_2', 'label': 'R1' }], 
    'edges': [
        {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
        {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
        {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
        {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'} # new link
    ]}
    yed_diagram = create_yed_diagram()
    yed_diagram.from_file("./Data/test_load.graphml")
    yed_diagram.add_node(id = 'e', label = 'R101', top_label = 'top', bottom_label = 'bot', description='some node description') 
    yed_diagram.add_link('e', 'c', label="some blabla") # new link
    yed_diagram.add_link('a', 'd')
    yed_diagram.from_dict(sample_graph)
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output)
    
def test_5_delete_nodes():
    ###########################################
    # Test delete_node method
    ###########################################  
    with open("./Output/should_be_yed.test_5_delete_nodes.graphml", "r") as f:
        expected_output = f.read() 
    yed_diagram = create_yed_diagram()
    yed_diagram.from_file("./Data/test_load.graphml")
    yed_diagram.add_node(id="bb")
    yed_diagram.add_node(id="cc")
    yed_diagram.delete_node(id="e", ids=["a", "cc"])
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output)   
  
def test_6_delete_links():  
    ###########################################
    # Test delete_link method
    ###########################################
    with open("./Output/should_be_yed.test_6_delete_links.graphml", "r") as f:
        expected_output = f.read() 
    yed_diagram = create_yed_diagram()
    yed_diagram.from_file("./Data/test_load.graphml")
    yed_diagram.add_node(id="bb")
    yed_diagram.add_node(id="cc")
    yed_diagram.add_node(id="dd")
    yed_diagram.add_link('bb', 'cc')
    yed_diagram.add_link('cc', 'dd')
    yed_diagram.delete_link(id="e0", ids=["e1", "e2"])  
    yed_diagram.delete_link(source="cc", target="dd")
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output) 
 
def test_7_from_list_and_update_and_dups():   
    ###########################################
    # Test graph load from list and 
    # edge update method and node_duplicates update 
    # behavior
    ###########################################
    with open("./Output/should_be_yed.test_7_from_list_and_update_and_dups.graphml", "r") as f:
        expected_output = f.read() 
    yed_diagram = create_yed_diagram()
    sample_list_graph = [
    {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'},
    {'source': {'id':'b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
    {'source': {'id':'b', 'bottom_label': 'node_b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'e', 'trgt_label': 'Gig0/2'}
    ]
    yed_diagram.node_duplicates="update"
    yed_diagram.from_list(sample_list_graph)
    new_edges={
        "LineStyle": {"color": "#00FF00", "width": "1.0"},
        "EdgeLabel": {"textColor": "#00FF00"},
    }
    yed_diagram.update_link(
        label="Copper", src_label="Gig0/0", trgt_label="Gig0/2", source="b", target="c", 
        new_label="UTP", new_src_label="Gi0/0", new_trgt_label="Gi0/3", 
        description="some additional data", attributes=new_edges
    )
    yed_diagram.update_node(
        id="a", width=300, height=300, top_label="top llbl"
    )
    yed_diagram.update_node(
        id="b", width=200, height=150, top_label="top llbl2"
    )
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output) 
    
def test8_test_from_csv():
    ###########################################
    # Test graph load from csv 
    ###########################################
    with open("./Output/should_be_yed.test8_test_from_csv.graphml", "r") as f:
        expected_output = f.read() 
    yed_diagram = create_yed_diagram()
    csv_links_data = """"source","src_label","label","target","trgt_label","description"
"a","Gig0/0\nUP","DF","b","Gig0/1","vlans_trunked: 1,2,3\nstate: up"
"b","Gig0/0","Copper","c","Gig0/2",
"b","Gig0/0","Copper","e","Gig0/2",
d,Gig0/21,FW,e,Gig0/23,
"""
    csv_nodes_data=""""id","pic","label","bottom_label","top_label","description"
a,router_1,"R1,2",,,
"b",,,"some","top_some",
"c",,"somelabel","botlabel","toplabel","some node description"
"d","firewall.svg","somelabel1",,,"some node description"
"e","router_2","R1",,,
"""
    yed_diagram.from_csv(csv_nodes_data)
    yed_diagram.from_csv(csv_links_data)
    yed_diagram.layout()
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output) 
    
def test9_test_from_list_with_update():
    """
    Test that data2 will update switch-1 with top label
    """
    with open("./Output/should_be_yed.test9_test_from_list_with_update.graphml", "r") as f:
        expected_output = f.read() 
    yed_diagram = create_yed_diagram(node_duplicates="update")
    data1 = [
                {
                    "source": "switch-1",
                    "src_label": "GigabitEthernet4/6",
                    "target": {
                        "bottom_label": "",
                        "id": "switch-2",
                        "top_label": "10.13.1.7"
                    },
                    "trgt_label": "GigabitEthernet1/5"
                },
                {
                    "source": "switch-1",
                    "src_label": "GigabitEthernet1/1",
                    "target": {
                        "bottom_label": "",
                        "id": "switch-3",
                        "top_label": "10.17.14.1"
                    },
                    "trgt_label": "GigabitEthernet0/1"
                },
                {
                    "source": "switch-1",
                    "src_label": "GigabitEthernet1/2",
                    "target": {
                        "bottom_label": "",
                        "id": "switch-4",
                        "top_label": "10.17.14.2"
                    },
                    "trgt_label": "GigabitEthernet0/10"
                }
            ]
    data2 = [
                {
                    "source": "switch-2",
                    "src_label": "GigabitEthernet1/5",
                    "target": {
                        "bottom_label": "",
                        "id": "switch-1",
                        "top_label": "10.13.1.17"
                    },
                    "trgt_label": "GigabitEthernet4/6"
                }
            ]
    yed_diagram.from_list(data1)
    yed_diagram.from_list(data2)
    ret = yed_diagram.dump_xml()
    assert normalize_xml(ret) == normalize_xml(expected_output) 
    
def test_10_test_explicit_link_id():
    yed_diagram = create_yed_diagram()
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"}
        ],
        "links": [
            {
                "source": "node-1", 
                "target": "node-2", 
                "link_id": 1
            },
            {
                "source": "node-2", 
                "target": "node-1", 
                "link_id": 2
            }
        ]
    }    
    yed_diagram.from_dict(data)
    yed_diagram.dump_file(filename="yed.test_10_test_explicit_link_id.graphml", folder="./Output/")
    with open ("./Output/yed.test_10_test_explicit_link_id.graphml") as produced:
        with open("./Output/should_be_yed.test_10_test_explicit_link_id.graphml") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
    
    
# test_10_test_explicit_link_id()