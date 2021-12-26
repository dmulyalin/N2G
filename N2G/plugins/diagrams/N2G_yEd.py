import xml.etree.ElementTree as ET
import hashlib
import os
from json import dumps as json_dumps  # need it to dump metadata for edges/nodes
from json import loads as json_loads  # need it to load metadata for edges/nodes

import logging

# initiate logging
log = logging.getLogger(__name__)
LOG_LEVEL = "ERROR"
LOG_FILE = None


def logging_config(LOG_LEVEL, LOG_FILE):
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL.upper() in valid_log_levels:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [N2G_YED %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=LOG_LEVEL.upper(),
            filename=LOG_FILE,
            filemode="w",
        )


logging_config(LOG_LEVEL, LOG_FILE)


class yed_diagram:
    """
    N2G yEd module allows to produce diagrams in yEd .graphml format.

    **Parameters**

    * ``node_duplicates`` (str) can be of value skip, log, update
    * ``link_duplicates`` (str) can be of value skip, log, update

    """

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
          <y:Geometry height="{height}" width="{width}" x="{x}" y="{y}"/>
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
          <y:Geometry width="{width}" height="{height}" x="{x}" y="{y}"/>
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
    width="70"></y:NodeLabel>
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

    def __init__(self, node_duplicates="skip", link_duplicates="skip"):
        self.drawing = ET.fromstring(self.graph_xml)
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self.y_attr = {}
        self.node_duplicates = node_duplicates
        self.link_duplicates = link_duplicates
        self.edges_ids = {}  # dictionary of "edge id hash": "yed generated edge id"
        self.nodes_ids = {}  # dictionary of "node id": "yed generated node id"
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
        xml_template,  # string, name of XML label template
        label="",  # string, center label of edge/nodes
        path="",  # string, xml tree path, if empty, work with element tag
        **kwargs  # attributes for edge/node label lement at "path" tag
    ):
        """
        function to create label elemnts for appending to edge/nodes' elements
        """
        element = ET.fromstring(xml_template)
        if label != None:
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
            if self.node_duplicates == "log":
                log.error("add_shape_node: node '{}' already added to graph".format(id))
            elif self.node_duplicates == "skip":
                pass
            elif self.node_duplicates == "update":
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
        width=120,
        height=60,
        x_pos=200,
        y_pos=150,
        **kwargs
    ):
        """
        Method to add node of type "shape".

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier, usually equal to node name
        * ``label`` (str) label at the center of the node, by default equal to id attribute
        * ``top_label`` (str) label displayed at the top of the node
        * ``bottom_label`` (str) label displayed at the bottom of the node
        * ``description`` (str) string to save as node ``description`` attribute
        * ``shape_type`` (str) shape type, default - "roundrectangle"
        * ``url`` (str) url string to save a node ``url`` attribute
        * ``width`` (int) node width in pixels
        * ``height`` (int) node height in pixels
        * ``x_pos`` (int) node position on x axis
        * ``y_pos`` (int) node position on y axis
        * ``attributes`` (dict) dictionary of yEd graphml tag names and attributes

        Attributes dictionary keys will be used as xml tag names and values
        dictionary will be used as xml tag attributes, example::

            {
                'Shape'     : {'type': 'roundrectangle'},
                'DropShadow': { 'color': '#B3A691', 'offsetX': '5', 'offsetY': '5'}
            }

        """
        # check duplicates
        if self._node_exists(
            id,
            label=label,
            top_label=top_label,
            bottom_label=bottom_label,
            attributes=attributes,
            description=description,
        ):
            return
        self.nodes_ids[id] = id
        # create node element:
        node = ET.fromstring(
            self.shape_node_xml.format(
                attrib_id=self.y_attr["node"]["nodegraphics"],
                id=id,
                shape_type=shape_type,
                width=width,
                height=height,
                x=x_pos,
                y=y_pos,
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
        # add description data and url
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
                id=self.y_attr["node"]["nmetadata"], text=json_dumps({"id": id})
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
        width=50,
        height=50,
        x_pos=200,
        y_pos=150,
        **kwargs
    ):
        """
        Method to add SVG picture as node by loading SVG file content into graphml

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier, usually equal to node name
        * ``pic`` (str) mandatory, name of svg file
        * ``pic_path`` (str) OS path to SVG file folder, default is ``./Pics/``
        * ``label`` (str) label displayed above SVG node, if not provided,  label set equal to id
        * ``description`` (str) string to save as node ``description`` attribute
        * ``url`` (str) url string to save as node ``url`` attribute
        * ``width`` (int) node width in pixels
        * ``height`` (int) node height in pixels
        * ``x_pos`` (int) node position on x axis
        * ``y_pos`` (int) node position on y axis
        * ``attributes`` (dict) dictionary of yEd graphml tag names and attributes

        Attributes dictionary keys will be used as xml tag names and values
        dictionary will be used as xml tag attributes, example::

            {
                'DropShadow': { 'color': '#B3A691', 'offsetX': '5', 'offsetY': '5'}
            }
        """
        # check duplicates
        if self._node_exists(
            id, label=label, attributes=attributes, description=description
        ):
            return
        # sanitize pic:
        if not pic.endswith(".svg"):
            pic += ".svg"
        pic_file_path = pic_path + pic
        # check if file exists
        if not os.path.exists(pic_file_path):
            log.error(
                "add_svg_node: failed to load svg, '{}' - file not found".format(
                    pic_file_path
                )
            )
            return
        self.nodes_ids[id] = id

        # load svg pic resource into graph resources section if not yet loaded:
        if not pic_file_path in self.svg_pics_dict:
            resource_id = hashlib.md5(pic_file_path.encode()).hexdigest()
            with open(pic_file_path, "r") as pic_file:
                pic_xml = pic_file.read()
                # extract pic width and height that can be containedin viewBox attribute as well:
                pic_element = ET.fromstring(pic_xml.encode("utf8"))
                if pic_element.attrib.get("viewBox"):
                    _, _, pic_width, pic_height = pic_element.attrib.get(
                        "viewBox"
                    ).split(" ")
                elif pic_element.find(".//*/{http://www.w3.org/2000/svg}svg"):
                    _, _, pic_width, pic_height = (
                        pic_element.find(".//*/{http://www.w3.org/2000/svg}svg")
                        .attrib.get("viewBox")
                        .split(" ")
                    )
                else:
                    pic_width = pic_element.get("width", width)
                    pic_height = pic_element.get("height", height)
                del pic_element
                pic_width = float(pic_width)
                pic_height = float(pic_height)
                # scale width and height down to 100px if size more than 100px
                if max(pic_width, pic_height) > 100:
                    factor = max(pic_width, pic_height) / 100
                    pic_width = pic_width / factor
                    pic_height = pic_height / factor
                # modify pic_xml for inclusion into resource element
                pic_xml = (
                    pic_xml.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("'", "&apos;")
                )
            # save pic id and it's params into sgv_pics_dict dictionary:
            self.svg_pics_dict[pic_file_path] = {
                "refid": resource_id,
                "height": pic_height,
                "width": pic_width,
            }

            # create resource element:
            svg_resource_element = ET.fromstring(
                self.resource_xml.format(id=resource_id, text_data=pic_xml)
            )
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
                width=params["width"],
                x=x_pos,
                y=y_pos,
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

    def _add_group_node(
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
        NOT IMPLEMENTED.

        Method to add group node to join nodes in cluster.
        """
        # check for node duplicates:
        if self._node_exists(
            id,
            label=label,
            top_label=top_label,
            bottom_label=bottom_label,
            attributes=attributes,
            description=description,
        ):
            return
        self.nodes_ids[id] = id
        # create node element:
        node = ET.fromstring(
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
            "./_default_ns_:data/y:ProxyAutoBoundsNode/y:Realizers/y:GroupNode",
            self.namespaces,
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
                id=self.y_attr["node"]["nmetadata"], text=json_dumps({"id": id})
            )
        )

        # set attributes for the node:
        self.set_attributes(GroupNode, attributes)
        self.graph_root.append(node)

    def add_node(self, id, **kwargs):
        """
        Convenience method to add node, by calling one of node add methods following
        these rules:

            * If ``pic`` attribute in kwargs, ``add_svg_node`` is called
            * If ``group`` kwargs attribute equal to `True`, ``_add_group_node`` called
            * ``add_shape_node`` called otherwise

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier, usually equal to node name

        """
        kwargs["id"] = id
        if kwargs.get("group", "").strip() == True:
            self._add_group_node(**kwargs)
        elif kwargs.get("pic", "").strip():
            self.add_svg_node(**kwargs)
        else:
            self.add_shape_node(**kwargs)

    def _link_exists(self, id, edge_tup):
        """method, used to check dublicate edges"""
        if id in self.edges_ids:
            if self.link_duplicates == "log":
                log.error(
                    "_link_exists: edge '{}' already added to graph".format(
                        ",".join(edge_tup)
                    )
                )
            elif self.link_duplicates == "skip":
                pass
            return True
        self.edges_ids.update({id: id})

    def add_link(
        self,
        source,
        target,
        label="",
        src_label="",
        trgt_label="",
        description="",
        attributes={},
        url="",
        link_id=None,
    ):
        """
        Method to add link between nodes.

        **Parameters**

        * ``source`` (str) mandatory, id of source node
        * ``target`` (str) mandatory, id of target node
        * ``label`` (str) label at the center of the edge, by default equal to id attribute
        * ``src_label`` (str) label to display at the source end of the edge
        * ``trgt_label`` (str) label to display at target end of the edge
        * ``description`` (str) string to save as link ``description`` attribute
        * ``url`` (str) string to save as link ``url`` attribute
        * ``attributes`` (dict) dictionary of yEd graphml tag names and attributes
        * ``link_id`` (str or int) optional link id value, must be unique across all links

        Attributes dictionary keys will be used as xml tag names and values
        dictionary will be used as xml tag attributes, example::

            {
                "LineStyle": {"color": "#00FF00", "width": "1.0"},
                "EdgeLabel": {"textColor": "#00FF00"},
            }

        .. note:: If source or target nodes does not exists, they will be automatically
          created

        """
        # check type of source and target attribute
        source_node_dict = source.copy() if isinstance(source, dict) else {"id": source}
        source = source_node_dict.pop("id")
        target_node_dict = target.copy() if isinstance(target, dict) else {"id": target}
        target = target_node_dict.pop("id")
        # check if target and source nodes exist, add it if not,
        # self._node_exists method will update node
        # if self.node_duplicates set to update, by default its set to skip
        if not self._node_exists(source, **source_node_dict):
            self.add_node(id=source, **source_node_dict)
        source_id = self.nodes_ids[source]
        if not self._node_exists(target, **target_node_dict):
            self.add_node(id=target, **target_node_dict)
        target_id = self.nodes_ids[target]
        # create edge id if not given
        if link_id:
            link_id = "link_id:{}".format(link_id)
            edge_tup = link_id
        else:
            edge_tup = tuple(sorted([label, src_label, trgt_label, source, target]))
            link_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        # check if edge already exists
        if self._link_exists(link_id, edge_tup):
            return
        # create edge element
        edge = ET.fromstring(
            self.edge_xml.format(
                attrib_id=self.y_attr["edge"]["edgegraphics"],
                id=link_id,
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
                text=json_dumps({"sid": source, "tid": target, "id": link_id}),
            )
        )

        # fill in edge attributes:
        self.set_attributes(PolyLineEdge, attributes)
        # append edge element to graph:
        self.graph_root.append(edge)

    def from_dict(self, data):
        """
        Method to build graph from dictionary.

        **Parameters**

        * ``data`` (dict) dictionary with nodes and link/edges details.

        Example ``data`` dictionary::

            sample_graph = {
                'nodes': [
                    {
                        'id': 'a',
                        'pic': 'router',
                        'label': 'R1'
                    },
                    {
                        'id': 'b',
                        'label': 'somelabel',
                        'bottom_label':'botlabel',
                        'top_label':'toplabel',
                        'description': 'some node description'
                    },
                    {
                        'id': 'e',
                        'label': 'E'
                    }
                ],
                'edges': [
                    {
                        'source': 'a',
                        'src_label': 'Gig0/0',
                        'label': 'DF',
                        'target': 'b',
                        'trgt_label': 'Gig0/1',
                        'description': 'vlans_trunked: 1,2,3'
                    }
                ],
                'links': [
                    {
                        'source': 'a',
                        'target': 'e'
                    }
                ]
            }

        **Dictionary Content Rules**

        * dictionary may contain ``nodes`` key with a list of nodes dictionaries
        * each node dictionary must contain unique ``id`` attribute, other attributes are optional
        * dictionary may contain ``edges`` or ``links`` key with a list of edges dictionaries
        * each link dictionary must contain ``source`` and ``target`` attributes, other attributes are optional

        """
        [self.add_node(**node) for node in data.get("nodes", [])]
        [self.add_link(**link) for link in data.get("links", [])]
        [self.add_link(**edge) for edge in data.get("edges", [])]

    def from_list(self, data):
        """
        Method to build graph from list.

        **Parameters**

        * ``data`` (list) list of link dictionaries,

        Example ``data`` list::

            sample_graph = [
                {
                    'source': 'a',
                    'src_label': 'Gig0/0\\nUP',
                    'label': 'DF',
                    'target': 'b',
                    'trgt_label': 'Gig0/1',
                    'description': 'vlans_trunked: 1,2,3\\nstate: up'
                },
                {
                    'source': 'a',
                    'target': {
                            'id': 'e',
                            'label': 'somelabel',
                            'bottom_label':'botlabel',
                            'top_label':'toplabel',
                            'description': 'some node description'
                        }
                    }
                }
            ]

        **List Content Rules**

            * each list item must have ``target`` and ``source`` attributes defined
            * ``target``/``source`` attributes can be either a string or a dictionary
            * dictionary ``target``/``source`` node must contain ``id`` attribute and
              other supported node attributes

        .. note::

            By default yed_diagram object ``node_duplicates`` action set to 'skip' meaning that node will be added on first occurrence
            and ignored after that. Set ``node_duplicates`` to 'update' if node with given id need to be updated by
            later occurrences in the list.
        """
        [self.add_link(**edge) for edge in data if edge]

    def from_file(self, filename, file_load="xml"):
        """
        Method to load data from file for processing. File format can
        be yEd graphml (XML) or CSV

        **Parameters**

        * ``filename`` (str) OS path to file to load
        * ``file_load`` (str) indicated the load of the file, supports ``xml``, ``csv``

        """
        with open(filename, "r") as f:
            if file_load.lower() == "xml":
                self.from_xml(f.read())
            elif file_load.lower() == "csv":
                self.from_csv(data=csv_load)

    def from_xml(self, text_data):
        """
        Method to load yEd graphml XML formatted text for processing

        **Parameters**

        * ``text_data`` (str) text data to load

        """
        self.drawing = ET.fromstring(text_data)
        # load graph details
        self.graph_root = self.drawing.find("./_default_ns_:graph", self.namespaces)
        self._load_yattrs()
        # load all nodes IDs and build mapping between nmetadata ID and ID generated by yED
        nmetadata_id = self.y_attr["node"].get("nmetadata")
        for node in self.graph_root.iterfind("./_default_ns_:node", self.namespaces):
            node_data = node.find(
                "./_default_ns_:data[@key='{}']".format(nmetadata_id), self.namespaces
            )
            node_data = json_loads(node_data.text)
            self.nodes_ids[node_data["id"]] = node.attrib["id"]
        # add all edges IDs to self.edges_ids list
        emetadata_id = self.y_attr["edge"].get("emetadata")
        for edge in self.graph_root.iterfind("./_default_ns_:edge", self.namespaces):
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
                for label_item in edge.iterfind(".//*/y:EdgeLabel", self.namespaces):
                    placement = label_item.attrib.get("preferredPlacement", "")
                    if "center" in placement:
                        label = label_item.text
                    elif "source" in placement:
                        src_label = label_item.text
                    elif "target" in placement:
                        trgt_label = label_item.text
                # form edge hash
                edge_tup = tuple(sorted([source, target, label, src_label, trgt_label]))
                edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
            self.edges_ids.update({edge_id: edge.attrib["id"]})

    def from_csv(self, text_data):
        """
        Method to build graph from CSV tables

        **Parameters**

        * ``text_data`` (str) CSV text with links or nodes details

        This method supports loading CSV text data that contains nodes or links
        information. If ``id`` in headers, ``from_dict`` method will be called for CSV
        processing, ``from_list`` method will be used otherwise.

        CSV data with nodes details should have headers matching add node methods
        arguments and rules.

        CSV data with links details should have headers matching ``add_link`` method
        arguments and rules.

        Sample CSV table with link details::

            "source","src_label","label","target","trgt_label","description"
            "a","Gig0/0","DF","b","Gig0/1","vlans_trunked: 1,2,3"
            "b","Gig0/0","Copper","c","Gig0/2",
            "b","Gig0/0","Copper","e","Gig0/2",
            d,Gig0/21,FW,e,Gig0/23,

        Sample CSV table with node details::

            "id","pic","label","bottom_label","top_label","description"
            a,router_1,"R1,2",,,
            "b",,,"some","top_some",
            "c",,"somelabel","botlabel","toplabel","some node description"
            "d","firewall.svg","somelabel1",,,"some node description"
            "e","router_2","R1",,,

        """
        # import libs
        from io import StringIO
        import csv

        # need to handle text data as file like object for csv reader to work
        iostring = StringIO(newline="")
        iostring.write(text_data)
        iostring.seek(0)
        # load csv data
        dict_reader = csv.DictReader(iostring)
        data_list = list(dict_reader)
        # if id given - meaning it is nodes data
        if data_list[0].get("id"):
            self.from_dict({"nodes": data_list})
        else:
            self.from_list(data_list)

    def dump_xml(self):
        """
        Method to return current diagram XML text
        """
        ret = ET.tostring(self.drawing, encoding="unicode")
        ret = ret.replace("_default_ns_:", "").replace(":_default_ns_", "")
        return ret

    def dump_file(self, filename=None, folder="./Output/"):
        """
        Method to save current diagram in .graphml file.

        **Parameters**

        * ``filename`` (str) name of the file to save diagram into
        * ``folder`` (str) OS path to folder where to save diagram file

        If no ``filename`` provided, timestamped format will be
        used to produce filename, e.g.: ``Sun Jun 28 20-30-57 2020_output.graphml``

        """
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
        """
        Method to set attributes for XML element

        **Parameters**

        * ``element`` (object) xml etree element object to set attributes for
        * ``attributes`` (dict) dictionary of yEd graphml tag names and attributes

        Attributes dictionary keys will be used as xml tag names and values
        dictionary will be used as xml tag attributes, example::

            {
                "LineStyle": {"color": "#00FF00", "width": "1.0"},
                "EdgeLabel": {"textColor": "#00FF00"},
            }

        """
        children = list(element)
        for tag, attribs in attributes.items():
            tag_exists = False
            for child in children:
                if tag in child.tag:
                    child.attrib.update(attribs)
                    tag_exists = True
            if tag_exists == False:  # create tag element:
                tag_elem = ET.fromstring(
                    '<y:{} xmlns:y="http://www.yworks.com/xml/graphml"/>'.format(tag)
                )
                tag_elem.attrib.update(attribs)
                element.append(tag_elem)

    def update_node(
        self,
        id,
        label=None,
        top_label=None,
        bottom_label=None,
        attributes={},
        description=None,
        width="",
        height="",
    ):
        """
        Method to update node details

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier, usually equal to node name
        * ``label`` (str) label at the center of the shape node or above SVG node
        * ``top_label`` (str) label displayed at the top of the node
        * ``bottom_label`` (str) label displayed at the bottom of the node
        * ``description`` (str) string to save as node ``description`` attribute
        * ``width`` (int) node width in pixels
        * ``height`` (int) node height in pixels
        * ``attributes`` (dict) dictionary of yEd graphml tag names and attributes

        Attributes dictionary keys will be used as xml tag names and values
        dictionary will be used as xml tag attributes, example::

            {
                'Shape'     : {'type': 'roundrectangle'},
                'DropShadow': { 'color': '#B3A691', 'offsetX': '5', 'offsetY': '5'}
            }

        This method will replace existing and add new labels to the node.

        Existing description attribute will be replaced with new value.

        Height and width will override existing values.

        Attributes will replace existing values.

        """
        # get node element:
        node = self.graph_root.find(
            "./_default_ns_:node[@id='{}']".format(self.nodes_ids.get(id, id)),
            self.namespaces,
        )
        if node is None:
            log.error(
                "update_node, cannot find node with id - {}".format(
                    self.nodes_ids.get(id, id)
                )
            )
            return
        labels = {"c": label, "n": label, "t": top_label, "b": bottom_label}
        # try to find shapenode element
        node_elem = node.find("./_default_ns_:data/y:ShapeNode", self.namespaces)
        # try to find svgnode element
        if node_elem is None:
            node_elem = node.find("./_default_ns_:data/y:SVGNode", self.namespaces)
            labels = {"n": label}
        if node_elem is None:
            log.error(
                "Failed to find ShapeNode or SVGNode for node with id: '{}'".format(
                    self.nodes_ids.get(id, id)
                )
            )
            return
        # update attributes, update description if it does not exists
        self.set_attributes(node_elem, attributes)
        if description:
            description_elem = node_elem.find(
                ".//y:data[@key='{}']".format(self.y_attr["node"]["description"]),
                self.namespaces,
            )
            if not description_elem:
                node_elem.append(
                    self._create_data_element(
                        id=self.y_attr["node"]["description"], text=description
                    )
                )
            else:
                description_elem.text = description
        # iterate over existing labels
        for label_elem in node_elem.iterfind(".//y:NodeLabel", self.namespaces):
            position = label_elem.attrib.get("modelPosition")
            if not labels.get(position) is None:
                label_elem.text = labels.pop(position)
        # add new labels
        for label_position, label in labels.items():
            if label is None:
                continue
            node_elem.append(
                self._create_label_element(
                    self.node_label_xml, label, modelPosition=label_position
                )
            )
        # set width and height
        node_geometry_element = node.find(".//*/y:Geometry", self.namespaces)
        if width:
            node_geometry_element.set("width", str(width))
        if height:
            node_geometry_element.set("height", str(height))

    def update_link(
        self,
        edge_id="",
        label="",
        src_label="",
        trgt_label="",
        source="",
        target="",
        new_label=None,
        new_src_label=None,
        new_trgt_label=None,
        description="",
        attributes={},
    ):
        """
        Method to update edge/link details.

        **Parameters**

        * ``edge_id`` (str) md5 hash edge id, if not provided, will be generated
          based on edge attributes
        * ``label`` (str) existing edge label
        * ``src_label`` (str) existing edge src_label
        * ``trgt_label`` (str) existing edge tgt_label
        * ``source`` (str) existing edge source node ID
        * ``target`` (str) existing edge target node id
        * ``new_label`` (str) new edge label
        * ``new_src_label`` (str) new edge src_label
        * ``new_trgt_label`` (str) new edge tgt_label
        * ``description`` (str) new edge description
        * ``attributes`` (str) dictionary of attributes to apply to edge element

        Either of these must be provided to find edge element to update:

        * ``edge_id`` MD5 hash or
        * ``label, src_label, trgt_label, source, target`` attributes to calculate ``edge_id``

        ``edge_id`` calculated based on - ``label, src_label, trgt_label, source, target`` -
        attributes following this algorithm:

        1. Edge tuple produced: ``tuple(sorted([label, src_label, trgt_label, source, target]))``
        2. MD5 hash derived from tuple: ``hashlib.md5(",".join(edge_tup).encode()).hexdigest()``

        This method will replace existing and add new labels to the link.

        Existing description attribute will be replaced with new value.

        Attributes will replace existing values.

        """
        # make new labels equal to existing labels if new label not provided
        new_label = new_label if new_label != None else label
        new_src_label = new_src_label if new_src_label != None else src_label
        new_trgt_label = new_trgt_label if new_trgt_label != None else trgt_label
        # generate existing and new edge ID
        edge_tup = tuple(sorted([label, src_label, trgt_label, source, target]))
        new_edge_tup = tuple(
            sorted([new_label, new_src_label, new_trgt_label, source, target])
        )
        edge_id = (
            hashlib.md5(",".join(edge_tup).encode()).hexdigest()
            if not edge_id
            else edge_id
        )
        new_edge_id = (
            hashlib.md5(",".join(new_edge_tup).encode()).hexdigest()
            if not edge_id
            else edge_id
        )
        if edge_id in self.edges_ids:
            self.edges_ids.update({new_edge_id: self.edges_ids.pop(edge_id)})
        elif edge_id:
            self.edges_ids[edge_id] = edge_id
        # find edge element
        edge = self.graph_root.find(
            './_default_ns_:edge[@id="{}"]'.format(
                self.edges_ids.get(edge_id, edge_id)
            ),
            namespaces=self.namespaces,
        )
        PolyLineEdge = edge.find("./_default_ns_:data/y:PolyLineEdge", self.namespaces)
        # update edge id
        edge.attrib["id"] = self.edges_ids[new_edge_id]
        # update description
        if description:
            description_elem = edge.find(
                ".//y:data[@key='{}']".format(self.y_attr["edge"]["description"]),
                self.namespaces,
            )
            if description_elem is None:
                edge.append(
                    self._create_data_element(
                        id=self.y_attr["edge"]["description"], text=description
                    )
                )
            else:
                description_elem.text = description
        # update labels
        labels = {
            "center": new_label,
            "source": new_src_label,
            "target": new_trgt_label,
        }
        # iterate over existing labels
        for label_elem in PolyLineEdge.iterfind(".//y:EdgeLabel", self.namespaces):
            label_placement_elem = label_elem.find(
                ".//y:PreferredPlacementDescriptor", self.namespaces
            )
            if not label_placement_elem is None:
                position = label_placement_elem.get("placement")
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
        missing_links={  # dict, attributes to apply to missing edges
            "LineStyle": {"color": "#C0C0C0", "width": "1.0"},
            "EdgeLabel": {"textColor": "#C0C0C0"},
        },
        new_links={  # dict, attributes to apply to new edges
            "LineStyle": {"color": "#00FF00", "width": "1.0"},
            "EdgeLabel": {"textColor": "#00FF00"},
        },
    ):
        """
        Method to combine two graphs - existing and new - and produce resulting
        graph following these rules:

        * nodes and links present in new graph but not in existing graph considered
          as new and will be updated with ``new_nodes`` and ``new_links`` attributes by
          default highlighting them in green
        * nodes and links missing from new graph but present in existing graph considered
          as missing and will be updated with ``missing_nodes`` and ``missing_links`` attributes
          by default highlighting them in gray
        * nodes and links present in both graphs will remain unchanged

        **Parameters**

        * ``data`` (dict) dictionary containing new graph data, dictionary format should be
          the same as for ``from_dict`` method.
        * ``missing_nodes`` (dict) dictionary with attributes to apply to missing nodes
        * ``new_nodes`` (dict) dictionary with attributes to apply to new nodes
        * ``missing_links`` (dict) dictionary with attributes to apply to missing links
        * ``new_links`` (dict) dictionary with attributes to apply to new links

        **Sample usage**::

            from N2G import yed_diagram
            diagram = yed_diagram()
            new_graph = {
                'nodes': [
                    {'id': 'a', 'pic': 'router_round', 'label': 'R1' }
                ],
                'edges': [
                    {'source': 'f', 'src_label': 'Gig0/21', 'label': 'DF', 'target': 'b'}
                ]
            }
            diagram.from_file("./old_graph.graphml")
            diagram.compare(new_graph)
            diagram.dump_file(filename="compared_graph.graphml")


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
                    # find edges connected to missing nodes
                    for edge in self.graph_root.iterfind(
                        "./_default_ns_:edge[@source='{}']".format(id), self.namespaces
                    ):
                        self.update_link(
                            edge_id=edge.get("id"), attributes=missing_links
                        )
                    for edge in self.graph_root.iterfind(
                        "./_default_ns_:edge[@source='{}']".format(
                            self.nodes_ids.get(id, "")
                        ),
                        self.namespaces,
                    ):
                        self.update_link(
                            edge_id=edge.get("id"), attributes=missing_links
                        )
                    for edge in self.graph_root.iterfind(
                        "./_default_ns_:edge[@target='{}']".format(id), self.namespaces
                    ):
                        self.update_link(
                            edge_id=edge.get("id"), attributes=missing_links
                        )
                    for edge in self.graph_root.iterfind(
                        "./_default_ns_:edge[@target='{}']".format(
                            self.nodes_ids.get(id, "")
                        ),
                        self.namespaces,
                    ):
                        self.update_link(
                            edge_id=edge.get("id"), attributes=missing_links
                        )
            # find new edges:
            existing_edges = []
            new_links_list = []
            # combine all edges under "links" key
            data.setdefault("links", [])
            data["links"] += data.pop("edges") if data.get("edges") else []
            for edge in data["links"]:
                edge.setdefault("attributes", {})
                # create edge id
                edge_tup = tuple(
                    sorted(
                        [
                            edge["source"],
                            edge["target"],
                            edge.get("label", ""),
                            edge.get("src_label", ""),
                            edge.get("trgt_label", ""),
                        ]
                    )
                )
                edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
                # add new edge
                if not edge_id in self.edges_ids:
                    edge["attributes"].update(new_links)
                    self.add_link(**edge)
                    new_links_list.append(edge_id)
                else:
                    existing_edges.append(edge_id)
            # find missing edges:
            for id in self.edges_ids.keys():
                if not id in existing_edges and not id in new_links_list:
                    self.update_link(edge_id=id, attributes=missing_links)

    def layout(self, algo="kk", width=1360, height=864, **kwargs):
        """
        Method to calculate graph layout using Python
        `igraph <https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms>`_
        library

        **Parameters**

        * ``algo`` (str) name of layout algorithm to use, default is 'kk'. Reference
          `Layout algorithms` table below for valid algo names
        * ``width`` (int) width in pixels to fit layout in
        * ``height`` (int) height in pixels to fit layout in
        * ``kwargs`` any additional kwargs to pass to igraph ``Graph.layout`` method

        **Layout algorithms**

        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | algo name                       |    description                                                                                                 |
        +=================================+================================================================================================================+
        | circle, circular                | Deterministic layout that places the vertices on a circle                                                      |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | drl                             | The Distributed Recursive Layout algorithm for large graphs                                                    |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | fr                              | Fruchterman-Reingold force-directed algorithm                                                                  |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | fr3d, fr_3d                     | Fruchterman-Reingold force-directed algorithm in three dimensions                                              |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | grid_fr                         | Fruchterman-Reingold force-directed algorithm with grid heuristics for large graphs                            |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | kk                              | Kamada-Kawai force-directed algorithm                                                                          |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | kk3d, kk_3d                     | Kamada-Kawai force-directed algorithm in three dimensions                                                      |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | large, lgl, large_graph         | The Large Graph Layout algorithm for large graphs                                                              |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | random                          | Places the vertices completely randomly                                                                        |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | random_3d                       | Places the vertices completely randomly in 3D                                                                  |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | rt, tree                        | Reingold-Tilford tree layout, useful for (almost) tree-like graphs                                             |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | rt_circular, tree               | Reingold-Tilford tree layout with a polar coordinate post-transformation, useful for (almost) tree-like graphs |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        | sphere, spherical, circular_3d  | Deterministic layout that places the vertices evenly on the surface of a sphere                                |
        +---------------------------------+----------------------------------------------------------------------------------------------------------------+
        """
        try:
            from igraph import Graph as ig
        except ImportError:
            raise SystemExit(
                "Failed to import igraph, install - pip install python-igraph"
            )
        igraph_graph = ig()
        # iterate over diagrams and layout elements
        nodes_iterator = self.graph_root.iterfind(
            "./_default_ns_:node", self.namespaces
        )
        links_iterator = self.graph_root.iterfind(
            "./_default_ns_:edge", self.namespaces
        )
        # populate igraph with nodes
        for item in nodes_iterator:
            igraph_graph.add_vertex(name=item.attrib["id"])
        # populate igraph with edges
        for item in links_iterator:
            igraph_graph.add_edge(
                source=item.attrib["source"], target=item.attrib["target"]
            )
        # calculate layout
        layout = igraph_graph.layout(layout=algo, **kwargs)
        # scale layout to diagram size
        layout.fit_into(bbox=(width, height))
        # add coordinates from layout to diagram nodes
        for index, coord_item in enumerate(layout.coords):
            x_coord, y_coord = coord_item
            node_id = igraph_graph.vs[index].attributes()["name"]
            node = self.graph_root.find(
                "./_default_ns_:node[@id='{}']".format(node_id), self.namespaces
            )
            node_geometry_element = node.find(".//*/y:Geometry", self.namespaces)
            node_geometry_element.set("x", str(round(x_coord)))
            node_geometry_element.set("y", str(round(y_coord)))

    def delete_node(self, id=None, ids=[]):
        """
        Method to delete node by its id. Bulk delete operation
        supported by providing list of node ids to delete.

        **Parameters**

        * ``id`` (str) id of single node to delete
        * ``ids`` (list) list of node ids to delete

        """
        ids = ids + [id] if id else ids
        for node_id in ids:
            node_id_to_pop = str(node_id)
            # try to find using provided id
            node = self.graph_root.find(
                "./_default_ns_:node[@id='{}']".format(node_id), self.namespaces
            )
            if node is None:
                # try to find using yed generated id
                node_id = self.nodes_ids.get(node_id, "")
                node = self.graph_root.find(
                    "./_default_ns_:node[@id='{}']".format(node_id), self.namespaces
                )
            if not node is None:
                self.graph_root.remove(node)
                self.nodes_ids.pop(node_id_to_pop)
                # delete edges
                for edge in self.graph_root.iterfind(
                    "./_default_ns_:edge[@source='{}']".format(node_id), self.namespaces
                ):
                    edge_id_to_pop = edge.get("id", "")
                    if not edge_id_to_pop in self.edges_ids:
                        edge_id_to_pop = None
                        # need to iterate over edges_ids values to find respective key to pop
                        for k, v in self.edges_ids.items():
                            if v == edge.get("id"):
                                edge_id_to_pop = k
                                break
                    if edge_id_to_pop:
                        self.edges_ids.pop(edge_id_to_pop)
                    self.graph_root.remove(edge)
                for edge in self.graph_root.iterfind(
                    "./_default_ns_:edge[@target='{}']".format(node_id), self.namespaces
                ):
                    edge_id_to_pop = edge.get("id", "")
                    if not edge_id_to_pop in self.edges_ids:
                        edge_id_to_pop = None
                        # need to iterate over edges_ids values to find respective key to pop
                        for k, v in self.edges_ids.items():
                            if v == edge.get("id"):
                                edge_id_to_pop = k
                                break
                    if edge_id_to_pop:
                        self.edges_ids.pop(edge_id_to_pop)
                    self.graph_root.remove(edge)

    def delete_link(
        self,
        id=None,
        ids=[],
        label="",
        src_label="",
        trgt_label="",
        source="",
        target="",
    ):
        """
        Method to delete link by its id. Bulk delete operation
        supported by providing list of link ids to delete.

        If link ``id`` or ``ids`` not provided, id calculated based on - ``label, src_label,
        trgt_label, source, target`` - attributes using this algorithm:

        1. Edge tuple produced: ``tuple(sorted([label, src_label, trgt_label, source, target]))``
        2. MD5 hash derived from tuple: ``hashlib.md5(",".join(edge_tup).encode()).hexdigest()``

        **Parameters**

        * ``id`` (str) id of single link to delete
        * ``ids`` (list) list of link ids to delete
        * ``label`` (str) link label to calculate id of single link to delete
        * ``src_label`` (str) link source label to calculate id of single link to delete
        * ``trgt_label`` (str) link target label to calculate id of single link to delete
        * ``source`` (str) link source to calculate id of single link to delete
        * ``target`` (str) link target to calculate id of single link to delete

        """
        if not id and not ids:
            # create edge id
            edge_tup = tuple(sorted([source, target, label, src_label, trgt_label]))
            ids.append(hashlib.md5(",".join(edge_tup).encode()).hexdigest())
        else:
            ids = ids + [id] if id else ids
        for edge_id in ids:
            edge_id_to_pop = str(edge_id)
            edge = self.graph_root.find(
                "./_default_ns_:edge[@id='{}']".format(edge_id), self.namespaces
            )
            if edge is None:
                # try to find using yed generated id
                edge_id = self.edges_ids.get(edge_id, "")
                edge = self.graph_root.find(
                    "./_default_ns_:edge[@id='{}']".format(edge_id), self.namespaces
                )
            if not edge is None:
                self.graph_root.remove(edge)
                # pop edge id from edges_ids dict
                if not edge_id_to_pop in self.edges_ids:
                    edge_id_to_pop = None
                    # need to iterate over edges_ids values to find respective key to pop
                    for k, v in self.edges_ids.items():
                        if v == edge_id:
                            edge_id_to_pop = k
                            break
                if edge_id_to_pop:
                    self.edges_ids.pop(edge_id_to_pop)

    def _find_node(
        self,
        id=None,
        label=None,
        top_label=None,
        bottom_label=None,
        description=None,
        url=None,
        match_method="exact",
    ):
        """
        NOT IMPLEMENTED

        Method  to take node attributes and return list of matched node IDs
        """
        pass

    def _find_link(
        self,
        edge_id=None,
        label=None,
        src_label=None,
        trgt_label=None,
        source=None,
        target=None,
        description=None,
        match_method="exact",
    ):
        """
        NOT IMPLEMENTED

        Method  to take node attributes and return list of matched node IDs
        """
        pass
