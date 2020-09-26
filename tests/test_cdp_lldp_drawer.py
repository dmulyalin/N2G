import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cdp_lldp_drawer

def test_cdp_drawing_yed_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail 
-------------------------
Device ID: switch-2
Entry address(es): 
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP 
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-3
Entry address(es): 
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es): 
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10
    """,
    """
switch-2#show cdp neighbors detail 
-------------------------
Device ID: switch-1
Entry address(es): 
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP 
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6    
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cdp_lldp_drawer(drawing, data, config)
    assert drawer.parsed_data == [{'cdp_peers': [{'source': 'switch-1',
                                                  'src_label': 'Ge4/6',
                                                  'target': {'bottom_label': 'cisco WS-C6509',
                                                             'id': 'switch-2',
                                                             'top_label': '10.2.2.2'},
                                                  'trgt_label': 'Ge1/5'},
                                                 {'source': 'switch-1',
                                                  'src_label': 'Ge1/1',
                                                  'target': {'bottom_label': 'cisco WS-C3560-48TS',
                                                             'id': 'switch-3',
                                                             'top_label': '10.3.3.3'},
                                                  'trgt_label': 'Ge0/1'},
                                                 {'source': 'switch-1',
                                                  'src_label': 'Ge1/2',
                                                  'target': {'bottom_label': 'cisco WS-C3560-48TS',
                                                             'id': 'switch-4',
                                                             'top_label': '10.4.4.4'},
                                                  'trgt_label': 'Ge0/10'},
                                                 {'source': 'switch-2',
                                                  'src_label': 'Ge1/5',
                                                  'target': {'bottom_label': 'cisco WS-C6509',
                                                             'id': 'switch-1',
                                                             'top_label': '10.1.1.1'},
                                                  'trgt_label': 'Ge4/6'}]}]
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict.graphml") as f:
        assert f.read() == """<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
    
    <key attr.name="Description" attr.type="string" for="graph" id="d0" />
    <key for="port" id="d1" yfiles.type="portgraphics" />
    <key for="port" id="d2" yfiles.type="portgeometry" />
    <key for="port" id="d3" yfiles.type="portuserdata" />
    <key attr.name="url" attr.type="string" for="node" id="d4" />
    <key attr.name="description" attr.type="string" for="node" id="d5" />
    <key for="node" id="d6" yfiles.type="nodegraphics" />
    <key for="graphml" id="d7" yfiles.type="resources" />
    <key attr.name="url" attr.type="string" for="edge" id="d8" />
    <key attr.name="description" attr.type="string" for="edge" id="d9" />
    <key for="edge" id="d10" yfiles.type="edgegraphics" />
    <key attr.name="nmetadata" attr.type="string" for="node" id="d11">
        <default />
    </key>
    <key attr.name="emetadata" attr.type="string" for="edge" id="d12">
        <default />
    </key>
    <key attr.name="gmetadata" attr.type="string" for="graph" id="d13">
        <default />
    </key>
    <graph edgedefault="directed" id="G">
    
    <node id="switch-1">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-1</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.1.1.1</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C6509</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-1"}</data></node><node id="switch-2">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-2</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.2.2.2</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C6509</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-2"}</data></node><edge id="0d1e25a0122c562fa9bc515040ed5607" source="switch-1" target="switch-2">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge4/6<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/5<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-2", "id": "0d1e25a0122c562fa9bc515040ed5607"}</data></edge><node id="switch-3">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-3</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.3.3.3</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C3560-48TS</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-3"}</data></node><edge id="6c9855a7f657e1b36f49ff33306a96fa" source="switch-1" target="switch-3">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/1<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge0/1<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-3", "id": "6c9855a7f657e1b36f49ff33306a96fa"}</data></edge><node id="switch-4">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-4</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.4.4.4</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C3560-48TS</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-4"}</data></node><edge id="1a55473cf64b1d33fe9a470093808d0d" source="switch-1" target="switch-4">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/2<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge0/10<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-4", "id": "1a55473cf64b1d33fe9a470093808d0d"}</data></edge></graph>
    <data key="d7">
        <y:Resources>
        </y:Resources>
    </data>
    </graphml>"""    
# test_cdp_drawing_yed_data_dict()

def test_cdp_drawing_yed_data_path():
    data = "./Data/SAMPLE_CDP_LLDP/"
    config = {}
    drawing = create_yed_diagram()
    drawer = cdp_lldp_drawer(drawing, data, config)
    assert drawer.parsed_data == [{'cdp_peers': [{'source': 'switch-1',
                                                  'src_label': 'Ge4/6',
                                                  'target': {'bottom_label': 'cisco WS-C6509',
                                                             'id': 'switch-2',
                                                             'top_label': '10.2.2.2'},
                                                  'trgt_label': 'Ge1/5'},
                                                 {'source': 'switch-1',
                                                  'src_label': 'Ge1/1',
                                                  'target': {'bottom_label': 'cisco WS-C3560-48TS',
                                                             'id': 'switch-3',
                                                             'top_label': '10.3.3.3'},
                                                  'trgt_label': 'Ge0/1'},
                                                 {'source': 'switch-1',
                                                  'src_label': 'Ge1/2',
                                                  'target': {'bottom_label': 'cisco WS-C3560-48TS',
                                                             'id': 'switch-4',
                                                             'top_label': '10.4.4.4'},
                                                  'trgt_label': 'Ge0/10'},
                                                 {'source': 'switch-2',
                                                  'src_label': 'Ge1/5',
                                                  'target': {'bottom_label': 'cisco WS-C6509',
                                                             'id': 'switch-1',
                                                             'top_label': '10.1.1.1'},
                                                  'trgt_label': 'Ge4/6'}]}]
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path.graphml") as f:
        assert f.read() == """<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
    
    <key attr.name="Description" attr.type="string" for="graph" id="d0" />
    <key for="port" id="d1" yfiles.type="portgraphics" />
    <key for="port" id="d2" yfiles.type="portgeometry" />
    <key for="port" id="d3" yfiles.type="portuserdata" />
    <key attr.name="url" attr.type="string" for="node" id="d4" />
    <key attr.name="description" attr.type="string" for="node" id="d5" />
    <key for="node" id="d6" yfiles.type="nodegraphics" />
    <key for="graphml" id="d7" yfiles.type="resources" />
    <key attr.name="url" attr.type="string" for="edge" id="d8" />
    <key attr.name="description" attr.type="string" for="edge" id="d9" />
    <key for="edge" id="d10" yfiles.type="edgegraphics" />
    <key attr.name="nmetadata" attr.type="string" for="node" id="d11">
        <default />
    </key>
    <key attr.name="emetadata" attr.type="string" for="edge" id="d12">
        <default />
    </key>
    <key attr.name="gmetadata" attr.type="string" for="graph" id="d13">
        <default />
    </key>
    <graph edgedefault="directed" id="G">
    
    <node id="switch-1">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-1</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.1.1.1</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C6509</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-1"}</data></node><node id="switch-2">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-2</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.2.2.2</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C6509</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-2"}</data></node><edge id="0d1e25a0122c562fa9bc515040ed5607" source="switch-1" target="switch-2">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge4/6<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/5<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-2", "id": "0d1e25a0122c562fa9bc515040ed5607"}</data></edge><node id="switch-3">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-3</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.3.3.3</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C3560-48TS</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-3"}</data></node><edge id="6c9855a7f657e1b36f49ff33306a96fa" source="switch-1" target="switch-3">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/1<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge0/1<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-3", "id": "6c9855a7f657e1b36f49ff33306a96fa"}</data></edge><node id="switch-4">
      <data key="d6">
        <y:ShapeNode>
          <y:Geometry height="60" width="120" x="200" y="150" />
          <y:Fill color="#FFFFFF" transparent="false" />
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0" />
          <y:Shape type="roundrectangle" />
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">switch-4</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="t" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">10.4.4.4</y:NodeLabel><y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="internal" modelPosition="b" textColor="#000000" verticalTextPosition="bottom" visible="true" width="70">cisco WS-C3560-48TS</y:NodeLabel></y:ShapeNode>
      </data>
    <data key="d11">{"id": "switch-4"}</data></node><edge id="1a55473cf64b1d33fe9a470093808d0d" source="switch-1" target="switch-4">
      <data key="d10">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0" />
         <y:Arrows source="none" target="none" />
         <y:BendStyle smoothed="false" />
        <y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge1/2<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="source" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel><y:EdgeLabel alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">Ge0/10<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="target" side="on_edge" sideReference="relative_to_edge_flow" />
    </y:EdgeLabel></y:PolyLineEdge>
      </data>
    <data key="d12">{"sid": "switch-1", "tid": "switch-4", "id": "1a55473cf64b1d33fe9a470093808d0d"}</data></edge></graph>
    <data key="d7">
        <y:Resources>
        </y:Resources>
    </data>
    </graphml>"""
    
# test_cdp_drawing_yed_data_path()