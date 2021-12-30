"""
JSON Data Plugin
****************

JSON data plugin loads structured data from JSON string and inputs it into
diagram class - if JSON string produces list, uses ``from_list`` method, 
if JSON string produces dictionary uses ``from_dict`` method.

Sample Usage 
------------

Code to demonstrate how to use ``json_data`` plugin::

    from N2G import v3d_diagramm
    from N2G import json_data
    
    sample_json_data = '''{
        "links": [{"data": {}, "label": "bla1", "source": "node-1", "src_label": "", "target": "node-2", "trgt_label": ""},
                {"data": {}, "label": "bla2", "source": "node-1", "src_label": "", "target": "node-3", "trgt_label": ""},
                {"data": {}, "label": "bla3", "source": "node-3", "src_label": "", "target": "node-5", "trgt_label": ""},
                {"data": {}, "label": "bla4", "source": "node-3", "src_label": "", "target": "node-4", "trgt_label": ""},
                {"data": {}, "label": "bla77", "source": "node-33", "src_label": "", "target": "node-44", "trgt_label": ""},
                {"data": {"cd": 123, "ef": 456}, "label": "bla6", "source": "node-6", "src_label": "", "target": "node-1", "trgt_label": ""}],
        "nodes": [{"color": "green", "data": {}, "id": "node-1", "label": "node-1", "nodeResolution": 16},
                {"color": "green", "data": {}, "id": "node-2", "label": "node-2", "nodeResolution": 8},
                {"color": "blue", "data": {"val": 4}, "id": "node-3", "label": "node-3", "nodeResolution": 8},
                {"color": "green", "data": {}, "id": "node-4", "label": "node-4", "nodeResolution": 8},
                {"color": "green", "data": {}, "id": "node-5", "label": "node-5", "nodeResolution": 8},
                {"color": "green", "data": {"a": "b", "c": "d"}, "id": "node-6", "label": "node-6", "nodeResolution": 8},
                {"color": "green", "data": {}, "id": "node-33", "label": "node-33", "nodeResolution": 8},
                {"color": "green", "data": {}, "id": "node-44", "label": "node-44", "nodeResolution": 8},
                {"color": "green", "data": {}, "id": "node-25", "label": "node-25", "nodeResolution": 8}]
    }'''

    v3d_drawing = create_v3d_diagram()
    json_data(v3d_drawing, sample_json_data)
    v3d_drawing.dump_file()
    
API Reference
-------------

.. autofunction:: N2G.plugins.data.json_data.json_data
"""
import logging
import json

# initiate logging
log = logging.getLogger(__name__)


def json_data(drawing, data):
    """
    Function to load graph data from JSON text.
    
    :param drawing: (obj) class object of one of N2G diagram plugins
    :param data: (str) JSON string to load
    
    If JSON string produces list, uses ``frm_list`` method, if dictionary uses ``from_dict`` method
    """
    loaded_data = json.loads(data)

    if isinstance(loaded_data, list):
        drawing.from_list(data=loaded_data)
    elif isinstance(loaded_data, dict):
        drawing.from_dict(data=loaded_data)
    else:
        raise TypeError(
            "N2G:json_data JSON data should load into list or dictionary, not '{}'".format(
                type(loaded_data)
            )
        )
