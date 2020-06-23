import xml.etree.ElementTree as ET
import hashlib
import uuid

from json import dumps as json_dumps  # need it to dump metadata for edges/nodes
from json import loads as json_loads  # need it to load metadata for edges/nodes

import logging

# initiate logging
log = logging.getLogger(__name__)
LOG_LEVEL = "INFO"
LOG_FILE = None


def logging_config(LOG_LEVEL, LOG_FILE):
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL.upper() in valid_log_levels:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [TTP %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=LOG_LEVEL.upper(),
            filename=LOG_FILE,
            filemode="w",
        )


logging_config(LOG_LEVEL, LOG_FILE)


class yed_diagram:

    # XML string templates to create lxml etree elements from:
    graph_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java" xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0" xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:yed="http://www.yworks.com/xml/yed/3" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
    <!--Created by yEd 3.17.2-->
    <key attr.name="Description" attr.type="string" for="graph" id="d0"/>
    <key for="port" id="d1" yfiles.type="portgraphics"/>
    <key for="port" id="d2" yfiles.type="portgeometry"/>
    <key for="port" id="d3" yfiles.type="portuserdata"/>
    <key attr.name="url" attr.type="string" for="node" id="d4"/>
    <key attr.name="description" attr.type="string" for="node" id="d5"/>
    <key for="node" id="d6" yfiles.type="nodegraphics"/>
    <key for="graphml" id="d7" yfiles.type="resources"/>
    <key attr.name="url" attr.type="string" for="edge" id="d8"/>
    <key attr.name="description" attr.type="string" for="edge" id="d9"/>
    <key for="edge" id="d10" yfiles.type="edgegraphics"/>
    <key attr.name="nmetadata" attr.type="string" for="node" id="d11">
        <default/>
    </key>
    <key attr.name="emetadata" attr.type="string" for="edge" id="d12">
        <default/>
    </key>
    <key attr.name="gmetadata" attr.type="string" for="graph" id="d13">
        <default/>
    </key>
    <graph edgedefault="directed" id="G">
    
    </graph>
    <data key="d7">
        <y:Resources>
        </y:Resources>
    </data>
    </graphml>
    """

    shape_node_xml = """
    <node id="{id}" xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns">
      <data key="{attrib_id}">
        <y:ShapeNode>
          <y:Geometry height="62.0" width="80.0" x="0" y="0"/>
          <y:Fill color="#FFFFFF" transparent="false"/>
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0"/>
          <y:Shape type="{shape_type}"/>
        </y:ShapeNode>
      </data>
    </node>
    """

    svg_node_xml = """
    <node id="{id}" xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns">
      <data key="{attrib_id}">
        <y:SVGNode>
          <y:Geometry width="{width}" height="{height}" x="0" y="0"/>
          <y:Fill color="#CCCCFF" transparent="false"/>
          <y:BorderStyle color="#000000" type="line" width="1.0"/>
          <y:SVGNodeProperties usingVisualBounds="true"/>
          <y:SVGModel svgBoundsPolicy="0">
            <y:SVGContent refid="{refid}"/>
          </y:SVGModel>
        </y:SVGNode>
      </data>
    </node>
    """

    group_node_xml = """
    <node xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns" id="nNodeID" yfiles.foldertype="group">
    <data key="{attrib_id}">
        <y:ProxyAutoBoundsNode>
        <y:Realizers active="0">
            <y:GroupNode>
            <y:Geometry height="50.0" width="50.0" x="0.0" y="0.0"/>
            <y:Fill color="#FFFFFF" color2="#FFFFFF" transparent="false"/>
            <y:BorderStyle color="#000000" type="line" width="1.0"/>
            <y:Shape type="rectangle"/>
            <y:State closed="false" closedHeight="50.0" closedWidth="157.0" innerGraphDisplayEnabled="true"/>
            <y:Insets bottom="5" bottomF="5.0" left="5" leftF="5.0" right="5" rightF="5.0" top="5" topF="5.0"/>
            <y:BorderInsets bottom="0" bottomF="0.0" left="31" leftF="31.0" right="0" rightF="0.0" top="0" topF="0.0"/>
            </y:GroupNode>
        </y:Realizers>
        </y:ProxyAutoBoundsNode>
    </data>
    <graph edgedefault="directed" id="nNodeID:">
    </graph>
    </node>
    """

    edge_xml = """
    <edge xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns" id="{id}" source="{source}" target="{target}">
      <data key="{attrib_id}">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0"/>
         <y:Arrows source="none" target="none"/>
         <y:BendStyle smoothed="false"/>
        </y:PolyLineEdge>
      </data>
    </edge>
    """
    
    node_label_xml = """
    <y:NodeLabel xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns" alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" 
    iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" 
    width="70">NodeLabel</y:NodeLabel>
    """
    
    edge_label_xml = """
    <y:EdgeLabel xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns" alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">
    EdgeLabel
    <y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="center" side="on_edge" sideReference="relative_to_edge_flow"/>
    </y:EdgeLabel>
    """

    resource_xml = """
    <y:Resource id="{id}" xmlns:y="http://www.yworks.com/xml/graphml" xmlns="http://graphml.graphdrawing.org/xmlns">{text_data}
    </y:Resource>
    """

    namespaces = {
        "_default_ns_": "http://graphml.graphdrawing.org/xmlns",
        "java": "http://www.yworks.com/xml/yfiles-common/1.0/java",
        "sys": "http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0",
        "x": "http://www.yworks.com/xml/yfiles-common/markup/2.0",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "y": "http://www.yworks.com/xml/graphml",
        "yed": "http://www.yworks.com/xml/yed/3",
    }

    def __init__(self, node_dublicates="skip", link_dublicates="skip"):
        self.drawing = ET.fromstring(self.graph_xml)
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self.y_attr = {}
        self.node_dublicates=node_dublicates
        self.link_dublicates=link_dublicates
        self.edges_ids = {} # dictionary of "edge id hash": "yed generated edge id"
        self.nodes_ids = {} # dictionary of "human friendly node id": "yed generated node id"
        self.svg_pics_dict = {}
        self._load_yattrs()
        # register name spaces names to dump them properly in XML output
        [ET.register_namespace(k, v) for k, v in self.namespaces.items()]

    def _load_yattrs(self):
        """
        function to load yed tags attributes adn form self.y_attr dict similar to this:
        self.y_attr = {'edge': {'description': 'd9',
                              'edgegraphics': 'd10',
                              'emetadata': 'd12',
                              'url': 'd8'},
                      'graph': {'Description': 'd0', 'gmetadata': 'd13'},
                      'graphml': {'resources': 'd7'},
                      'node': {'description': 'd5',
                              'nmetadata': 'd11',
                              'nodegraphics': 'd6',
                              'url': 'd4'},
                      'port': {'portgeometry': 'd2', 'portgraphics': 'd1', 'portuserdata': 'd3'}}
        """
        keys = self.drawing.findall("./_default_ns_:key", self.namespaces)
        for key in keys:
            if "attr.name" in key.attrib:
                attrname = key.attrib["attr.name"]
            elif "yfiles.type" in key.attrib:
                attrname = key.attrib["yfiles.type"]
            self.y_attr.setdefault(key.attrib["for"], {})
            self.y_attr[key.attrib["for"]][attrname] = key.attrib["id"]

    def _create_label_element(
        self,
        xml_template, # string, name of XML label template
        label="",  # string, center label of edge/nodes
        path="",  # string, xml tree path, if empty, work with element tag
        **kwargs  # attributes for edge/node label lement at "path" tag
    ):
        """
        function to create label elemnts for appending to edge/nodes' elements
        """
        element = ET.fromstring(xml_template)
        if label != "":
            element.text = label
        if path == "":
            element.attrib.update(kwargs)
        else:
            element.find(path, self.namespaces).attrib.update(kwargs)
        return element

    def _create_data_element(
        self,
        id,  # string, id of data element, e,g, d11, d4, d1 etc.
        text,  # string, text to add to data element
    ):
        elem = ET.fromstring('<data key="{}"/>'.format(id))
        elem.text = text.strip()
        return elem

    def _node_exists(self, id, **kwargs):
        # check if node with given name already exists
        if id in self.nodes_ids:
            if self.node_dublicates == "log":
                log.error("add_shape_node: node '{}' already added to graph".format(id))
            elif self.node_dublicates == "skip":
                pass
            elif self.node_dublicates == "update":
                self.update_node(id, **kwargs)
            return True
        else:
            return False

    def add_shape_node(
        self,
        id,
        label="",
        top_label="",
        bottom_label="",
        attributes={},
        description="",
        shape_type="roundrectangle",
        url="",
    ):
        """
        Method to add node of type "shape", by default shape is "roundrectangle"
        
        **Arguments**
        
            * attributes - dictionary of yEd graphml tag name and its attributes, e.g.:
                {
                    'Shape'     : {'type': 'roundrectangle'},
                    'DropShadow': { 'color': '#B3A691', 'offsetX': '5', 'offsetY': '5'}
                }
        """
        # check duplicates
        if self._node_exists(id, label=label, top_label=top_label, 
            bottom_label=bottom_label, attributes=attributes, description=description):
            return
        self.nodes_ids[id] = id
        # create node element:
        node = ET.fromstring(
            self.shape_node_xml.format(
                attrib_id=self.y_attr["node"]["nodegraphics"],
                id=id,
                shape_type=shape_type,
            )
        )

        # add labels
        if label == "":
            label = id
        labels = {"c": label, "t": top_label, "b": bottom_label}
        ShapeNode = node.find("./_default_ns_:data/y:ShapeNode", self.namespaces)
        for position, label_text in labels.items():
            if label_text.strip():
                ShapeNode.append(
                    self._create_label_element(
                        self.node_label_xml, label_text, modelPosition=position
                    )
                )
        # add description data
        if description != "":
            node.append(
                self._create_data_element(
                    id=self.y_attr["node"]["description"], text=description
                )
            )
        if url != "":
            node.append(
                self._create_data_element(id=self.y_attr["node"]["url"], text=url)
            )
        # save original node ID in nmetadata attribute - used to load graph from file:
        node.append(
            self._create_data_element(
                id=self.y_attr["node"]["nmetadata"], text=json_dumps({"id": id}),
            )
        )

        # set attributes for the node children:
        self.set_attributes(ShapeNode, attributes)
        # addnode to graph
        self.graph_root.append(node)

    def add_svg_node(
        self,
        pic,
        id,
        pic_path="./Pics/",
        label="",
        attributes={},
        description="",
        url="",  # string, data to add tonode URL
    ):
        """
        method to add svg picture node. This method loads SVG picture as resource content into the XML graph file.
        """
        # check duplicates
        if self._node_exists(id, label=label, attributes=attributes, description=description):
            return
        self.nodes_ids[id] = id
        # sanitize pic:
        if not pic.endswith(".svg"):
            pic += ".svg"
        pic_file_path = pic_path + pic

        # load svg pic resource into graph resources section if not yet loaded:
        if not pic_file_path in self.svg_pics_dict:
            resource_id = str(uuid.uuid1())
            with open(pic_file_path, "r") as pic_file:
                pic_xml = pic_file.read()
                # extract pic width and height that can be containedin viewBox attribute as well:
                pic_element = ET.fromstring(pic_xml.encode('utf8'))
                if pic_element.attrib.get("viewBox"):
                    _, _, pic_width, pic_height = pic_element.attrib.get("viewBox").split(" ")
                elif pic_element.find(".//*/{http://www.w3.org/2000/svg}svg"):
                    _, _, pic_width, pic_height = pic_element.find(".//*/{http://www.w3.org/2000/svg}svg").attrib.get("viewBox").split(" ")
                else:
                    pic_width = pic_element.get("width", 50)
                    pic_height = pic_element.get("height", 50)
                del(pic_element)
                pic_width = float(pic_width)
                pic_height = float(pic_height)
                # scale width and height down to 100px if size more than 100px
                if  max(pic_width, pic_height) > 100:
                    factor = max(pic_width, pic_height) / 100
                    pic_width = pic_width / factor
                    pic_height = pic_height / factor
                # modify pic_xml for inclusion into resource element
                pic_xml = pic_xml.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;")

            # save pic id and it's params into sgv_pics_dict dictionary:
            self.svg_pics_dict[pic_file_path] = {"refid": resource_id, "height": pic_height, "width": pic_width}

            # create resource element:
            svg_resource_element = ET.fromstring(self.resource_xml.format(
                id=resource_id,
                text_data=pic_xml
            ))
            self.drawing.find(
                "./_default_ns_:data/y:Resources", self.namespaces
            ).append(svg_resource_element)
            del svg_resource_element
        
        params = self.svg_pics_dict[pic_file_path]
        # create svg_node element:
        svg_node = ET.fromstring(
            self.svg_node_xml.format(
                attrib_id=self.y_attr["node"]["nodegraphics"], 
                id=id,
                refid=params["refid"],
                height=params["height"],
                width=params["width"]
            )
        )
            
        # add label and description data to the node:
        if label == "":
            label = id 
        svg_node.find("./_default_ns_:data/y:SVGNode", self.namespaces).append(
            self._create_label_element(
                self.node_label_xml, label, modelName="sandwich", modelPosition="n"
            )
        )
        if description != "":
            svg_node.append(
                self._create_data_element(
                    id=self.y_attr["node"]["description"], text=description
                )
            )
        if url != "":
            svg_node.append(
                self._create_data_element(id=self.y_attr["node"]["url"], text=url)
            )
        # save original id in node custom attribute:
        svg_node.append(
            self._create_data_element(
                id=self.y_attr["node"]["nmetadata"], text=json_dumps({"id": id})
            )
        )

        # add node to the graph and delete node_element:
        self.graph_root.append(svg_node)

    def add_group_node(
        self,
        id,  # string, name of the node
        label="",  # string, label at the center of the node
        top_label="",  # string, label at the top of the node
        bottom_label="",  # string, label at the bottom of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
        url="",  # string, data to add tonode URL
    ):
        """
        method to add node of type "shape", by default shape is "rectangle"
        """
        # check for node dublicates:
        if self._node_exists(id, label=label, top_label=top_label, bottom_label=bottom_label,
            attributes=attributes, description=description):
            return
        self.nodes_ids[id] = id
        # create node element:
        node = etree.fromstring(
            group_node_xml.format(attrib_id=self.y_attr["node"]["nodegraphics"])
        )
        self.nodes_ids[id] = id
        node.set("id", id)
        # set id for groupnode graph:
        node.find("./_default_ns_:graph", self.namespaces).attrib["id"] = "{}:".format(
            id
        )

        # add labels
        GroupNode = node.find(
            "./_default_ns_:data/y:ProxyAutoBoundsNode/y:Realizers/y:GroupNode", self.namespaces
        )
        if label == "":
            label = id
        labels = {"c": label, "t": top_label, "b": bottom_label}
        for position, label_text in labels.items():
            if label_text.strip():
                GroupNode.append(
                    self._create_label_element(
                        self.node_label_xml, label_text, modelPosition=position
                    )
                )
        # add description data
        if description != "":
            node.append(
                self._create_data_element(
                    id=self.y_attr["node"]["description"], text=description
                )
            )
        if url != "":
            node.append(
                self._create_data_element(id=self.y_attr["node"]["url"], text=url)
            )
        # save original id in node custom attribute:
        node.append(
            self._create_data_element(
                id=self.y_attr["node"]["nmetadata"],
                text=json_dumps({"id": id}),
            )
        )

        # set attributes for the node:
        self.set_attributes(GroupNode, attributes)
        self.graph_root.append(node)

    def add_node(self, **kwargs):
        """
        Method to add node, by calling one of node add methods
        
        **Rules**
            * If 'pic' attribute in kwargs - create svg node
            * If group attribute in kwargs and equal to True, add group node
            * Add shape node asa default action
        """
        if kwargs.get("group") == True:
            self.add_group_node(**kwargs)
        elif kwargs.get("pic"):
            self.add_svg_node(**kwargs)
        else:
            self.add_shape_node(**kwargs)

    def _link_exists(self, id, edge_tup):
        """method, used to check dublicate edges 
        """
        if id in self.edges_ids:
            if self.link_dublicates == "log":
                log.error(
                    "_link_exists: edge '{}' already added to graph".format(
                        ",".join(edge_tup)
                    )
                )
            elif self.link_dublicates == "skip":
                pass
            return True
        self.edges_ids.update({id: id})

    def add_link(
        self,
        source,  # string, name of the source node
        target,  # string, name of the terget node
        label="",  # string, label to display in the center of the edge
        src_label="",  # string, label to display at source end of the edge
        trgt_label="",  # string, label to display at target end of the edge
        description="",  # string, text to add as description data to the edge
        attributes={},  # dict, edge attributes
        url="",  # string, data to add to edge URL
    ):
        """method to add edge
        """
        # check type of source and target attribute
        source_node_dict = source.copy() if isinstance(source, dict) else {"id": source}
        source = source_node_dict.pop("id")
        target_node_dict = target.copy() if isinstance(target, dict) else {"id": target}
        target = target_node_dict.pop("id")
        # create edge id
        edge_tup = tuple(sorted([label, src_label, trgt_label, source, target]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        # check if edge already exists
        if self._link_exists(edge_id, edge_tup):
            return
        # check if target and source nodes exist, add it if not, 
        # self._node_exists method will update node
        # if self.node_dublicates set to update, by default its set to skip
        if not self._node_exists(source, **source_node_dict):
            self.add_node(id=source, **source_node_dict)
        source_id = self.nodes_ids[source]
        if not self._node_exists(target, **target_node_dict):
            self.add_node(id=target, **target_node_dict)
        target_id = self.nodes_ids[target]
        # create edge element
        edge = ET.fromstring(
            self.edge_xml.format(
                attrib_id=self.y_attr["edge"]["edgegraphics"],
                id=edge_id,
                source=source_id,
                target=target_id,
            )
        )
        # fill labels and description:
        PolyLineEdge = edge.find("./_default_ns_:data/y:PolyLineEdge", self.namespaces)
        
        labels = {"center": label, "source": src_label, "target": trgt_label}
        for position, label_text in labels.items():
            if label_text.strip():
                PolyLineEdge.append(
                    self._create_label_element(
                        self.edge_label_xml,
                        label_text,
                        path="y:PreferredPlacementDescriptor",
                        placement=position,
                    )
                )
        if description != "":
            edge.append(
                self._create_data_element(
                    id=self.y_attr["edge"]["description"], text=description
                )
            )
        if url != "":
            edge.append(
                self._create_data_element(id=self.y_attr["edge"]["url"], text=url)
            )
        # save source and target original nodes' id in edge emetadata attribute:
        edge.append(
            self._create_data_element(
                id=self.y_attr["edge"]["emetadata"],
                text=json_dumps({"sid": source, "tid": target, "id": edge_id}),
            )
        )

        # fill in edge attributes:
        self.set_attributes(PolyLineEdge, attributes)
        # append edge element to graph:
        self.graph_root.append(edge)

    def from_dict(self, data):
        """
        Method to load graph from dictionary structured data.
        
        **Args**
        
            * data - dictionary with nodes and link/edges details, example::
            
                sample_graph = {
                    'nodes': [
                        {'id': 'a', 'pic': 'router', 'label': 'R1' }, 
                        {'id': 'b', label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'},
                        {'id': 'e', label': 'E'}
                    ], 
                    'edges': [
                        {'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'}
                    ],
                    'links': [
                        {'source': 'a', 'target': 'e'}
                    ]
                }
                
        **Rules**
            
            * dictionary must contain node key with a list of nodes dictionaries
            * each node dictionary must containunique id attribute, other attributes are optional
            * dictionary must contain edges or links key with a list of edges dictionaries
            * each edge dictionary must contain source and target attributes, other attributes are optional
        """
        [self.add_node(**node) for node in data.get("nodes", [])]
        [self.add_link(**link) for link in data.get("links", [])]
        [self.add_link(**edge) for edge in data.get("edges", [])]
        
    def from_list(self, data):
        """
        Method to load graph from list.
        
        **Args**
        
            * data - list of dictionaries with nodes and link/edges details, example::
            
                sample_graph = [
                    {
                    'source': 'a', 'src_label': 'Gig0/0\nUP', 'label': 'DF', 'target': 'b', 'trgt_label': 'Gig0/1', 'description': 'vlans_trunked: 1,2,3\nstate: up'
                    },
                    {
                    'source': 'a', 'target': {
                            {'id': 'e', label': 'somelabel', 'bottom_label':'botlabel', 'top_label':'toplabel', 'description': 'some node description'}
                        }
                    }                
                ]
            
        **Rules**
            * each edge dictionary must have target and source defined 
            * target/source can be a string or a dictionary 
            * dictionary target/source node must contain id attribute, other attributes are optional and can be same as for nodes
            * target/source id must be unique     

        By default node_dublicates action set to 'skip' meaning that node will be added on first occurrence 
        and ignored after that. Set node_dublicates to 'update' if node with given id need to be updated by 
        later occurrences.
        """
        [self.add_link(**edge) for edge in data]
            

    def from_file(self, filename):
        """
        Method to load nodes and links from yed graphml file.
        
        **Args**
        
            * filename - OS path to .graphml file to load
        """
        with open(filename, "r") as f:
            self.from_text(f.read())
            
    def from_text(self, text_data):
        """
        Method to load graph from .graphml XML text produced by yEd
        
        **Args**
        
            * text_data - text data to load
        """
        self.drawing = ET.fromstring(text_data)
        # load graph details
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self._load_yattrs()
        # load all nodes IDs and build mapping between nmetadata ID and ID generated by yED
        nmetadata_id = self.y_attr["node"].get("nmetadata")
        for node in self.graph_root.findall("./_default_ns_:node", self.namespaces):
            node_data = node.find(
                "./_default_ns_:data[@key='{}']".format(nmetadata_id), self.namespaces
            )
            node_data = json_loads(node_data.text)
            self.nodes_ids[node_data["id"]] = node.attrib["id"]
        # add all edges IDs to self.edges_ids list
        emetadata_id = self.y_attr["edge"].get("emetadata")
        for edge in self.graph_root.findall("./_default_ns_:edge", self.namespaces):
            edge_data = edge.find(
                "./_default_ns_:data[@key='{}']".format(emetadata_id), self.namespaces
            )
            edge_data = json_loads(edge_data.text)
            source = edge_data.get("sid")
            target = edge_data.get("tid")
            edge_id = edge_data.get("id")
            if not edge_id:
                # get labels from edge and for. edge hash id
                label, src_label, trgt_label = "", "", ""
                for label_item in edge.findall(".//*/y:EdgeLabel", self.namespaces):
                    placement = label_item.attrib.get("preferredPlacement", "")
                    if "center" in placement:
                        label = label_item.text
                    elif "source" in placement:
                        src_label = label_item.text
                    elif "target" in placement:
                        trgt_label = label_item.text
                # form edge hash
                edge_tup = tuple(sorted([source, target, label, src_label, trgt_label,]))
                edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
            self.edges_ids.update({edge_id: edge.attrib["id"]})

    def dump_xml(self):
        ret = ET.tostring(self.drawing, encoding="unicode")
        ret = ret.replace("_default_ns_:", "").replace(":_default_ns_", "")
        return ret

    def dump_file(self, filename=None, folder="./Output/"):
        import os
        import time

        # check output folder, if not exists, create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        # create file name
        if not filename:
            ctime = time.ctime().replace(":", "-")
            filename = "{}_output.graphml".format(ctime)
        # save file to disk
        with open(folder + filename, "w") as outfile:
            outfile.write(self.dump_xml())

    def set_attributes(
        self,
        element,  # lxml object to update attributes for
        attributes={},  # dictionary of attributes to update
    ):
        """method to update attributes into element"""
        children = element.getchildren()
        for tag, attribs in attributes.items():
            tag_exists = False
            for child in children:
                if tag in child.tag:
                    child.attrib.update(attribs)
                    tag_exists = True
            if tag_exists == False:  # create tag element:
                tag_elem = etree.fromstring(
                    '<y:{} xmlns:y="http://www.yworks.com/xml/graphml"/>'.format(tag)
                )
                tag_elem.attrib.update(attribs)
                element.append(tag_elem)

    def update_node(
        self,
        id,  # string, name of the node
        label="",  # string, label at the center of the node
        top_label="",  # string, label at the top of the node
        bottom_label="",  # string, label at the bottom of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
    ):
        # get node element:
        node = self.graph_root.find(
            "./_default_ns_:node[@id='{}']".format(self.nodes_ids.get(id, id)), self.namespaces
        )
        if node is None:
            log.error("update_node, cannot find node with id - {}".format(self.nodes_ids.get(id, id)))
            return
        labels = {"c": label, "n": label, "t": top_label, "b": bottom_label}
        # try to find shapenode element
        node_elem = node.find(
            "./_default_ns_:data/y:ShapeNode", self.namespaces
        )
        # try to find svgnode element
        if node_elem is None:
            node_elem = node.find("./_default_ns_:data/y:SVGNode", self.namespaces)
            labels = {"n": label}
        if node_elem is None:
            log.error("Failed to find ShapeNode or SVGNode for node with id: '{}'".format(self.nodes_ids.get(id, id)))
            return
        # update attributes, update description if it does not exists
        self.set_attributes(node_elem, attributes)
        if description:
            description_elem = node_elem.find(".//y:data[@key='{}']".format(self.y_attr["node"]["description"]), self.namespaces)
            if not description_elem:
                node_elem.append(
                    self._create_data_element(
                        id=self.y_attr["node"]["description"], text=description
                    )
                )
            else:
                description_elem.text=description
        # iterate over existing labels
        for label_elem in node_elem.findall(".//y:NodeLabel", self.namespaces):
            position = label_elem.attrib.get("modelPosition")
            if labels.get(position, "").strip():
                label_elem.text = labels.pop(position)
        # add new labels
        for label_position, label in labels.items():
            if not label.strip():
                continue
            node_elem.append(
                self._create_label_element(
                    self.node_label_xml, label, modelPosition=label_position
                )
            )

    def update_link(self, 
        edge_id="",
        label="", 
        src_label="", 
        trgt_label="", 
        source="", 
        target="", 
        new_label="", 
        new_src_label="", 
        new_trgt_label="", 
        description="", 
        attributes={}
        ):
        """
        Method to update edge/link. Element to update looked up by ID. IT calculated based on
        label, src_label, trgt_label, source, target attributes.
        
        **Kwargs**
            * edge_id - md5 hash edge id, if not provided, will be generated based on existing labels
            * label - existing edge label
            * src_label - existing edge src_label 
            * trgt_label - existing edge tgt_label
            * source - existing edge source node ID 
            * target - existing edge target node id 
            * new_label - new edge label 
            * new_src_label - new edge src_label 
            * new_trgt_label - new edge tgt_label 
            * description - new edge description 
            * attributes - dictionary of attributes to apply to edge element        
        """
        # get edge new labels
        new_label = new_label if new_label.strip() else label
        new_src_label = new_src_label if new_src_label.strip() else src_label
        new_trgt_label = new_trgt_label if new_trgt_label.strip() else trgt_label
        # generate existing and new edge ID
        edge_tup = tuple(sorted([label, src_label, trgt_label, source, target]))
        new_edge_tup = tuple(sorted([new_label, new_src_label, new_trgt_label, source, target])) 
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest() if not edge_id else edge_id
        new_edge_id = hashlib.md5(",".join(new_edge_tup).encode()).hexdigest() if not edge_id else edge_id
        if edge_id in self.edges_ids:
            self.edges_ids.update(
                    {
                    new_edge_id: self.edges_ids.pop(edge_id)
                }
            )
        else:
            log.warning("update_link, link does not exist - source '{}', target '{}', label '{}', src_label '{}', trgt_label '{}'".format(
                    source, target, label, src_label, trgt_label
                )
            )            
            return            
		# find edge element
        edge = self.graph_root.find('./_default_ns_:edge[@id="{}"]'.format(self.edges_ids.get(edge_id, edge_id)), namespaces=self.namespaces)
        PolyLineEdge = edge.find("./_default_ns_:data/y:PolyLineEdge", self.namespaces)
        # update edge id
        edge.attrib["id"] = self.edges_ids[new_edge_id]
        # update description
        if description:
            description_elem = edge.find(".//y:data[@key='{}']".format(self.y_attr["edge"]["description"]), self.namespaces)
            if description_elem is None:
                edge.append(
                    self._create_data_element(
                        id=self.y_attr["edge"]["description"], text=description
                    )
                )
            else:
                description_elem.text=description
        # update labels
        labels = {"center": new_label, "source": new_src_label, "target": new_trgt_label}
        # iterate over existing labels
        for label_elem in PolyLineEdge.findall(".//y:EdgeLabel", self.namespaces):
            label_placement_elem = label_elem.find(".//y:PreferredPlacementDescriptor",  self.namespaces)
            position = label_placement_elem.attrib.get("placement")
            if labels.get(position, "").strip():
                label_elem.text = labels.pop(position)
        # add new labels
        for position, label_text in labels.items():
            if not label_text.strip():
                continue
            PolyLineEdge.append(
                self._create_label_element(
                    self.edge_label_xml,
                    label_text,
                    path="y:PreferredPlacementDescriptor",
                    placement=position,
                )
            )
        # update attributes
        self.set_attributes(PolyLineEdge, attributes)

    def compare(
        self,
        data,  # N2G dictionary data to compare against
        missing_nodes={  # dict, attributes to apply to missing nodes
            "BorderStyle": {"color": "#C0C0C0", "width": "2.0"},
            "NodeLabel": {"textColor": "#C0C0C0"},
        },
        new_nodes={  # dict, attributes to apply to new nodes
            "BorderStyle": {"color": "#00FF00", "width": "5.0"},
            "NodeLabel": {"textColor": "#00FF00"},
        },
        missing_edges={  # dict, attributes to apply to missing edges
            "LineStyle": {"color": "#C0C0C0", "width": "1.0"},
            "EdgeLabel": {"textColor": "#C0C0C0"},
        },
        new_edges={  # dict, attributes to apply to new edges
            "LineStyle": {"color": "#00FF00", "width": "1.0"},
            "EdgeLabel": {"textColor": "#00FF00"},
        },
    ):
        """method to compare data graph with self.drawing and produce resulting graph
        """
        if isinstance(data, dict):
            # find new nodes
            existing_nodes = []
            new_nodes_list = []
            for node in data["nodes"]:
                node.setdefault("attributes", {})
                if not node["id"] in self.nodes_ids:
                    node["attributes"].update(new_nodes)
                    self.add_node(**node)
                    new_nodes_list.append(node["id"])
                else:
                    existing_nodes.append(node["id"])
            # find missing nodes
            for id in self.nodes_ids.keys():
                if not id in existing_nodes and not id in new_nodes_list:
                    self.update_node(id=id, attributes=missing_nodes)
                    
            # find new edges:
            existing_edges = []
            new_edges_list = []
            for edge in data["edges"]:
                edge.setdefault("attributes", {})
                # create edge id
                edge_tup = tuple(sorted(
                    [
                        edge["source"], 
                        edge["target"], 
                        edge.get("label", ""), 
                        edge.get("src_label", ""), 
                        edge.get("trgt_label", "")
                    ]))
                edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
                # add new edge
                if not edge_id in self.edges_ids:
                    edge["attributes"].update(new_edges)
                    self.add_link(**edge)
                    new_edges_list.append(edge_id)
                else:
                    existing_edges.append(edge_id)                
            # find missing edges:
            for id in self.edges_ids.keys():
                if not id in existing_edges and not id in new_edges_list:
                    self.update_link(edge_id=id, attributes=missing_edges)
