from argparse import ArgumentParser as argparse_ArgumentParser
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram

#form arg parser menu:
argparser = argparse_ArgumentParser(description="Need to Graph CLI script.")
argparser.add_argument('-v', action='store_true', dest='SHVER', default=False, help='Show version')

#extract argparser arguments:
args = argparser.parse_args()
SHVER=args.SHVER   #boolean, if present print version and script info to the screen
if SHVER:
    raise SystemExit("""Version : 0.0
Python  : 3.x
OS      : Windows 7/10
Release : 03/03/2019

Features:

v0.0 xx/xx/xx
- ...
    """)
    
"""sample usage yed"""
###########################################
# Test adding elements one by one
###########################################
# yed_diagram = create_yed_diagram()
# yed_diagram.add_node('a', top_label = 'top', bottom_label = 'bot')
# yed_diagram.add_node('b', label = 'somelabel', top_label = 'top', bottom_label = 'bot')
# yed_diagram.add_link('a', 'b', label = 'DF', src_label = 'Gi0/1', trgt_label = 'Fas1/2')
# yed_diagram.add_node('XR12', pic = 'router.svg')
# yed_diagram.add_node('XR13', pic = 'router.svg')
# yed_diagram.add_node('XR14', pic = 'router')
# yed_diagram.add_link('XR12', 'a', description = """
# vlans_trunked: 1,22,33,44,55
# state: up
# """)
# yed_diagram.add_link('XR14', 'XR12')
# yed_diagram.dump_file()

###########################################
# Test from dict method
###########################################
# yed_diagram = create_yed_diagram()
# sample_graph={
# 'nodes': [
# {'id': 'a', 'pic': 'router_round', 'label': 'R1' }, 
# {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
# {'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
# {'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'},
# {'id': 'e', 'pic': 'router_angles', 'label': 'R1' }], 
# 'edges': [
# {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
# {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
# {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
# {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'}
# ]}
# yed_diagram.from_dict(sample_graph)
# yed_diagram.dump_file()

###########################################
# Test from dict with layout
###########################################
# yed_diagram = create_yed_diagram()
# sample_graph={
# 'nodes': [
# {'id': 'a', 'pic': 'router_round', 'label': 'R1' }, 
# {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
# {'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
# {'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'},
# {'id': 'e', 'pic': 'router_angles', 'label': 'R1' }], 
# 'edges': [
# {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
# {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
# {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
# {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'}
# ]}
# yed_diagram.from_dict(sample_graph)
# yed_diagram.layout(algo="kk")
# yed_diagram.dump_file()

###########################################
# Test graph compare
###########################################
# yed_diagram = create_yed_diagram()
# compare_graph = {
# 'nodes': [
# {'id': 'a', 'pic': 'router_round', 'label': 'R1' }, 
# {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
# {'id': 'e', 'pic': 'router_angles', 'label': 'R1' }], 
# 'edges': [
# {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
# {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
# {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
# # {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'},
# {'source': 'e', 'src_label': 'Gig0/11', 'label': 'ed', 'target': 'c', 'trgt_label': 'Gig0/8'}
# ]}
# yed_diagram.from_file("./Output/test_load.graphml")
# yed_diagram.compare(compare_graph)
# yed_diagram.dump_file()

###########################################
# Test graph load from file with adding 
# new and overlapping element
###########################################
# sample_graph={
# 'nodes': [
# {'id': 'a', 'pic': 'router_round', 'label': 'R1' }, 
# {'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
# {'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
# {'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'},
# {'id': 'e', 'pic': 'router_angles', 'label': 'R1' }], 
# 'edges': [
# {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
# {'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
# {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
# {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'}
# ]}
# yed_diagram = create_yed_diagram()
# yed_diagram.from_file("./Output/test_load.graphml")
# yed_diagram.add_node(id = 'e', label = 'R101', top_label = 'top', bottom_label = 'bot', description='some node description')
# yed_diagram.add_link('e', 'c', label="some blabla")
# yed_diagram.add_link('a', 'd')
# yed_diagram.from_dict(sample_graph)
# yed_diagram.dump_file()

###########################################
# Test delete_node method
###########################################
yed_diagram = create_yed_diagram()
yed_diagram.from_file("./Output/test_load.graphml")
yed_diagram.delete_node("e", "a")
yed_diagram.dump_file()

###########################################
# Test graph load from list and 
# edge update method and node_dublicates update 
# behavior
###########################################
# yed_diagram = create_yed_diagram()
# sample_list_graph = [
# {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'},
# {'source': {'id':'b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
# {'source': {'id':'b', 'bottom_label': 'node_b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'e', 'trgt_label': 'Gig0/2'}
# ]
# yed_diagram.node_dublicates="update"
# yed_diagram.from_list(sample_list_graph)
# new_edges={
#     # dict, attributes to apply to new edges
#     "LineStyle": {"color": "#00FF00", "width": "1.0"},
#     "EdgeLabel": {"textColor": "#00FF00"},
# }
# yed_diagram.update_link(
#     label="Copper", src_label="Gig0/0", trgt_label="Gig0/2", source="b", target="c", 
#     new_label="UTP", new_src_label="Gi0/0", new_trgt_label="Gi0/3", 
#     description="some additional data", attributes=new_edges
# )
# yed_diagram.update_node(
#     id="a", width=300, height=300, top_label="top llbl"
# )
# yed_diagram.update_node(
#     id="b", width=200, height=150, top_label="top llbl2"
# )
# yed_diagram.dump_file()

###########################################
# Test graph load from csv 
###########################################
# yed_diagram = create_yed_diagram()
# csv_links_data = """"source","src_label","label","target","trgt_label","description"
# "a","Gig0/0\nUP","DF","b","Gig0/1","vlans_trunked: 1,2,3\nstate: up"
# "b","Gig0/0","Copper","c","Gig0/2",
# "b","Gig0/0","Copper","e","Gig0/2",
# d,Gig0/21,FW,e,Gig0/23,
# """
# csv_nodes_data=""""id","pic","label","bottom_label","top_label","description"
# a,router_round,"R1,2",,,
# "b",,,"some","top_some",
# "c",,"somelabel","botlabel","toplabel","some node description"
# "d","firewall.svg","somelabel1",,,"some node description"
# "e","router_angles","R1",,,
# """
# yed_diagram.from_csv(csv_nodes_data)
# yed_diagram.from_csv(csv_links_data)
# yed_diagram.layout()
# yed_diagram.dump_file()


"""sample usage drawio"""
###########################################
# Test adding elements one by one
###########################################
# drawing = create_drawio_diagram()
# drawing.add_diagram("Page-1")
# drawing.add_node(id="node-1")
# drawing.add_node(id="node-2")
# drawing.add_node(id="node-3")
# drawing.add_node(id="node-4")
# drawing.add_node(id="node-5")
# drawing.add_node(id="node-2")
# drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
# drawing.add_link("node-1", "node-2", label="bla1")
# drawing.add_link("node-1", "node-3", label="bla2")
# drawing.add_link("node-3", "node-5", label="bla3")
# drawing.add_link("node-3", "node-4", label="bla4")
# drawing.add_link("node-33", "node-44", label="bla77")
# drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
# drawing.add_diagram("page_2", name="PAGE 2")
# drawing.add_node(id="node-25", url="Page-1")
# drawing.add_node(id="node-2", label="node-2 same id is on page 1")
# drawing.add_diagram("page_2")
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test from_dict method
###########################################
# drawing = create_drawio_diagram()
# data = {
#     "nodes": [
#         {"id": "node-1"},
#         {"id": "node-2"},
#         {"id": "node-3"},
#         {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
#     ],
#     "links": [
#         {"source": "node-1", "target": "node-2", "label": "bla1"},
#         {"source": "node-2", "target": "node-3", "label": "bla2"},
#         {"source": "node-3", "target": "node-1", "label": "bla3"},
#         {"source": "node-4", "target": "node-3", "label": "bla4"}
#     ]
# }
# drawing.from_dict(data, diagram_name="Page-1")
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test from_list method
###########################################
# drawing = create_drawio_diagram()
# data = [
#     {"source": {"id": "node-1"}, "target": "node-2", "label": "bla1"},
#     {"source": "node-2", "target": "node-3", "label": "bla2", "data": {"abc": 123}},
#     {"source": "node-3", "target": "node-1", "label": "bla3"},
#     {"source": {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}, "target": "node-3", "label": "bla4"}
# ]
# drawing.from_list(data, diagram_name="Page-1")
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test from_csv method
###########################################
# drawing = create_drawio_diagram()
# csv_links_data = """"source","label","target"
# "a","DF","b"
# "b","Copper","c"
# "b","Copper","e"
# d,FW,e
# """
# csv_nodes_data=""""id","label","style","width","height"
# a,"R1,2","./Pics/cisco_router.txt",78,53
# "b","some",,,
# "c","somelabel",,,
# "d","somelabel1",,,
# "e","R1",,,
# """
# drawing.from_csv(csv_nodes_data)
# drawing.from_csv(csv_links_data)
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test loading from file and dups handling
###########################################
# data = {
#     "nodes": [
#         {"id": "node-1"},
#         {"id": "node-2"},
#         {"id": "node-3"},
#         {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
#     ],
#     "links": [
#         {"source": "node-1", "target": "node-2", "label": "bla1"},
#         {"source": "node-2", "target": "node-3", "label": "bla2"},
#         {"source": "node-3", "target": "node-1", "label": "bla3"},
#         {"source": "node-4", "target": "node-3", "label": "bla4"}
#     ]
# }
# drawing = create_drawio_diagram()
# drawing.from_file("./Output/test_load.xml")
# drawing.from_dict(data, diagram_name="Page-1")
# drawing.add_node(id="node-55")
# drawing.add_link("node-55", "node-3")
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test nodes styles from drawio library
###########################################
# building_style="shape=mxgraph.cisco.buildings.generic_building;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
# drawing = create_drawio_diagram()
# drawing.from_file("./Output/test_load.xml")
# drawing.add_diagram("Page-1")
# drawing.add_node(id="Router-1", style="./Pics/cisco_router.txt", width=78, height=53)
# drawing.add_node(id="Router-2", style="./Pics/cisco_router.txt", width=78, height=53)
# drawing.add_node(id="Router-3", style="./Pics/cisco_router.txt", width=78, height=53)
# drawing.add_node(id="Switch-1", style="./Pics/cisco_l3_switch.txt", width=64, height=82)
# drawing.add_node(id="Building-1", style=building_style, width=90, height=136)
# drawing.add_link("Router-1", "Router-2")
# drawing.add_link("Router-1", "Router-3")
# drawing.add_link("Router-1", "node-2")
# drawing.add_link("Switch-1", "Router-3")
# drawing.add_link("Building-1", "Router-3")
# drawing.layout(algo="kk")
# drawing.dump_file()

###########################################
# Test node update
###########################################
# qsfp_router_style="shape=mxgraph.cisco.misc.asr_1000_series;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
# drawing = create_drawio_diagram()
# drawing.from_file("./Output/test_load.xml")
# drawing.update_node(id="node-2", label="node-2 Updated label")
# drawing.update_node(id="node-3", style=qsfp_router_style, width=88, height=86, label="node_qfp")
# drawing.update_node(id="node-1", data={"k1": "v1", "k2": "v2"}, url="http://ya.ru")
# drawing.dump_file()

###########################################
# Test link update
###########################################
# new_link_style="endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;endFill=0;strokeWidth=5;"
# drawing = create_drawio_diagram()
# drawing.from_file("./Output/test_load.xml")
# drawing.update_link(source="node-1", target="node-2", label="bla1", new_label="edge new label", style=new_link_style, data={"a": "b"}, url="http://ya.ru")
# drawing.update_link(source="node-1", target="node-3", label="bla3", style=new_link_style)
# drawing.update_link(source="node-1", target="node-3", label="bla24", style=new_link_style)
# drawing.dump_file()

###########################################
# Test compare method
###########################################
# existing_graph = {
#     "nodes": [
#         {"id": "node-1"},
#         {"id": "node-2"},
#         {"id": "node-3"},
#         {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"},
#         {"id": "node-55", "style": "./Pics/cisco_l3_switch.txt", "width": 64, "height": 82},
# ],
#     "links": [
#         {"source": "node-1", "target": "node-2", "label": "bla1"},
#         {"source": "node-2", "target": "node-3", "label": "bla2"},
#         {"source": "node-3", "target": "node-1", "label": "bla3"},
#         {"source": "node-4", "target": "node-3", "label": "bla4"},
#         {"source": "node-55", "target": "node-1", "label": "bla155"},        
#     ]
# }
# new_graph = {
#     "nodes": [
#         {"id": "node-99"},
#         {"id": "node-100", "style": "./Pics/cisco_router.txt", "width": 78, "height": 53},
#         {"id": "node-2"},
#         {"id": "node-3"},
#         {"id": "node-4", "data": {"a": "b", "c": "d"}, "url": "http://google.com"}
#     ],
#     "links": [
#         {"source": "node-2", "target": "node-3", "label": "bla2"},
#         {"source": "node-4", "target": "node-3", "label": "bla4"},
#         {"source": "node-99", "target": "node-3", "label": "bla99"},
#         {"source": "node-100", "target": "node-99", "label": "bla10099"},
#     ]
# }
# drawing = create_drawio_diagram()
# drawing.from_dict(data=existing_graph)
# drawing.compare(new_graph)
# drawing.layout(algo="kk")
# drawing.dump_file()