from argparse import ArgumentParser as argparse_ArgumentParser
from N2G import drawio_diagram
from N2G import yed_diagram

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
yed_diagram = yed_diagram()
#graph1.addnode('a', top_label = 'top', bottom_label = 'bot')
#graph1.addnode('b', label = 'somelabel', top_label = 'top', bottom_label = 'bot')
#graph1.addedge('a', 'b', label = 'DF', src_label = 'Gi0/1', trgt_label = 'Fas1/2')
#graph1.addnode('XR12', pic = 'router.svg')
#graph1.addnode('XR14', pic = 'router')
#graph1.addedge('XR12', 'a', description = """
#vlans_trunked: 1,22,33,44,55
#state: up
#""")
#graph1.addedge('XR14', 'XR12')
##graph1.save(display = True)

sample_graph={
'nodes': [
{'id': 'a', 'pic': 'router', 'label': 'R1' }, 
{'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
{'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
{'id': 'd', 'pic':'firewall.svg', 'label': 'somelabel1', 'description': 'some node description'}], 
'edges': [
{'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
{'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
{'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
{'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'}
]}
yed_diagram.fromdict(sample_graph)
yed_diagram.save()

#compare_graph = {
#'nodes': [
#{'id': 'a', 'pic': 'router', 'label': 'R1' }, 
#{'id': 'b', 'bottom_label':'some', 'top_label':'top_some'}, 
#{'id': 'c', 'label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
#{'id': 'e', 'label': 'somelabel111'}], 
#'edges': [
#{'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}, 
#{'source': 'b', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
##{'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
#{'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'},
#{'source': 'e', 'src_label': 'Gig0/11', 'label': 'ed', 'target': 'c', 'trgt_label': 'Gig0/8'}
#]}

#graph3 = graph('./Data/garph_2.graphml')
#graph3.addnode(id = 'e', label = 'R101', top_label = 'top', bottom_label = 'bot', description='some node description')
#graph3.addedge('e', 'c')
#graph3.addedge('somelabel', 'somelabel1')
#graph3.fromdict(sample_graph, dublicates = 'skip')
#graph3.compare(compare_graph)
#graph3.save()
#print("graph3.ids_dict: ", graph3.ids_dict)
#print("graph3.nodes_dict: ", graph3.nodes_dict)
#print("graph3.edges_dict: ", graph3.edges_dict)

#graph1 = graph()
#graph1.addnode('a', top_label = 'top', bottom_label = 'bot', group = True, description = 'some description', url='123.com')
#graph1.addnode('a', top_label = 'top', bottom_label = 'bot', parent = 'a', description = 'some description', url='123.com')
#graph1.save(display = True)


"""sample usage drawio"""
# drawing = drawio_diagram()

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

# test fromdict
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