import sys
import pprint
import json
import pytest

sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import v3d_diagramm as create_v3d_diagram
from N2G import json_data

sample_data = {
    'links': [{'data': {}, 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
              {'data': {}, 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
              {'data': {}, 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
              {'data': {}, 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
              {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
              {'data': {'cd': 123, 'ef': 456}, 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
    'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
              {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
              {'color': 'blue', 'data': {'val': 4}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
              {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
              {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
              {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8},
              {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
              {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
              {'color': 'green', 'data': {}, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]
}
                         
sample_data_list = [
    {'data': {}, 'label': 'bla1', 'source': {'id': 'node-1', 'nodeResolution': 16}, 'src_label': '', 'target': {'id': 'node-2'}, 'trgt_label': ''},
    {'data': {}, 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
    {'data': {}, 'label': 'bla3', 'source': {'id': 'node-3'}, 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
    {'data': {}, 'label': 'bla4', 'source': {'id': 'node-3', 'data': {'val': 4}}, 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
    {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
    {'data': {'cd': 123, 'ef': 456}, 'label': 'bla6', 'source': {'id': 'node-6', 'data': {'a': 'b', 'c': 'd'}}, 'src_label': '', 'target': 'node-1', 'trgt_label': ''}
]

def test_v3d_from_json_dict():
    sample_data_json = json.dumps(sample_data)
    v3d_drawing = create_v3d_diagram()
    json_data(v3d_drawing, sample_data_json)
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'blue', 'data': {'val': 4}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]}

# test_v3d_from_json_dict()

def test_v3d_from_json_list():
    sample_data_json = json.dumps(sample_data_list)
    v3d_drawing = create_v3d_diagram()
    json_data(v3d_drawing, sample_data_json)
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8}]}
           
# test_v3d_from_json_list()


def test_v3d_wrong_data():
    v3d_drawing = create_v3d_diagram()
    with pytest.raises(TypeError):
        json_data(v3d_drawing, data="1")    
           
# test_v3d_wrong_data()