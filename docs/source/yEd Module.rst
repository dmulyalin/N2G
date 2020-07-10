yEd Module 
================

N2G yEd Module supports producing graphml XML structured text files that can be opened by yWorks yEd Graph editor.


Quick start
-----------

Nodes and links can be added one by one using ``add_node`` and ``add_link`` methods

.. code-block:: python 
        
    from N2G import yed_diagram
    
    diagram = yed_diagram()
    diagram.add_node('R1', top_label='Core', bottom_label='ASR1004')
    diagram.add_node('R2', top_label='Edge', bottom_label='MX240')
    diagram.add_link('R1', 'R2', label='DF', src_label='Gi0/1', trgt_label='ge-0/1/2')
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")    
    
After opening and editing diagram, it might look like this:

.. raw:: html
    :file: _images/quick_start_example.svg
    
Adding SVG nodes 
----------------

By default N2G uses shape nodes, but svg image can be sourced from directory on your system and used as node image instead. However, svg images as nodes can support only one label attribute, that label will be displayed above svg picture.

.. code-block:: python 
        
    from N2G import yed_diagram
    
    diagram = yed_diagram()
    diagram.add_node('R1', pic="router.svg", pic_path="./Pics/")
    diagram.add_node('R2', pic="router_edge.svg", pic_path="./Pics/")
    diagram.add_link('R1', 'R2', label='DF', src_label='Gi0/1', trgt_label='ge-0/1/2')
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")    
    
After opening and editing diagram, it might look like this:

.. image:: _images/svg_nodes_example.png    

Nodes and links data attributes
-------------------------------

Description and URL attributes can be added to node and link. Description attribute can be used by yEd to search for elements as well as diagrams exported in svg format can display data attributes as a tooltips.

.. code-block:: python 
        
    from N2G import yed_diagram
    
    diagram = yed_diagram()
    diagram.add_node('R1', top_label='Core', bottom_label='ASR1004', description="loopback0: 192.168.1.1", url="google.com")
    diagram.add_node('R2', top_label='Edge', bottom_label='MX240', description="loopback0: 192.168.1.2")
    diagram.add_link('R1', 'R2', label='DF', src_label='Gi0/1', trgt_label='ge-0/1/2', description="link media-type: 10G-LR", url="github.com")
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")
    
After opening and editing diagram, it might look like this:

.. raw:: html
    :file: _images/nodes_links_data_url.svg
    
Node R1 and link should be clickable on above image as they contain URL information, tooltip should be displayed if svg will be open on its own.

Loading graph from dictionary
-----------------------------

Diagram elements can be loaded from dictionary structure. That dictionary may contain nodes, links and edges keys, these keys should contain list of dictionaries where each dictionary item will contain elements attributes such as id, labels, description etc. 

.. code-block:: python 

    from N2G import yed_diagram
    
    diagram = yed_diagram()
    sample_graph={
    'nodes': [
        {'id': 'a', 'pic': 'router.svg', 'label': 'R1' }, 
        {'id': 'R2', 'bottom_label':'CE12800', 'top_label':'1.1.1.1'}, 
        {'id': 'c', 'label': 'R3', 'bottom_label':'FI', 'top_label':'fns751', 'description': 'role: access'},
        {'id': 'd', 'pic':'firewall.svg', 'label': 'FW1', 'description': 'location: US'},
        {'id': 'R4', 'pic': 'router'}
    ], 
    'links': [
        {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'R2', 'trgt_label': 'Gig0/1', 'description': 'role: uplink'}, 
        {'source': 'R2', 'src_label': 'Gig0/0', 'label': 'Copper', 'target': 'c', 'trgt_label': 'Gig0/2'},
        {'source': 'c', 'src_label': 'Gig0/0', 'label': 'ZR', 'target': 'a', 'trgt_label': 'Gig0/3'},
        {'source': 'd', 'src_label': 'Gig0/10', 'label': 'LR', 'target': 'c', 'trgt_label': 'Gig0/8'},
        {'source': 'd', 'src_label': 'Gig0/11', 'target': 'R4', 'trgt_label': 'Gig0/18'}
    ]}
    diagram.from_dict(sample_graph)
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")
    
After opening and editing diagram, it might look like this:

.. raw:: html
    :file: _images/from_dict_example.svg
        
Loading graph from csv
----------------------

Similar to from_dict method, from_csv method can take csv data with element details and add the to diagram. Two types of csv table should be provided - one for nodes, another for links.

.. code-block:: python 

    from N2G import yed_diagram
    
    diagram = yed_diagram()
    csv_links_data = """"source","src_label","label","target","trgt_label","description"
    "a","Gig0/0\\nUP","DF","R1","Gig0/1","vlans_trunked: 1,2,3\\nstate: up"
    "R1","Gig0/0","Copper","c","Gig0/2",
    "R1","Gig0/0","Copper","e","Gig0/2",
    d,Gig0/21,FW,e,Gig0/23,
    """
    csv_nodes_data=""""id","pic","label","bottom_label","top_label","description"
    a,router,"R12",,,
    "R1",,,"SGD1378","servers",
    "c",,"R3","SGE3412","servers","1.1.1.1"
    "d","firewall.svg","FW1",,,"2.2.2.2"
    "e","router","R11",,,
    """
    diagram.from_csv(csv_nodes_data)
    diagram.from_csv(csv_links_data)
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")

After opening and editing diagram, it might look like this:

.. raw:: html
    :file: _images/from_csv_example.svg
    
API reference
-------------------

API reference for N2G yEd module.

.. automodule:: N2G

.. autoclass:: yed_diagram
   :members: