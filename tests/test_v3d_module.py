import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir
import pprint
from N2G import v3d_diagramm as create_v3d_diagram

def test_1_add_elements_one_by_one():
    ###########################################
    # Test adding elements one by one
    ###########################################
    v3d_drawing = create_v3d_diagram()
    v3d_drawing.add_node(id="node-1", nodeResolution=16, color="green")
    v3d_drawing.add_node(id="node-2")
    v3d_drawing.add_node(id="node-3", color="blue", val=4)
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
    # v3d_drawing.run()
    result = v3d_drawing.dump_dict()
    pprint.pprint(result)
    assert result == {'links': [{'id': 'b35ebf8a6eeb7084dd9f3e14ec85eb9c',
                                 'label': 'bla1',
                                 'source': 'node-1',
                                 'src_label': '',
                                 'target': 'node-2',
                                 'trgt_label': ''},
                                {'id': '6b78b13fcfd7ba69c4c23a4daa1057a3',
                                 'label': 'bla2',
                                 'source': 'node-1',
                                 'src_label': '',
                                 'target': 'node-3',
                                 'trgt_label': ''},
                                {'id': '7ddc80c768882b8121f24382f55971d2',
                                 'label': 'bla3',
                                 'source': 'node-3',
                                 'src_label': '',
                                 'target': 'node-5',
                                 'trgt_label': ''},
                                {'id': 'd5fa69cbdbc6ae606177e052dcdf4fdc',
                                 'label': 'bla4',
                                 'source': 'node-3',
                                 'src_label': '',
                                 'target': 'node-4',
                                 'trgt_label': ''},
                                {'id': '7975fd6bf9d010bd5226c4dac6e20e64',
                                 'label': 'bla77',
                                 'source': 'node-33',
                                 'src_label': '',
                                 'target': 'node-44',
                                 'trgt_label': ''},
                                {'id': 'b2bd8ff3afbb6b786a0607bcef755f42',
                                 'label': 'bla6',
                                 'source': 'node-6',
                                 'src_label': '',
                                 'target': 'node-1',
                                 'trgt_label': ''}],
                      'nodes': [{'id': 'node-1', 'label': 'node-1'},
                                {'id': 'node-2', 'label': 'node-2'},
                                {'id': 'node-3', 'label': 'node-3'},
                                {'id': 'node-4', 'label': 'node-4'},
                                {'id': 'node-5', 'label': 'node-5'},
                                {'id': 'node-6', 'label': 'node-6'},
                                {'id': 'node-33', 'label': 'node-33'},
                                {'id': 'node-44', 'label': 'node-44'},
                                {'id': 'node-25', 'label': 'node-25'}]}
    
# test_1_add_elements_one_by_one()