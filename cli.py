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
# Test graph load from list and 
# edge update method and node_dublicates update 
# behavior
###########################################
yed_diagram = create_yed_diagram()
sample_list_graph = [
{'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'},
{'source': {'id':'b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
{'source': {'id':'b', 'bottom_label': 'node_b'}, 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'e', 'trgt_label': 'Gig0/2'}
]
yed_diagram.node_dublicates="update"
yed_diagram.from_list(sample_list_graph)
new_edges={
    # dict, attributes to apply to new edges
    "LineStyle": {"color": "#00FF00", "width": "1.0"},
    "EdgeLabel": {"textColor": "#00FF00"},
}
yed_diagram.update_link(
    label="Copper", src_label="Gig0/0", trgt_label="Gig0/2", source="b", target="c", 
    new_label="UTP", new_src_label="Gi0/0", new_trgt_label="Gi0/3", 
    description="some additional data", attributes=new_edges
)
yed_diagram.dump_file()




"""sample usage drawio"""
# drawing = create_drawio_diagram()

# test adding one by one
## drawing.add_diagram("Page-1")
## drawing.add_node(id="node-1")
## drawing.add_node(id="node-2")
## drawing.add_node(id="node-3")
## drawing.add_node(id="node-4")
## drawing.add_node(id="node-5")
## drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
## drawing.add_link("node-1", "node-2", label="bla1")
## drawing.add_link("node-1", "node-3", label="bla2")
## drawing.add_link("node-3", "node-5", label="bla3")
## drawing.add_link("node-3", "node-4", label="bla4")
## drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
## drawing.add_diagram("page_2")
## drawing.add_node(id="node-25", url="Page-1")
## drawing.layout(algo="kk")
## drawing.dump_file()

# test from_dict
## data = {
##     "nodes": [
##         {"id": "node-1"},
##         {"id": "node-2"},
##         {"id": "node-3"},
##         {"id": "node-4", "data": {"a": "b", "c": "d"}, "link": "http://google.com"}
##     ],
##     "links": [
##         {"source": "node-1", "target": "node-2", "label": "bla1"},
##         {"source": "node-2", "target": "node-3", "label": "bla2"},
##         {"source": "node-3", "target": "node-1", "label": "bla3"},
##         {"source": "node-4", "target": "node-3", "label": "bla4"}
##     ]
## }
## drawing.from_dict(data, diagram_name="Page-1")
## drawing.layout(algo="kk")
## drawing.dump_file()

#test loading from file
## drawing.from_file("./Output/test_load.xml")
## drawing.add_node(id="node-55")
## drawing.add_link("node-55", "node-3")
## drawing.layout(algo="kk")
## drawing.dump_file()