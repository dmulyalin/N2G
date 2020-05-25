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
    <node id="{id}" xmlns:y="http://www.yworks.com/xml/graphml">
      <data key="{attrib_id}">
        <y:ShapeNode>
          <y:Geometry height="62.0" width="80.0"/>
          <y:Fill color="#FFFFFF" transparent="false"/>
          <y:BorderStyle color="#000000" raised="false" type="line" width="3.0"/>
          <y:Shape type="rectangle"/>
        </y:ShapeNode>
      </data>
    </node>
    """

    svg_node_xml = """
    <node id="{id}" xmlns:y="http://www.yworks.com/xml/graphml">
      <data key="{attrib_id}">
        <y:SVGNode>
          <y:Geometry height="50" width="50"/>
          <y:Fill color="#CCCCFF" transparent="false"/>
          <y:BorderStyle color="#000000" type="line" width="1.0"/>
          <y:SVGNodeProperties usingVisualBounds="true"/>
          <y:SVGModel svgBoundsPolicy="0">
            <y:SVGContent refid="svgPicID"/>
          </y:SVGModel>
        </y:SVGNode>
      </data>
    </node>
    """

    group_node_xml = """
    <node xmlns:y="http://www.yworks.com/xml/graphml" id="nNodeID" yfiles.foldertype="group">
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

    node_label_xml = """
    <y:NodeLabel xmlns:y="http://www.yworks.com/xml/graphml" alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" 
    fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="18" horizontalTextPosition="center" 
    iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" verticalTextPosition="bottom" visible="true" 
    width="70">NodeLabel</y:NodeLabel>
    """

    edge_xml = """
    <edge xmlns:y="http://www.yworks.com/xml/graphml" id="{id}" source="{source}" target="{target}">
      <data key="{attrib_id}">
        <y:PolyLineEdge>
         <y:LineStyle color="#000000" type="line" width="1.0"/>
         <y:Arrows source="none" target="none"/>
         <y:BendStyle smoothed="false"/>
        </y:PolyLineEdge>
      </data>
    </edge>
    """

    edge_label_xml = """
    <y:EdgeLabel xmlns:y="http://www.yworks.com/xml/graphml" alignment="center" backgroundColor="#FFFFFF" configuration="AutoFlippingLabel" distance="2.0" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasLineColor="false" height="18" horizontalTextPosition="center" iconTextGap="4" modelName="free" modelPosition="anywhere" preferredPlacement="target_on_edge" ratio="0.5" textColor="#000000" upX="-1.0" upY="-6E-17" verticalTextPosition="bottom" visible="true" width="32">EdgeLabel<y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" angleReference="relative_to_edge_flow" angleRotationOnRightSide="co" distance="-1.0" placement="center" side="on_edge" sideReference="relative_to_edge_flow"/></y:EdgeLabel>
    """

    resource_xml = """
    <y:Resource id="1" xmlns:y="http://www.yworks.com/xml/graphml">
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

    def __init__(self):
        self.drawing = ET.fromstring(self.graph_xml)
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self.y_attr = {}
        self.edges_ids = []
        self.nodes_ids = {}
        self.svg_pics_dict = {}
        self._load_yattrs()
        # register name spaces names to dump them properly in XML output
        _ = [ET.register_namespace(k, v) for k, v in self.namespaces.items()]

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
            if not key.attrib["for"] in self.y_attr:
                self.y_attr[key.attrib["for"]] = {}
            self.y_attr[key.attrib["for"]][attrname] = key.attrib["id"]

    def _create_label_element(
        self,
        xml_template,  # string, name of XML label template
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

    def _node_exists(self, id, dublicates="log"):
        # check if node with given name already exists, if so, raise error and stop programm:
        if id in self.nodes_ids:
            if dublicates == "log":
                log.error("_addshapenode: node '{}' already added to graph".format(id))
            elif dublicates == "update":
                self.update_node(self.nodes_dict[id], label, attributes, description)
            return True
        self.nodes_ids[id] = id

    def _addshapenode(
        self,
        id,  # string, name of the node
        label="",  # string, label at the center of the node
        top_label="",  # string, label at the top of the node
        bottom_label="",  # string, label at the bottom of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
        dublicates="log",  # string, action if node dublicate found
        url="",  # string, data to add tonode URL
    ):
        """
        method to add node of type "shape", by default shape is "rectangle"
        """
        # check duplicates
        if self._node_exists(id, dublicates):
            return
        # create node element:
        node = ET.fromstring(
            self.shape_node_xml.format(
                attrib_id=self.y_attr["node"]["nodegraphics"], id=id
            )
        )

        # add labels and description data to the node:
        ShapeNode = node.find("./data/y:ShapeNode", self.namespaces)
        if label == "":
            ShapeNode.append(
                self._create_label_element(self.node_label_xml, id, modelPosition="c")
            )
        if label != "":
            ShapeNode.append(
                self._create_label_element(
                    self.node_label_xml, label, modelPosition="c"
                )
            )
        if top_label != "":
            ShapeNode.append(
                self._create_label_element(
                    self.node_label_xml, top_label, modelPosition="t"
                )
            )
        if bottom_label != "":
            ShapeNode.append(
                self._create_label_element(
                    self.node_label_xml, bottom_label, modelPosition="b"
                )
            )
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
                text=json_dumps(
                    {"id": id}
                ),
            )
        )

        # set attributes for the node:
        if attributes:
            self.set_attributes(ShapeNode, attributes)
        self.graph_root.append(node)

    def _addsvgnode(
        self,
        pic,  # string, name of SVG picture file to use
        id,  # string, name of the node
        pic_path="./Pics/",  # string, OS path to SVG picture file
        label="",  # string, label to display above the top of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
        dublicates="exit",  # string, action if node dublicate found
        url="",  # string, data to add tonode URL
    ):
        """
        method to add svg picture node. This method loads SVG picture as resource content into the XML graph file.
        """
        # check duplicates
        if self._node_exists(id, dublicates):
            return
        # sanitize pic:
        if not pic.endswith(".svg"):
            pic += ".svg"
        # create svg_node element:
        svg_node = ET.fromstring(
            self.svg_node_xml.format(
                attrib_id=self.y_attr["node"]["nodegraphics"], id=id
            )
        )

        # check if svg pic with given name already been loaded, if yes, use it:
        svg_pic_already_loaded = False
        for path, params in self.svg_pics_dict.items():
            if path == pic_path + pic:  # hence svg pic already been loaded
                svg_node.find(
                    "./data/y:SVGNode/y:SVGModel/y:SVGContent", self.namespaces
                ).attrib["refid"] = str(params[0])
                svg_node.find("./data/y:SVGNode/y:Geometry", self.namespaces).attrib[
                    "width"
                ] = str(params[1])
                svg_node.find("./data/y:SVGNode/y:Geometry", self.namespaces).attrib[
                    "height"
                ] = str(params[2])
                svg_pic_already_loaded = True
                break
        # load svg pic resource into graph resources section if not yet loaded:
        if svg_pic_already_loaded == False:
            with open(pic_path + pic) as pic_file:
                pic_xml = pic_file.read()
                # extract pic width and height that can be contained in viewBox attribute as well:
                pic_element = ET.fromstring(pic_xml.encode("utf8"))
                pic_viewbox = pic_element.attrib.get("viewBox")
                if pic_viewbox:
                    pic_width = pic_viewbox.split(" ")[3]
                    pic_height = pic_viewbox.split(" ")[2]
                else:
                    pic_width = pic_element.attrib.get("width")
                    pic_height = pic_element.attrib.get("height")
                del pic_element
                # modify pic_xml for inclusion into resource element
                pic_xml = pic_xml.replace("\<", "&lt;").replace("\>", "&gt;")
            resource_id = str(uuid.uuid1())

            # save pic and it's params into sgv_pics_dict dictionary:
            self.svg_pics_dict[pic_path + pic] = [resource_id, pic_width, pic_height]

            # create resource element:
            svg_resource_element = ET.fromstring(self.resource_xml)
            svg_resource_element.attrib["id"] = resource_id
            svg_resource_element.text = pic_xml
            self.drawing.find(
                "./_default_ns_:data/y:Resources", self.namespaces
            ).append(svg_resource_element)
            del svg_resource_element

            # add svg resource refid, width, height parametrs to svg_node element:
            svg_node.find(
                "./data/y:SVGNode/y:SVGModel/y:SVGContent", self.namespaces
            ).attrib["refid"] = resource_id
            svg_node.find("./data/y:SVGNode/y:Geometry", self.namespaces).attrib[
                "width"
            ] = pic_width
            svg_node.find("./data/y:SVGNode/y:Geometry", self.namespaces).attrib[
                "height"
            ] = pic_height
        # add label and description data to the node:
        if label == "":
            svg_node.find("./data/y:SVGNode", self.namespaces).append(
                self._create_label_element(
                    self.node_label_xml, id, modelName="sandwich", modelPosition="n"
                )
            )
        elif label != "":
            svg_node.find("./data/y:SVGNode", self.namespaces).append(
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

    def _addgroupnode(
        self,
        id,  # string, name of the node
        label="",  # string, label at the center of the node
        top_label="",  # string, label at the top of the node
        bottom_label="",  # string, label at the bottom of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
        dublicates="log",  # string, action if node dublicate found
        url="",  # string, data to add tonode URL
    ):
        """
        method to add node of type "shape", by default shape is "rectangle"
        """
        # check for node dublicates:
        if self._node_exists(id, dublicates):
            return
        # create node element:
        node = etree.fromstring(
            group_node_xml.format(attrib_id=self.y_attr["node"]["nodegraphics"])
        )
        self.nodes_dict[id] = id
        node.set("id", id)
        # set id for groupnode graph:
        node.find("./_default_ns_:graph", self.namespaces).attrib["id"] = "{}:".format(id)

        # add labels and description data to the node:
        GroupNode = node.find(
            "./data/y:ProxyAutoBoundsNode/y:Realizers/y:GroupNode",
            self.namespaces
        )
        if label != "":
            GroupNode.append(
                self._create_label_element(self.node_label_xml, label, modelPosition="c")
            )
        if top_label != "":
            GroupNode.append(
                self._create_label_element(self.node_label_xml, top_label, modelPosition="t")
            )
        if bottom_label != "":
            GroupNode.append(
                self._create_label_element(
                    self.node_label_xml, bottom_label, modelPosition="b"
                )
            )
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
                text=json_dumps(
                    {"id": id}, sort_keys=True, indent=4, separators=(",", ": ")
                ),
            )
        )

        # set attributes for the node:
        if attributes:
            self.set_attributes(GroupNode, attributes)
        self.graph_root.append(node)

    def add_node(
        self,
        id,  # string, name of the node
        label="",  # string, label at the center of shape node or above the top of svg node
        top_label="",  # string, label at the top of the node, ignored if pic is present
        bottom_label="",  # string, label at the bottom of the node, ignored if pic is present
        pic="",  # string, name of SVG picture file to use
        pic_path="./Pics/",  # string, OS path to SVG picture file
        attributes={},  #
        description="",  #
        url="",  # string, data to add to node URL
        dublicates="exit",  #
        group=False,  # boolean, to indicate if node is a group if True or relation to group
    ):
        """
        method to add node, by calling one of internal methods, decision made based on presence of 
        'pic', e.g., if present, create svg node, if not, create shape node
        """
        if group == True:
            self._addgroupnode(
                id=id,
                label=label,
                top_label=top_label,
                bottom_label=bottom_label,
                attributes=attributes,
                description=description,
                dublicates=dublicates,
                url=url,
            )
        elif pic == "":
            self._addshapenode(
                id=id,
                label=label,
                top_label=top_label,
                bottom_label=bottom_label,
                attributes=attributes,
                description=description,
                dublicates=dublicates,
                url=url,
            )
        else:
            self._addsvgnode(
                id=id,
                pic=pic,
                pic_path=pic_path,
                label=label,
                attributes=attributes,
                description=description,
                dublicates=dublicates,
                url=url,
            )

    def _edge_exists(self, id, dublicates, edge_tup):
        """method, used to check dublicate edges 
        """
        if id in self.edges_ids:
            if dublicates == "log":
                log.error(
                    "_edge_exists: edge '{}' already added to graph".format(
                        ",", join(edge_tup)
                    )
                )
            return True
        self.edges_ids.append(id)

    def add_link(
        self,
        source,  # string, name of the source node
        target,  # string, name of the terget node
        label="",  # string, label to display in the center of the edge
        src_label="",  # string, label to display at source end of the edge
        trgt_label="",  # string, label to display at target end of the edge
        description="",  # string, text to add as description data to the edge
        label_attribs={},  #
        src_label_attribs={},  #
        trgt_label_attribs={},  #
        attributes={},  # dict, edge attributes
        dublicates="log",  #
        url="",  # string, data to add to edge URL
    ):
        """method to add edge
        """
        # create edge id
        edge_tup = tuple(sorted([source, target, label, src_label, trgt_label,]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        # check dublicates
        if self._edge_exists(edge_id, dublicates, edge_tup):
            return
        # create edge element:
        try:
            source_id = self.nodes_ids[source]
        except KeyError:
            log.error("add_link: no source node found, node id - '{}'".format(source))
            return
        try:
            target_id = self.nodes_ids[target]
        except KeyError:
            log.error("add_link: no target node found, node id - '{}'".format(target))
            return
        edge = ET.fromstring(
            self.edge_xml.format(
                attrib_id=self.y_attr["edge"]["edgegraphics"],
                id=edge_id,
                source=source_id,
                target=target_id
            )
        )
        # fill labels and description:
        PolyLineEdge = edge.find("./data/y:PolyLineEdge", self.namespaces)
        if label != "":
            PolyLineEdge.append(
                self._create_label_element(
                    self.edge_label_xml,
                    label,
                    path="y:PreferredPlacementDescriptor",
                    placement="center",
                )
            )
        if src_label != "":
            PolyLineEdge.append(
                self._create_label_element(
                    self.edge_label_xml,
                    src_label,
                    path="y:PreferredPlacementDescriptor",
                    placement="source",
                )
            )
        if trgt_label != "":
            PolyLineEdge.append(
                self._create_label_element(
                    self.edge_label_xml,
                    trgt_label,
                    path="y:PreferredPlacementDescriptor",
                    placement="target",
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
        # save source and target original nodes' id in edge custom attributes:
        edge.append(
            self._create_data_element(
                id=self.y_attr["edge"]["emetadata"],
                text=json_dumps({"sid": source, "tid": target}),
            )
        )

        # fill in edge attributes:
        if attributes:
            self.set_attributes(PolyLineEdge, attributes)
        # append edge element to graph:
        self.graph_root.append(edge)

    def from_dict(
        self,
        data,  # dictionary, structure: {nodes:[{node1 kwargs}], edges:[{edge1 kwargs}]}
        dublicates="exit",  # string, action to do with dublicates
    ):
        """
        method to load graph from dictionary structured data.
        """
        for node in data.get("nodes", []):
            self.add_node(dublicates=dublicates, **node)
        for link in data.get("links", []):
            self.add_link(dublicates=dublicates, **link)
        for edge in data.get("edges", []):
            self.add_link(dublicates=dublicates, **edge)

    def from_file(self, filename):
        with open(filename, "r") as f:
            self.drawing = ET.fromstring(f.read())
        # load graph details
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self._load_yattrs()
        # load all nodes IDs and build mapping between previously saved ID and ID generated by yED
        nmetadata_id = self.y_attr["node"]["nmetadata"]
        for node in self.graph_root.findall("./_default_ns_:node", self.namespaces):
            node_data = node.find("./_default_ns_:data[@key='{}']".format(nmetadata_id), self.namespaces)
            node_data = json_loads(node_data.text)
            self.nodes_ids[node_data["id"]] = node.attrib["id"]
        # add all edges IDs to self.edges_ids list
        emetadata_id = self.y_attr["edge"]["emetadata"]
        for edge in self.graph_root.findall("./_default_ns_:edge", self.namespaces):
            edge_data = edge.find("./_default_ns_:data[@key='{}']".format(emetadata_id), self.namespaces)
            edge_data = json_loads(edge_data.text)
            source = edge_data["sid"]
            target = edge_data["tid"]
            for label_item in edge.findall(".//*/y:EdgeLabel", self.namespaces):
                placement = label_item.attrib.get("preferredPlacement", "")
                if "center" in placement:
                    label = label_item.text
                elif "source" in placement:
                    src_label = label_item.text
                elif "target" in placement:
                    trgt_label = label_item.text
            edge_tup = tuple(sorted([source, target, label, src_label, trgt_label,]))
            edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
            self.edges_ids.append(edge_id)
        
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
        element,  # lxml object to update attributes in
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
        node_id,  # string, name of the node
        label="",  # string, label at the center of the node
        top_label="",  # string, label at the top of the node
        bottom_label="",  # string, label at the bottom of the node
        attributes={},  # dictionary, contains node attributes
        description="",  # string, data to add in node description
    ):
        # get node element:
        node = self.drawing.xpath(
            './/_default_ns_:node[@id="{}"]'.format(node_id), namespaces=self.ns_dict
        )[0]
        ShapeNode = node.xpath(
            "./_default_ns_:data/y:ShapeNode", namespaces=self.ns_dict
        )
        SVGNode = node.xpath("./_default_ns_:data/y:SVGNode", namespaces=self.ns_dict)
        if ShapeNode:
            NODE = ShapeNode[0]
        elif SVGNode:
            NODE = SVGNode[0]

        # update node attributes:
        self.set_attributes(NODE, attributes)

        # update node labels:
        labels = NODE.findall(".//y:NodeLabel", namespaces=self.ns_dict)
        for l in labels:
            if not "modelPosition" in l.attrib:
                continue
            if l.attrib["modelPosition"] == "c":
                if label:
                    l.text = label
            elif l.attrib["modelPosition"] == "t":
                if top_label:
                    l.text = top_label
            elif l.attrib["modelPosition"] == "b":
                if bottom_label:
                    l.text = bottom_label
            # update label for SVG node
            elif l.attrib["modelPosition"] == "n":
                if label:
                    l.text = label

    def update_edge(self, edge_id="", attributes={}):
        edge = self.drawing.xpath(
            './/_default_ns_:edge[@id="{}"]'.format(edge_id), namespaces=self.ns_dict
        )[0]
        PolyLineEdge = edge.xpath(
            "./_default_ns_:data/y:PolyLineEdge", namespaces=self.ns_dict
        )[0]

        self.set_attributes(PolyLineEdge, attributes)

    def compare(
        self,
        data,  # N2G dictionary data to compare against
        missing_nodes={  # dict, attributes to apply to missing nodes
            "BorderStyle": {"color": "# C0C0C0", "width": "2.0"},
            "NodeLabel": {"textColor": "# C0C0C0"},
        },
        new_nodes={  # dict, attributes to apply to new nodes
            "BorderStyle": {"color": "# 00FF00", "width": "5.0"},
            "NodeLabel": {"textColor": "# 00FF00"},
        },
        missing_edges={  # dict, attributes to apply to missing edges
            "LineStyle": {"color": "# C0C0C0", "width": "1.0"},
            "EdgeLabel": {"textColor": "# C0C0C0"},
        },
        new_edges={  # dict, attributes to apply to new edges
            "LineStyle": {"color": "# 00FF00", "width": "1.0"},
            "EdgeLabel": {"textColor": "# 00FF00"},
        },
    ):
        """method to compare data graph with self.drawing producing third, resulting graph
        """
        # create results_graph object based on self.drawing, that will used to produce
        # compare results graph:
        results_graph = graph(str(etree.tostring(self.drawing), "ascii"))

        if type(data) == dict:
            # find new nodes:
            not_missing_nodes = []
            for node in data["nodes"]:
                if not node["id"] in self.nodes_dict:
                    if "attributes" in node:
                        node["attributes"].update(new_nodes)
                    else:
                        node["attributes"] = new_nodes
                    results_graph.add_node(**node)
                elif node["id"] in self.nodes_dict:
                    not_missing_nodes.append(self.nodes_dict[node["id"]])
            # find missing nodes:
            for id in self.nodes_dict.values():
                if not id in not_missing_nodes:
                    results_graph.update_node(node_id=id, attributes=missing_nodes)
            # find new edges:
            not_missing_edges = []
            for edge in data["edges"]:
                # create edge tuple:
                edge_tup = []

                # try to find source node:
                if edge["source"] in self.nodes_dict:
                    edge_tup.append(edge["source"])
                # if no such node, means we have new edge, add it:
                else:
                    if "attributes" in edge:
                        edge["attributes"].update(new_edges)
                    else:
                        edge["attributes"] = new_edges
                    results_graph.add_link(**edge)
                    continue
                # try to find target node:
                if edge["target"] in self.nodes_dict:
                    edge_tup.append(edge["target"])
                # if no such node, means we have new edge, add it:
                else:
                    if "attributes" in edge:
                        edge["attributes"].update(new_edges)
                    else:
                        edge["attributes"] = new_edges
                    results_graph.add_link(**edge)
                    continue
                # fill in the rest of labels to form tuple:
                if "label" in edge:
                    edge_tup.append(edge["label"])
                else:
                    edge_tup.append("")
                if "src_label" in edge:
                    edge_tup.append(edge["src_label"])
                else:
                    edge_tup.append("")
                if "trgt_label" in edge:
                    edge_tup.append(edge["trgt_label"])
                else:
                    edge_tup.append("")

                edge_tup = tuple(sorted(edge_tup))

                # if no edge_tup in self_edges_dict - means new edge:
                if not edge_tup in self.edges_dict:
                    if "attributes" in edge:
                        edge["attributes"].update(new_edges)
                    else:
                        edge["attributes"] = new_edges
                    results_graph.add_link(**edge)
                # if edge_tup in self_edges_dict - means existing edge:
                elif edge_tup in self.edges_dict:
                    not_missing_edges.append(self.edges_dict[edge_tup])
            # find missing edges:
            for id in self.edges_dict.values():
                if not id in not_missing_edges:
                    results_graph.update_edge(edge_id=id, attributes=missing_edges)
        results_graph.save(file=ctime + "_compare_result.graphml")