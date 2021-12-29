import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir
import pprint
import json

from N2G import v3d_diagramm as create_v3d_diagram

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
                         
def test_v3d_add_elements_one_by_one():
    ###########################################
    # Test adding elements one by one
    ###########################################
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1", nodeResolution=16, color="green")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3", color="blue", data={"val": 4})
    v3d_drawing.add_node(id="node-4")
    v3d_drawing.add_node(id="node-5")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    v3d_drawing.add_link("node-1", "node-3", label="bla2")
    v3d_drawing.add_link("node-3", "node-5", label="bla3")
    v3d_drawing.add_link("node-3", "node-4", label="bla4")
    v3d_drawing.add_link("node-33", "node-44", label="bla77")
    v3d_drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
    v3d_drawing.add_node(id="node-25")
    v3d_drawing.add_node(id="node-2", label="node-2 same id is on page 1")
    # v3d_drawing.run(port=9099)
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {},
            'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c',
            'label': 'bla1',
            'source': 'node-1',
            'src_label': '',
            'target': 'node-2',
            'trgt_label': ''},
           {'data': {},
            'id': '6b78b13fcfd7ba69c4c23a4daa1057a3',
            'label': 'bla2',
            'source': 'node-1',
            'src_label': '',
            'target': 'node-3',
            'trgt_label': ''},
           {'data': {},
            'id': '7ddc80c768882b8121f24382f55971d2',
            'label': 'bla3',
            'source': 'node-3',
            'src_label': '',
            'target': 'node-5',
            'trgt_label': ''},
           {'data': {},
            'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc',
            'label': 'bla4',
            'source': 'node-3',
            'src_label': '',
            'target': 'node-4',
            'trgt_label': ''},
           {'data': {},
            'id': '7975fd6bf9d010bd5226c4dac6e20e64',
            'label': 'bla77',
            'source': 'node-33',
            'src_label': '',
            'target': 'node-44',
            'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456},
            'id': 'b2bd8ff3afbb6b786a0607bcef755f42',
            'label': 'bla6',
            'source': 'node-6',
            'src_label': '',
            'target': 'node-1',
            'trgt_label': ''}],
 'nodes': [{'color': 'green',
            'data': {},
            'id': 'node-1',
            'label': 'node-1',
            'nodeResolution': 16},
           {'color': 'green',
            'data': {},
            'id': 'node-2',
            'label': 'node-2',
            'nodeResolution': 8},
           {'color': 'blue',
            'data': {'val': 4},
            'id': 'node-3',
            'label': 'node-3',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {},
            'id': 'node-4',
            'label': 'node-4',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {},
            'id': 'node-5',
            'label': 'node-5',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {'a': 'b', 'c': 'd'},
            'id': 'node-6',
            'label': 'node-6',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {},
            'id': 'node-33',
            'label': 'node-33',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {},
            'id': 'node-44',
            'label': 'node-44',
            'nodeResolution': 8},
           {'color': 'green',
            'data': {},
            'id': 'node-25',
            'label': 'node-25',
            'nodeResolution': 8}]}
    
# test_v3d_add_elements_one_by_one()

def test_v3d_from_dict():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_dict(sample_data)
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
           
# test_v3d_from_dict()

def test_v3d_dups_handling():
    v3d_drawing = create_v3d_diagram()
    data_with_dups = dict(sample_data)
    data_with_dups["nodes"].extend(
        [
            {'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 567},
            {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 123},
            {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 11},
        ]
    )
    data_with_dups["links"].extend(
        [
            {'data': {}, 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
            {'data': {}, 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
            {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
        ]
    )
    # pprint.pprint(data_with_dups, width=200)
    v3d_drawing.from_dict(data_with_dups)
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
           
# test_v3d_dups_handling()


def test_v3d_delete_nodes():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1", nodeResolution=16, color="green")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3", color="blue", data={"val": 4})
    v3d_drawing.add_node(id="node-4")
    v3d_drawing.add_node(id="node-5")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    v3d_drawing.add_link("node-1", "node-3", label="bla2")
    v3d_drawing.add_link("node-3", "node-5", label="bla3")
    v3d_drawing.add_link("node-3", "node-4", label="bla4")
    v3d_drawing.add_link("node-33", "node-44", label="bla77")
    v3d_drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
    v3d_drawing.add_node(id="node-25")
    v3d_drawing.add_node(id="node-2", label="node-2 same id is on page 1")
    # delete nodes
    v3d_drawing.delete_node(id="node-2")
    v3d_drawing.delete_node(id="node-6")
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
                                {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
                                {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
                                {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''}],
                      'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
                                {'color': 'blue', 'data': {'val': 4}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]}
                                
# test_v3d_delete_nodes()

def test_v3d_delete_links():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1", nodeResolution=16, color="green")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3", color="blue", data={"val": 4})
    v3d_drawing.add_node(id="node-4")
    v3d_drawing.add_node(id="node-5")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-6", data={"a": "b", "c": "d"}, url="http://google.com")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    v3d_drawing.add_link("node-1", "node-3", label="bla2")
    v3d_drawing.add_link("node-3", "node-5", label="bla3")
    v3d_drawing.add_link("node-3", "node-4", label="bla4")
    v3d_drawing.add_link("node-33", "node-44", label="bla77")
    v3d_drawing.add_link("node-6", "node-1", label="bla6", data={"cd": 123, "ef": 456})
    v3d_drawing.add_node(id="node-25")
    v3d_drawing.add_node(id="node-2", label="node-2 same id is on page 1")
    # delete links
    v3d_drawing.delete_link(id="no existing link id")
    v3d_drawing.delete_link(id="6b78b13fcfd7ba69c4c23a4daa1057a3")
    v3d_drawing.delete_link("node-33", "node-44", label="bla77")
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
                                {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
                                {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
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
           
# test_v3d_delete_links()

def test_v3d_update_node():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    # update node
    v3d_drawing.update_node(id="node-1", nodeResolution=16, color="green", data={"foo": "bar"})
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [],
                      'nodes': [
                          {'color': 'green', 'data': {'foo': 'bar'}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16}, 
                          {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8}]}
           
# test_v3d_update_node()


def test_v3d_update_link():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3")
    v3d_drawing.add_link("node-1", "node-2", label="link 1", data={'foo': 'bar'})    
    v3d_drawing.add_link("node-2", "node-3", label="link 2")
    v3d_drawing.add_link("node-3", "node-1", label="link 3")
    # result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    # update link 1 by id
    v3d_drawing.update_link(id="b976d190850cf080e04fbc635ff787c9", data={"foo": "barfoo"}, url="https://123.lab")
    # update link 2 by labels
    v3d_drawing.update_link("node-2", "node-3", label="link 2", new_label="link 2 new label", new_src_label="Eth1", data={1:2})
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {'foo': 'barfoo'},
                                 'id': 'b976d190850cf080e04fbc635ff787c9',
                                 'label': 'link 1',
                                 'source': 'node-1',
                                 'src_label': '',
                                 'target': 'node-2',
                                 'trgt_label': '',
                                 'url': 'https://123.lab'},
                                {'data': {1: 2}, 'id': 'd3e5c2b0871cdd336734df495c88b103', 'label': 'link 2 new label', 'source': 'node-2', 'src_label': 'Eth1', 'target': 'node-3', 'trgt_label': ''},
                                {'data': {}, 'id': '5fffb982d2b1d2be48ad17ad28fd944b', 'label': 'link 3', 'source': 'node-3', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
                      'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8}]}
# test_v3d_update_link()

def test_v3d_update_non_exist_node():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    # update node
    v3d_drawing.update_node(id="node-111", nodeResolution=16, color="green", data={"foo": "bar"})
    result = v3d_drawing.dump_dict()
    pprint.pprint(result, width=200)
    assert result == {'links': [], 
                      'nodes': [
                        {'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 8}, 
                        {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8}]}
                          
# test_v3d_update_non_exist_node()

def test_v3d_update_non_exist_link():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3")
    v3d_drawing.add_link("node-1", "node-2", label="link 1", data={'foo': 'bar'})    
    v3d_drawing.add_link("node-2", "node-3", label="link 2")
    v3d_drawing.add_link("node-3", "node-1", label="link 3")
    # update by id non existing link
    v3d_drawing.update_link(id="non existing id", data={"foo": "barfoo"}, url="https://123.lab")
    # update non existing link by labels
    v3d_drawing.update_link("node-22", "node-33", label="link 22", new_label="link 2 new label", new_src_label="Eth1", data={1:2})    
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {'foo': 'bar'}, 'id': 'b976d190850cf080e04fbc635ff787c9', 'label': 'link 1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
                                {'data': {}, 'id': '3569635b08a26eb33179ed54bbe2e381', 'label': 'link 2', 'source': 'node-2', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
                                {'data': {}, 'id': '5fffb982d2b1d2be48ad17ad28fd944b', 'label': 'link 3', 'source': 'node-3', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
                      'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8}]}
           
# test_v3d_update_non_exist_link()

def test_v3d_from_list():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_list(sample_data_list)
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
           
test_v3d_from_list()

def test_v3d_from_list_with_links_dups_skip():
    sample_data_list_with_dups = list(sample_data_list)
    sample_data_list_with_dups.extend([
        {'data': {}, 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': '', 'data': {'foo': 'bar'}},
        {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': '', 'url': 'http://123.lab'}
    ])
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_list(sample_data_list_with_dups)
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
           
# test_v3d_from_list_with_links_dups_skip()

def test_v3d_from_list_with_links_dups_update():
    sample_data_list_with_dups = list(sample_data_list)
    sample_data_list_with_dups.extend([
        {'data': {}, 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': '', 'data': {'foo': 'bar'}},
        {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': '', 'url': 'http://123.lab'}
    ])
    v3d_drawing = create_v3d_diagram(link_duplicates="update")
    v3d_drawing.from_list(sample_data_list_with_dups)
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {'foo': 'bar'}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': '', 'url': 'http://123.lab'},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8}]}
    
# test_v3d_from_list_with_links_dups_update()

def test_v3d_from_list_with_node_dups_update():
    v3d_drawing = create_v3d_diagram(node_duplicates="update")
    v3d_drawing.from_list(sample_data_list)
    result = v3d_drawing.dump_dict()
    pprint.pprint(result, width=200)
    # node-3 should have data updated as per later entry in sample_data_list
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'green', 'data': {'val': 4}, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8}]}
    
# test_v3d_from_list_with_node_dups_update()

def test_v3d_test_add_link_with_explicit_link_id():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_link("node-1", "node-2", label="bla1", id='link-1-id')
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [
        {'data': {}, 'id': 'link-1-id', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
        {'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''}],
    'nodes': [
        {'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 8}, 
        {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8}]}
 
# test_v3d_test_add_link_with_explicit_link_id()
    
def test_v3d_dump_dict():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [
        {'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''}],
    'nodes': [
        {'color': 'green', 'data': {}, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 8}, 
        {'color': 'green', 'data': {}, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8}]}

# test_v3d_dump_dict()

def test_v3d_dump_json():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    result = v3d_drawing.dump_json()
    # print(result)
    assert result == '{"nodes": [{"id": "node-1", "label": "node-1", "color": "green", "nodeResolution": 8, "data": {}}, {"id": "node-2", "label": "node-2", "color": "green", "nodeResolution": 8, "data": {}}], "links": [{"id": "b35ebf8a6eeb7084dd9f3e14ec85eb9c", "label": "bla1", "source": "node-1", "target": "node-2", "src_label": "", "trgt_label": "", "data": {}}]}'

# test_v3d_dump_json()

def test_v3d_dump_file():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_link("node-1", "node-2", label="bla1")
    v3d_drawing.dump_file(filename="test_v3d_dump_file.json")
    with open("./Output/test_v3d_dump_file.json") as f:
        assert f.read() == """{
    "links": [
        {
            "data": {},
            "id": "b35ebf8a6eeb7084dd9f3e14ec85eb9c",
            "label": "bla1",
            "source": "node-1",
            "src_label": "",
            "target": "node-2",
            "trgt_label": ""
        }
    ],
    "nodes": [
        {
            "color": "green",
            "data": {},
            "id": "node-1",
            "label": "node-1",
            "nodeResolution": 8
        },
        {
            "color": "green",
            "data": {},
            "id": "node-2",
            "label": "node-2",
            "nodeResolution": 8
        }
    ]
}"""

# test_v3d_dump_file()

def test_v3d_from_json():
    sample_data_json = json.dumps(sample_data)
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_json(sample_data_json)
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

# test_v3d_from_json()

def test_v3d_layout_3d_algo():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_dict(sample_data)
    v3d_drawing.layout(algo='kk3d')
    # v3d_drawing.run()
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
                                {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
                                {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
                                {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
                                {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
                                {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
                      'nodes': [{'color': 'green', 'data': {}, 'fx': 52, 'fy': 69, 'fz': 21, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
                                {'color': 'green', 'data': {}, 'fx': 29, 'fy': 94, 'fz': 31, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
                                {'color': 'blue', 'data': {'val': 4}, 'fx': 45, 'fy': 36, 'fz': 7, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'fx': 13, 'fy': 20, 'fz': 0, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'fx': 64, 'fy': 6, 'fz': 6, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
                                {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'fx': 80, 'fy': 82, 'fz': 38, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'fx': 4, 'fy': 13, 'fz': 88, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'fx': 10, 'fy': 41, 'fz': 100, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
                                {'color': 'green', 'data': {}, 'fx': 96, 'fy': 12, 'fz': 85, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]}
# test_v3d_layout_3d_algo()


def test_v3d_layout_2d_algo():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_dict(sample_data)
    v3d_drawing.layout(algo='kk')
    # v3d_drawing.run()
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'fx': 24, 'fy': 53, 'fz': 0, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'fx': 28, 'fy': 27, 'fz': 0, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'blue', 'data': {'val': 4}, 'fx': 36, 'fy': 77, 'fz': 0, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 59, 'fy': 91, 'fz': 0, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 26, 'fy': 99, 'fz': 0, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'fx': 0, 'fy': 47, 'fz': 0, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 96, 'fy': 40, 'fz': 0, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 100, 'fy': 63, 'fz': 0, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 63, 'fy': 1, 'fz': 0, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]}
           
# test_v3d_layout_2d_algo()

def test_v3d_layout_3d_algo_custom_diemnsion_size():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_dict(sample_data)
    v3d_drawing.layout(algo='kk3d', dx=200, dy=200, dz=200)
    # v3d_drawing.run()
    result = v3d_drawing.dump_dict()
    # pprint.pprint(result, width=200)
    assert result == {'links': [{'data': {}, 'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c', 'label': 'bla1', 'source': 'node-1', 'src_label': '', 'target': 'node-2', 'trgt_label': ''},
           {'data': {}, 'id': '6b78b13fcfd7ba69c4c23a4daa1057a3', 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
           {'data': {}, 'id': '7ddc80c768882b8121f24382f55971d2', 'label': 'bla3', 'source': 'node-3', 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
           {'data': {}, 'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc', 'label': 'bla4', 'source': 'node-3', 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
           {'data': {}, 'id': '7975fd6bf9d010bd5226c4dac6e20e64', 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
           {'data': {'cd': 123, 'ef': 456}, 'id': 'b2bd8ff3afbb6b786a0607bcef755f42', 'label': 'bla6', 'source': 'node-6', 'src_label': '', 'target': 'node-1', 'trgt_label': ''}],
 'nodes': [{'color': 'green', 'data': {}, 'fx': 103, 'fy': 138, 'fz': 41, 'id': 'node-1', 'label': 'node-1', 'nodeResolution': 16},
           {'color': 'green', 'data': {}, 'fx': 58, 'fy': 188, 'fz': 62, 'id': 'node-2', 'label': 'node-2', 'nodeResolution': 8},
           {'color': 'blue', 'data': {'val': 4}, 'fx': 89, 'fy': 72, 'fz': 13, 'id': 'node-3', 'label': 'node-3', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 27, 'fy': 41, 'fz': 0, 'id': 'node-4', 'label': 'node-4', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 127, 'fy': 12, 'fz': 11, 'id': 'node-5', 'label': 'node-5', 'nodeResolution': 8},
           {'color': 'green', 'data': {'a': 'b', 'c': 'd'}, 'fx': 160, 'fy': 164, 'fz': 75, 'id': 'node-6', 'label': 'node-6', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 8, 'fy': 25, 'fz': 176, 'id': 'node-33', 'label': 'node-33', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 21, 'fy': 83, 'fz': 200, 'id': 'node-44', 'label': 'node-44', 'nodeResolution': 8},
           {'color': 'green', 'data': {}, 'fx': 192, 'fy': 24, 'fz': 169, 'id': 'node-25', 'label': 'node-25', 'nodeResolution': 8}]}

# test_v3d_layout_3d_algo_custom_diemnsion_size()

def test_v3d_run_dry_run():
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.from_dict(sample_data)
    result = v3d_drawing.run(dry_run=True)
    # pprint.pprint(result)
    assert result == {'ip': '0.0.0.0',
                      'message': 'would start flask development server using graph_browser app',
                      'port': 9000}
                      
# test_v3d_run_dry_run()
