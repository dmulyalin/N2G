yEd Module usage
================

yEd Module description goes here


Quick start
-----------

.. code-block:: 
        
    from N2G import yed_diagram as create_yed_diagram
	
    yed_diagram = create_yed_diagram()
    graph_data = [
        {
            'source': 'a', 
            'src_label': 'Gig0/0\nUP', 
            'label': 'DF', 
            'target': 'b', 
            'trgt_label': 'Gig0/1', 
            'description': 'vlans_trunked: 1,2,3\nstate: up'
        },
        {
            'source': 
                {
                    'id':'b', 
                    'bottom_label': 'node_b'
                }, 
            'src_label': 'Gig0/0', 
            'label': 'Copper', 
            'target': 'e', 
            'trgt_label': 'Gig0/2'}
    ]
    yed_diagram.from_list(graph_data)
    yed_diagram.layout(algo="kk")
    yed_diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")    
	
	
API reference
-------------------

API reference for N2G yEd module.

.. automodule:: N2G_yEd

.. autoclass:: yed_diagram
   :members: