import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from utils_tests import normalize_xml

def test_1_add_elements_one_by_one():
    ###########################################
    # Test adding elements one by one
    ###########################################
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.add_diagram("Page-1")
    drawio_drawing.add_node(id="node-1")
    drawio_drawing.add_node(id="node-2")
    drawio_drawing.add_node(id="node-3")
    drawio_drawing.add_node(id="node-4")
    drawio_drawing.add_node(id="node-5")
    drawio_drawing.add_node(id="node-2")
    drawio_drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
    drawio_drawing.add_link("node-1", "node-2", label="bla1")
    drawio_drawing.add_link("node-1", "node-3", label="bla2")
    drawio_drawing.add_link("node-3", "node-5", label="bla3")
    drawio_drawing.add_link("node-3", "node-4", label="bla4")
    drawio_drawing.add_link("node-33", "node-44", label="bla77")
    drawio_drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
    drawio_drawing.add_diagram("page_2", name="PAGE 2")
    drawio_drawing.add_node(id="node-25", url="Page-1")
    drawio_drawing.add_node(id="node-2", label="node-2 same id is on page 1")
    drawio_drawing.add_diagram("page_2")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_1_add_elements_one_by_one.drawio", folder="./Output/")
    with open ("./Output/test_1_add_elements_one_by_one.drawio") as produced:
        with open("./Output/should_be_test_1_add_elements_one_by_one.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())
    
# test_1_add_elements_one_by_one()
    
def test_2_from_dict():
    ###########################################
    # Test from_dict method
    ###########################################
    drawio_drawing = create_drawio_diagram()
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
    drawio_drawing.from_dict(data, diagram_name="Page-1")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_2_from_dict.drawio", folder="./Output/")
    with open ("./Output/test_2_from_dict.drawio") as produced:
        with open("./Output/should_be_test_2_from_dict.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
    
def test_3_from_list():
    ###########################################
    # Test from_list method
    ###########################################
    drawio_drawing = create_drawio_diagram()
    data = [
        {"source": {"id": "node-1"}, "target": "node-2", "label": "bla1"},
        {"source": "node-2", "target": "node-3", "label": "bla2", "data": {"abc": 123}},
        {"source": "node-3", "target": "node-1", "label": "bla3"},
        {"source": {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}, "target": "node-3", "label": "bla4"}
    ]
    drawio_drawing.from_list(data, diagram_name="Page-1")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_3_from_list.drawio", folder="./Output/")
    with open ("./Output/test_3_from_list.drawio") as produced:
        with open("./Output/should_be_test_3_from_list.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
    
def test_4_from_csv():
    ###########################################
    # Test from_csv method
    ###########################################
    drawio_drawing = create_drawio_diagram()
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
    drawio_drawing.from_csv(csv_nodes_data)
    drawio_drawing.from_csv(csv_links_data)
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_4_from_csv.drawio", folder="./Output/")  
    with open ("./Output/test_4_from_csv.drawio") as produced:
        with open("./Output/should_be_test_4_from_csv.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
    
def test_5_from_file_and_dups():
    ###########################################
    # Test loading from file and dups handling
    ###########################################
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
            {"source": "node-4", "target": "node-3", "label": "bla4"}        ]
    }
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.from_dict(data, diagram_name="Page-1")   
    drawio_drawing.add_node(id="node-55")
    drawio_drawing.add_node(id="node-66") # new node
    drawio_drawing.add_link("node-55", "node-3") # new link
    drawio_drawing.add_link("node-55", "node-66") # new link
    drawio_drawing.layout(algo="kk") 
    drawio_drawing.dump_file(filename="test_5_from_file_and_dups.drawio", folder="./Output/")  
    with open ("./Output/test_5_from_file_and_dups.drawio") as produced:
        with open("./Output/should_be_test_5_from_file_and_dups.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
            
def test_6_nodes_styles():
    ###########################################
    # Test nodes styles from drawio library
    ########################################### 
    building_style="shape=mxgraph.cisco.buildings.generic_building;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.add_diagram("Page-1")
    drawio_drawing.add_node(id="Router-1", style="./Pics/router_1.txt", width=78, height=53)
    drawio_drawing.add_node(id="Router-2", style="./Pics/router_1.txt", width=78, height=53)
    drawio_drawing.add_node(id="Router-3", style="./Pics/router_1.txt", width=78, height=53)
    drawio_drawing.add_node(id="Switch-1", style="./Pics/switch_l3.txt", width=64, height=82)
    drawio_drawing.add_node(id="Building-1", style=building_style, width=90, height=136)
    drawio_drawing.add_link("Router-1", "Router-2")
    drawio_drawing.add_link("Router-1", "Router-3")
    drawio_drawing.add_link("Router-1", "node-2")
    drawio_drawing.add_link("Switch-1", "Router-3")
    drawio_drawing.add_link("Building-1", "Router-3")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_6_nodes_styles.drawio", folder="./Output/") 
    with open ("./Output/test_6_nodes_styles.drawio") as produced:
        with open("./Output/should_be_test_6_nodes_styles.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
            
def test_7_node_update():    
    ###########################################
    # Test node update
    ###########################################
    qsfp_router_style="shape=mxgraph.cisco.misc.asr_1000_series;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.update_node(id="node-2", label="node-2 Updated label")
    drawio_drawing.update_node(id="node-3", style=qsfp_router_style, width=88, height=86, label="node_qfp")
    drawio_drawing.update_node(id="node-1", data={"k1": "v1", "k2": "v2"}, url="http://ya.ru")     
    drawio_drawing.dump_file(filename="test_7_node_update.drawio", folder="./Output/")   
    with open ("./Output/test_7_node_update.drawio") as produced:
        with open("./Output/should_be_test_7_node_update.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
            
def test_8_link_update():    
    ###########################################
    # Test link update
    ###########################################
    new_link_style="endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;endFill=0;strokeWidth=5;"
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.update_link(source="node-1", target="node-2", label="bla1", new_label="edge new label", style=new_link_style, data={"a": "b"}, url="http://ya.ru")
    drawio_drawing.update_link(source="node-1", target="node-3", label="bla3", style=new_link_style)
    drawio_drawing.dump_file(filename="test_8_link_update.drawio", folder="./Output/") 
    with open ("./Output/test_8_link_update.drawio") as produced:
        with open("./Output/should_be_test_8_link_update.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
            
def test_9_compare():    
    ###########################################
    # Test graphs compare method
    ###########################################
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
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_dict(data=existing_graph)
    drawio_drawing.compare(new_graph)
    drawio_drawing.layout(algo="kk")    
    drawio_drawing.dump_file(filename="test_9_compare.drawio", folder="./Output/") 
    with open ("./Output/test_9_compare.drawio") as produced:
        with open("./Output/should_be_test_9_compare.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())     

def test_10_node_delete():    
    ###########################################
    # Test node delte
    ###########################################
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.delete_node(id="node-55", ids=["node-2"])
    drawio_drawing.dump_file(filename="test_10_node_delete.drawio", folder="./Output/") 
    with open ("./Output/test_10_node_delete.drawio") as produced:
        with open("./Output/should_be_test_10_node_delete.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())   
            
def test_11_link_delete():    
    ###########################################
    # Test node delete
    ###########################################    
    drawio_drawing = create_drawio_diagram()
    drawio_drawing.from_file("./Data/test_load.drawio")
    drawio_drawing.delete_link(id="d5fa69cbdbc6ae606177e052dcdf4fdc") # bla4 link
    drawio_drawing.delete_link(source="node-1", target="node-2", label="bla1")
    drawio_drawing.dump_file(filename="test_11_link_delete.drawio", folder="./Output/") 
    with open ("./Output/test_11_link_delete.drawio") as produced:
        with open("./Output/should_be_test_11_link_delete.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())   
            
def test_12_add_link_labels():    
    ###########################################
    # Test link labels
    ###########################################    
    drawio_drawing = create_drawio_diagram()
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"},
            {"id": "node-3"}
        ],
        "links": [
            {"source": "node-1", "target": "node-2", "label": "bla1", "src_label": "Gi1/1", "trgt_label": "Gi2/29"},
            {"source": "node-2", "target": "node-3", "label": "bla2", "src_label": "Gi2/2", "trgt_label": "Gi2/17"},
            {"source": "node-3", "target": "node-1", "label": "bla3", "src_label": "Gi3/6", "trgt_label": "Gi5/21"}
        ]
    }
    drawio_drawing.from_dict(data, diagram_name="Page-1")
    drawio_drawing.dump_file(filename="test_12_add_link_labels.drawio", folder="./Output/")
    with open ("./Output/test_12_add_link_labels.drawio") as produced:
        with open("./Output/should_be_test_12_add_link_labels.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())   
            
def test_13_update_link_labels():    
    ###########################################
    # Test link labels update
    ###########################################    
    new_link_style="endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;endFill=0;strokeWidth=5;"
    new_src_trgt_style = "labelBackgroundColor=#ffffff;;labelBorderColor=#000000;fontColor=#FF66B3;fontStyle=1"
    drawio_drawing = create_drawio_diagram()
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"},
            {"id": "node-3"}
        ],
        "links": [
            {"source": "node-1", "target": "node-2", "label": "bla1", "src_label": "Gi1/1", "trgt_label": "Gi2/29"},
            {"source": "node-2", "target": "node-3"},
            {"source": "node-3", "target": "node-1", "src_label": "Gi3/6", "trgt_label": "Gi5/21"}
        ]
    }
    drawio_drawing.from_dict(data, diagram_name="Page-1")
    drawio_drawing.update_link(
        source="node-1", 
        target="node-2", 
        label="bla1",
        src_label="Gi1/1", 
        trgt_label="Gi2/29", 
        style=new_link_style, 
        data={"a": "b"}, 
        new_src_label="GigEth1/1",
        new_trgt_label="GigEth2/29",
        src_label_style=new_src_trgt_style,
        trgt_label_style=new_src_trgt_style
    )
    drawio_drawing.update_link(
        source="node-3", 
        target="node-1", 
        src_label="Gi3/6", 
        trgt_label="Gi5/21", 
        new_src_label="GE3/6",
        new_trgt_label="GE5/21"
    )
    drawio_drawing.update_link(
        source="node-2", 
        target="node-3", 
        new_src_label="Gi1/1",
        new_trgt_label="Gi2/29"
    )
    drawio_drawing.dump_file(filename="test_13_update_link_labels.drawio", folder="./Output/")
    with open ("./Output/test_13_update_link_labels.drawio") as produced:
        with open("./Output/should_be_test_13_update_link_labels.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 

# test_13_update_link_labels()


def test_14_test_explicit_link_id():
    drawio_drawing = create_drawio_diagram()
    data = {
        "nodes": [
            {"id": "node-1"},
            {"id": "node-2"}
        ],
        "links": [
            {
                "source": "node-1", 
                "target": "node-2", 
                "link_id": 1,
                'style': 'endArrow=classic;endFill=0;sourcePortConstraint=east;targetPortConstraint=west;edgeStyle=orthogonalEdgeStyle;'
            },
            {
                "source": "node-2", 
                "target": "node-1", 
                "link_id": 2,
                'style': 'endArrow=classic;endFill=0;sourcePortConstraint=east;targetPortConstraint=west;edgeStyle=orthogonalEdgeStyle;'
            }
        ]
    }    
    drawio_drawing.from_dict(data, diagram_name="Page-1")
    drawio_drawing.dump_file(filename="test_14_test_explicit_link_id.drawio", folder="./Output/")
    with open ("./Output/test_14_test_explicit_link_id.drawio") as produced:
        with open("./Output/should_be_test_14_test_explicit_link_id.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read()) 
    
# test_14_test_explicit_link_id()