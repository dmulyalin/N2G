import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram


def test_1_add_elements_one_by_one():
    ###########################################
    # Test adding elements one by one
    ###########################################
    with open("./drawio.test_1_add_elements_one_by_one.drawio", "r") as f:
        expected_output = f.read()
    drawing = create_drawio_diagram()
    drawing.add_diagram("Page-1")
    drawing.add_node(id="node-1")
    drawing.add_node(id="node-2")
    drawing.add_node(id="node-3")
    drawing.add_node(id="node-4")
    drawing.add_node(id="node-5")
    drawing.add_node(id="node-2")
    drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
    drawing.add_link("node-1", "node-2", label="bla1")
    drawing.add_link("node-1", "node-3", label="bla2")
    drawing.add_link("node-3", "node-5", label="bla3")
    drawing.add_link("node-3", "node-4", label="bla4")
    drawing.add_link("node-33", "node-44", label="bla77")
    drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
    drawing.add_diagram("page_2", name="PAGE 2")
    drawing.add_node(id="node-25", url="Page-1")
    drawing.add_node(id="node-2", label="node-2 same id is on page 1")
    drawing.add_diagram("page_2")
    drawing.layout(algo="kk")
    ret = drawing.dump_xml()
    assert ret == expected_output    
    
def test_2_from_dict():
    ###########################################
    # Test from_dict method
    ###########################################
    with open("./drawio.test_2_from_dict.drawio", "r") as f:
        expected_output = f.read()
    drawing = create_drawio_diagram()
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"},
            {"id": "node-3"},
            {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
        ],
        "links": [
            {"source": "node-1", "target": "node-2", "label": "bla1"},
            {"source": "node-2", "target": "node-3", "label": "bla2"},
            {"source": "node-3", "target": "node-1", "label": "bla3"},
            {"source": "node-4", "target": "node-3", "label": "bla4"}
        ]
    }
    drawing.from_dict(data, diagram_name="Page-1")
    drawing.layout(algo="kk")
    ret = drawing.dump_xml()
    assert ret == expected_output  
    
def test_3_from_list():
    ###########################################
    # Test from_list method
    ###########################################
    with open("./drawio.test_3_from_list.drawio", "r") as f:
        expected_output = f.read()
    drawing = create_drawio_diagram()
    data = [
        {"source": {"id": "node-1"}, "target": "node-2", "label": "bla1"},
        {"source": "node-2", "target": "node-3", "label": "bla2", "data": {"abc": 123}},
        {"source": "node-3", "target": "node-1", "label": "bla3"},
        {"source": {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}, "target": "node-3", "label": "bla4"}
    ]
    drawing.from_list(data, diagram_name="Page-1")
    drawing.layout(algo="kk")
    ret = drawing.dump_xml()
    assert ret == expected_output  
    
def test_4_from_csv():
    ###########################################
    # Test from_csv method
    ###########################################
    with open("./drawio.test_4_from_csv.drawio", "r") as f:
        expected_output = f.read()
    drawing = create_drawio_diagram()
    csv_links_data = """"source","label","target"
"a","DF","b"
"b","Copper","c"
"b","Copper","e"
d,FW,e
"""
    csv_nodes_data=""""id","label","style","width","height"
a,"R1,2","./Pics/cisco_router.txt",78,53
"b","some",,,
"c","somelabel",,,
"d","somelabel1",,,
"e","R1",,,
"""
    drawing.from_csv(csv_nodes_data)
    drawing.from_csv(csv_links_data)
    drawing.layout(algo="kk")
    ret = drawing.dump_xml()
    assert ret == expected_output      
    
def test_4_from_file_and_dups():
    ###########################################
    # Test loading from file and dups handling
    ###########################################
    with open("./drawio.test_4_from_file_and_dups.drawio", "r") as f:
        expected_output = f.read()  
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"},
            {"id": "node-3"},
            {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
        ],
        "links": [
            {"source": "node-1", "target": "node-2", "label": "bla1"},
            {"source": "node-2", "target": "node-3", "label": "bla2"},
            {"source": "node-3", "target": "node-1", "label": "bla3"},
            {"source": "node-4", "target": "node-3", "label": "bla4"}
        ]
    }
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.from_dict(data, diagram_name="Page-1")
    drawing.add_node(id="node-55")
    drawing.add_node(id="node-66") # new node
    drawing.add_link("node-55", "node-3") # new link
    drawing.add_link("node-55", "node-66") # new link
    drawing.layout(algo="kk")   
    ret = drawing.dump_xml()
    assert ret == expected_output  

def test_5_nodes_styles():
    ###########################################
    # Test nodes styles from drawio library
    ###########################################
    with open("./drawio.test_5_nodes_styles.drawio", "r") as f:
        expected_output = f.read()     
    building_style="shape=mxgraph.cisco.buildings.generic_building;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.add_diagram("Page-1")
    drawing.add_node(id="Router-1", style="./Pics/router_1.txt", width=78, height=53)
    drawing.add_node(id="Router-2", style="./Pics/router_1.txt", width=78, height=53)
    drawing.add_node(id="Router-3", style="./Pics/router_1.txt", width=78, height=53)
    drawing.add_node(id="Switch-1", style="./Pics/switch_l3.txt", width=64, height=82)
    drawing.add_node(id="Building-1", style=building_style, width=90, height=136)
    drawing.add_link("Router-1", "Router-2")
    drawing.add_link("Router-1", "Router-3")
    drawing.add_link("Router-1", "node-2")
    drawing.add_link("Switch-1", "Router-3")
    drawing.add_link("Building-1", "Router-3")
    drawing.layout(algo="kk")
    ret = drawing.dump_xml()
    assert ret == expected_output 
    
def test_6_node_update():    
    ###########################################
    # Test node update
    ###########################################
    with open("./drawio.test_6_node_update.drawio", "r") as f:
        expected_output = f.read()  
    qsfp_router_style="shape=mxgraph.cisco.misc.asr_1000_series;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.update_node(id="node-2", label="node-2 Updated label")
    drawing.update_node(id="node-3", style=qsfp_router_style, width=88, height=86, label="node_qfp")
    drawing.update_node(id="node-1", data={"k1": "v1", "k2": "v2"}, url="http://ya.ru")     
    ret = drawing.dump_xml()
    assert ret == expected_output   

def test_7_link_update():    
    ###########################################
    # Test link update
    ###########################################
    with open("./drawio.test_7_link_update.drawio", "r") as f:
        expected_output = f.read() 
    new_link_style="endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;endFill=0;strokeWidth=5;"
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.update_link(source="node-1", target="node-2", label="bla1", new_label="edge new label", style=new_link_style, data={"a": "b"}, url="http://ya.ru")
    drawing.update_link(source="node-1", target="node-3", label="bla3", style=new_link_style)
    ret = drawing.dump_xml()
    assert ret == expected_output  

def test_8_compare():    
    ###########################################
    # Test graphs compare method
    ###########################################
    with open("./drawio.test_8_compare.drawio", "r") as f:
        expected_output = f.read() 
    existing_graph = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"},
            {"id": "node-3"},
            {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"},
            {"id": "node-55", "style": "./Pics/switch_l3.txt", "width": 64, "height": 82},
    ],
        "links": [
            {"source": "node-1", "target": "node-2", "label": "bla1"},
            {"source": "node-2", "target": "node-3", "label": "bla2"},
            {"source": "node-3", "target": "node-1", "label": "bla3"},
            {"source": "node-4", "target": "node-3", "label": "bla4"},
            {"source": "node-55", "target": "node-1", "label": "bla155"},        
        ]
    }
    new_graph = {
        "nodes": [
            {"id": "node-99"},
            {"id": "node-100", "style": "./Pics/router_1.txt", "width": 78, "height": 53},
            {"id": "node-2"},
            {"id": "node-3"},
            {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
        ],
        "links": [
            {"source": "node-2", "target": "node-3", "label": "bla2"},
            {"source": "node-4", "target": "node-3", "label": "bla4"},
            {"source": "node-99", "target": "node-3", "label": "bla99"},
            {"source": "node-100", "target": "node-99", "label": "bla10099"},
        ]
    }
    drawing = create_drawio_diagram()
    drawing.from_dict(data=existing_graph)
    drawing.compare(new_graph)
    drawing.layout(algo="kk")    
    ret = drawing.dump_xml()
    assert ret == expected_output   

def test_9_node_delete():    
    ###########################################
    # Test node delte
    ###########################################
    with open("./drawio.test_9_node_delete.drawio", "r") as f:
        expected_output = f.read()     
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.delete_node(id="node-55", ids=["node-2"])
    ret = drawing.dump_xml()
    assert ret == expected_output 
    
def test_10_link_delete():    
    ###########################################
    # Test node delte
    ###########################################
    with open("./drawio.test_10_link_delete.drawio", "r") as f:
        expected_output = f.read()     
    drawing = create_drawio_diagram()
    drawing.from_file("./test_load.drawio")
    drawing.delete_link(id="3972a5fc4a57b84e0376216959d97b1c") # bla4 link
    drawing.delete_link(source="node-1", target="node-2", label="bla1")
    ret = drawing.dump_xml()
    assert ret == expected_output 