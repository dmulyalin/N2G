import xml.etree.ElementTree as ET
import os
import hashlib
import logging

# initiate logging
log = logging.getLogger(__name__)
LOG_LEVEL = "ERROR"
LOG_FILE = None


def logging_config(LOG_LEVEL, LOG_FILE):
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL.upper() in valid_log_levels:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [N2G_DRAWIO %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=LOG_LEVEL.upper(),
            filename=LOG_FILE,
            filemode="w",
        )


logging_config(LOG_LEVEL, LOG_FILE)


class drawio_diagram:
    """
    N2G DrawIO module allows to produce diagrams compatible with DrawIO XML format.

    **Parameters**

    * ``node_duplicates`` (str) can be of value skip, log, update
    * ``link_duplicates`` (str) can be of value skip, log, update

    """

    # XML string templates to create etree elements from:
    drawio_drawing_xml = """
    <mxfile type="device" compressed="false">
    </mxfile>
    """

    drawio_diagram_xml = """
    <diagram id="{id}" name="{name}">
      <mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="1">
        <root>
          <mxCell id="0"/>   
          <mxCell id="1" parent="0"/>
        </root>
      </mxGraphModel>
    </diagram>
    """

    drawio_node_object_xml = """
    <object id="{id}" label="{label}">
      <mxCell style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="{height}" as="geometry"/>
      </mxCell>
    </object>
    """

    drawio_link_object_xml = """
    <object id="{id}" label="{label}">
      <mxCell style="{style}" edge="1" parent="1" source="{source_id}" target="{target_id}">
          <mxGeometry relative="1" as="geometry"/>
      </mxCell>
    </object>
    """

    drawio_link_label_xml = """
    <mxCell id="{id}" value="{label}" style="{style};" vertex="1" connectable="0" parent="{parent_id}">
      <mxGeometry x="{x}" relative="{rel}" as="geometry">
        <mxPoint as="offset" />
      </mxGeometry>
    </mxCell>
    """

    def __init__(self, node_duplicates="skip", link_duplicates="skip"):
        self.drawing = ET.fromstring(self.drawio_drawing_xml)
        self.nodes_ids = {}  # dictionary of {diagram_name: [node_id1, node_id2]}
        self.edges_ids = {}  # dictionary of {diagram_name: [edge_id1, edge_id2]}
        self.node_duplicates = node_duplicates
        self.link_duplicates = link_duplicates
        self.current_diagram = None
        self.current_diagram_id = ""
        self.default_node_style = "rounded=1;whiteSpace=wrap;html=1;"
        self.default_link_style = "endArrow=none;"
        self.default_link_label_style = "labelBackgroundColor=#ffffff;"

    def add_diagram(self, id, name="", width=1360, height=864):
        """
        Method to add new diagram tab and switch to it.

        .. warning:: This method must be called to create at list one
          diagram tab to work with prior to nodes and links can be added
          to the drawing calling ``add_link`` or ``add_node`` methods.

        **Parameters**

        * ``id`` (str) id of the diagram, should be unique across other diagrams
        * ``name`` (str) tab name
        * ``width`` (int) width of diagram in pixels
        * ``height`` (int) height of diagram in pixels

        """
        if id in self.nodes_ids or id in self.edges_ids:
            return
        if not name.strip():
            name = id
        diagram = ET.fromstring(
            self.drawio_diagram_xml.format(id=id, name=name, width=width, height=height)
        )
        self.nodes_ids[id] = []
        self.edges_ids[id] = []
        self.drawing.append(diagram)
        self.go_to_diagram(diagram_name=name)

    def go_to_diagram(self, diagram_name=None, diagram_index=None):
        """
        DrawIO supports adding multiple diagram tabs within single document.
        This method allows to switch between diarams in different tabs. That
        way each tab can be updated separately.

        **Parameters**

        * ``diagram_name`` (str) name of diagram tab to switch to
        * ``diagram_index`` (int) index of diagram tab to switch to, will
          change to last tab if index is out of range. Index can be positive
          or negative number and follows Python list index behaviour. For
          instance, index equal to "-1" we go to last tab, "0" will go to
          first tab

        """
        if diagram_name != None:
            self.current_diagram = self.drawing.find(
                "./diagram[@name='{name}']".format(name=diagram_name)
            )
        elif diagram_index != None:
            try:
                self.current_diagram = self.drawing.findall("./diagram")[diagram_index]
            except IndexError:
                self.current_diagram = self.drawing.findall("./diagram")[-1]
        self.current_root = self.current_diagram.find("./mxGraphModel/root")
        self.current_diagram_id = self.current_diagram.attrib["id"]

    def _add_data_or_url(self, element, data, url):
        # add data if any
        attribs = {k: str(v) for k, v in data.items()}
        # add URL if any
        if url:
            # check if url is another diagram name
            diagram_link = self.drawing.find("./diagram[@name='{}']".format(url))
            if diagram_link is not None:
                url = "data:page/id,{diagram_id}".format(
                    diagram_id=diagram_link.attrib["id"]
                )
            attribs["link"] = url
        element.attrib.update(attribs)
        return element

    def _node_exists(self, id, **kwargs):
        # check if node with given id already exists
        if id in self.nodes_ids[self.current_diagram_id]:
            if self.node_duplicates == "log":
                log.error("add_shape_node: node '{}' already added to graph".format(id))
            elif self.node_duplicates == "skip":
                pass
            elif self.node_duplicates == "update":
                self.update_node(id, **kwargs)
            return True
        else:
            return False

    def add_node(
        self,
        id,
        label="",
        data={},
        url="",
        style="",
        width=120,
        height=60,
        x_pos=200,
        y_pos=150,
        **kwargs
    ):
        """
        Method to add node to the diagram.

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier, usually equal to node name
        * ``label`` (str) node label, if not provided, set equal to id
        * ``data`` (dict) dictionary of key value pairs to add as node data
        * ``url`` (str) url string to save as node ``url`` attribute
        * ``width`` (int) node width in pixels
        * ``height`` (int) node height in pixels
        * ``x_pos`` (int) node position on x axis
        * ``y_pos`` (int) node position on y axis
        * ``style`` (str) string containing DrawIO style parameters to apply to the node

        Sample DrawIO style string for the node::

            shape=mxgraph.cisco.misc.asr_1000_series;html=1;pointerEvents=1;
            dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;
            verticalLabelPosition=bottom;verticalAlign=top;align=center;
            outlineConnect=0;

        """
        node_data = {}
        if self._node_exists(id, label=label, data=data, url=url):
            return
        self.nodes_ids[self.current_diagram_id].append(id)
        if not label.strip():
            label = id
        # try to get style from file
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                style = style_file.read()
        # create node element
        node = ET.fromstring(
            self.drawio_node_object_xml.format(
                id=id,
                label=label,
                width=width if str(width).strip() else 120,
                height=height if str(height).strip() else 60,
                x_pos=x_pos,
                y_pos=y_pos,
                style=style if style else self.default_node_style,
            )
        )
        # add data attributes and/or url to node
        node_data.update(data)
        node_data.update(kwargs)
        node = self._add_data_or_url(node, node_data, url)
        self.current_root.append(node)

    def update_node(
        self, id, label=None, data={}, url=None, style="", width="", height="", **kwargs
    ):
        """
        Method to update node details. Uses node ``id`` to search for node to update

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier
        * ``label`` (str) label at the center of the node
        * ``data`` (dict) dictionary of data items to add to the node
        * ``width`` (int) node width in pixels
        * ``height`` (int) node height in pixels
        * ``url`` (str) url string to save as node `url` attribute
        * ``style`` (str) string containing DrawIO style parameters to apply to the node

        """
        node_data = {}
        node = self.current_root.find("./object[@id='{}']".format(id))
        # update data and url attributes
        node_data.update(data)
        node_data.update(kwargs)
        node = self._add_data_or_url(node, node_data, url)
        # update label
        if not label is None:
            node.attrib["label"] = label
        # update style
        mxCell_elem = node.find("./mxCell")
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                mxCell_elem.attrib["style"] = style_file.read()
        elif style:
            mxCell_elem.attrib["style"] = style
        # update size
        mxGeometry_elem = node.find("./mxCell/mxGeometry")
        if width:
            mxGeometry_elem.attrib["width"] = str(width)
        if height:
            mxGeometry_elem.attrib["height"] = str(height)

    def _link_exists(self, id, edge_tup):
        """method, used to check duplicate edges"""
        # check if edge with given id already exists
        if id in self.edges_ids[self.current_diagram_id]:
            if self.link_duplicates == "log":
                log.error(
                    "_link_exists: edge '{}' already added to graph".format(
                        ",".join(edge_tup)
                    )
                )
            elif self.link_duplicates == "skip":
                pass
            return True
        self.edges_ids[self.current_diagram_id].append(id)

    def add_link(
        self,
        source,
        target,
        style="",
        label="",
        data={},
        url="",
        src_label="",
        trgt_label="",
        src_label_style="",
        trgt_label_style="",
        link_id=None,
        **kwargs
    ):
        """
        Method to add link between nodes to the diagram.

        **Parameters**

        * ``source`` (str) mandatory, source node id
        * ``source`` (str) mandatory, target node id
        * ``label`` (str) link label to display at the centre of the link
        * ``data`` (dict) dictionary of key value pairs to add as link data
        * ``url`` (str) url string to save as link ``url`` attribute
        * ``style`` (str) string or OS path to text file with style to apply to the link
        * ``src_label`` (str) link label to display next to source node
        * ``trgt_label`` (str) link label to display next to target node
        * ``src_label_style`` (str) source label style string
        * ``trgt_label_style`` (str) target label style string
        * ``link_id`` (str or int) optional link id value, must be unique across all links

        Sample DrawIO style string for the link::

            endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;
            edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;
            endFill=0;strokeWidth=5;

        .. note:: If source or target nodes does not exists, they will be automatically
          created

        All labels are optional and substituted with empty values to calculate link id.
        """
        link_data = {}
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
        if not self._node_exists(target, **target_node_dict):
            self.add_node(id=target, **target_node_dict)
        # create link id if not given
        if link_id:
            link_id = "link_id:{}".format(link_id)
            edge_tup = link_id
        else:
            edge_tup = tuple(sorted([label, source, target, src_label, trgt_label]))
            link_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        if self._link_exists(link_id, edge_tup):
            return
        # try to get style from file
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                style = style_file.read()
        # create link
        link = ET.fromstring(
            self.drawio_link_object_xml.format(
                id=link_id,
                label=label,
                source_id=source,
                target_id=target,
                style=style or self.default_link_style,
            )
        )
        # add link source label
        if src_label:
            src_label_obj = ET.fromstring(
                self.drawio_link_label_xml.format(
                    id="{}-src".format(link_id),
                    label=src_label,
                    parent_id=link_id,
                    style=src_label_style or self.default_link_label_style,
                    x="-0.5",
                    rel="1",
                )
            )
            self.current_root.append(src_label_obj)
            kwargs["src_label"] = src_label
        # add link target label
        if trgt_label:
            trgt_label_obj = ET.fromstring(
                self.drawio_link_label_xml.format(
                    id="{}-trgt".format(link_id),
                    label=trgt_label,
                    parent_id=link_id,
                    style=trgt_label_style or self.default_link_label_style,
                    x="0.5",
                    rel="-1",
                )
            )
            self.current_root.append(trgt_label_obj)
            kwargs["trgt_label"] = trgt_label
        # add links data and url
        link_data.update(data)
        link_data.update(kwargs)
        link_data.update({"source": source, "target": target})
        link = self._add_data_or_url(link, link_data, url)
        # save link to graph
        self.current_root.append(link)

    def dump_xml(self):
        """
        Method to return current diagram XML text
        """
        ret = ET.tostring(self.drawing, encoding="unicode")
        return ret

    def dump_file(self, filename=None, folder="./Output/"):
        """
        Method to save current diagram in .drawio file.

        **Parameters**

        * ``filename`` (str) name of the file to save diagram into
        * ``folder`` (str) OS path to folder where to save diagram file

        If no ``filename`` provided, timestamped format will be
        used to produce filename, e.g.: ``Sun Jun 28 20-30-57 2020_output.drawio``

        """
        import time

        # check output folder, if not exists, create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        # create file name
        if not filename:
            ctime = time.ctime().replace(":", "-")
            filename = "{}_output.drawio".format(ctime)
        # save file to disk
        with open(folder + filename, "w") as outfile:
            outfile.write(self.dump_xml())

    def layout(self, algo="kk", **kwargs):
        """
        Method to calculate graph layout using Python
        `igraph <https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms>`_
        library

        **Parameters**

        * ``algo`` (str) name of layout algorithm to use, default is 'kk'. Reference
          `Layout algorithms` table below for valid algo names
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
        # iterate over diagrams and layout elements
        for diagram in self.drawing.findall("./diagram"):
            igraph_graph = ig()
            self.go_to_diagram(diagram.attrib["name"])
            # populate igraph with nodes and edges from object tags
            for item in self.current_root.iterfind("./object"):
                # add edges, item[0] refernece to object's mxCell child tag
                if item[0].get("source") and item[0].get("target"):
                    igraph_graph.add_vertex(name=item[0].get("source"))
                    igraph_graph.add_vertex(name=item[0].get("target"))
                    igraph_graph.add_edge(
                        source=item[0].get("source"), target=item[0].get("target")
                    )
                # add nodes
                else:
                    igraph_graph.add_vertex(name=item.get("id"))
            # calculate layout
            layout = igraph_graph.layout(layout=algo, **kwargs)
            # scale layout to diagram size
            w = int(self.current_diagram.find("./mxGraphModel").attrib["dx"])
            h = int(self.current_diagram.find("./mxGraphModel").attrib["dy"])
            layout.fit_into(bbox=(w, h))
            # add coordinates from layout to diagram nodes
            for index, coord_item in enumerate(layout.coords):
                x_coord, y_coord = coord_item
                node_id = igraph_graph.vs[index].attributes()["name"]
                node_geometry_element = self.current_root.find(
                    "./object[@id='{id}']/mxCell/mxGeometry".format(id=node_id)
                )
                node_geometry_element.set("x", str(round(x_coord)))
                node_geometry_element.set("y", str(round(y_coord)))

    def from_dict(self, data, diagram_name="Page-1", width=1360, height=864):
        """
        Method to build graph from dictionary.

        **Parameters**

        * ``diagram_name`` (str) name of the diagram tab where to add links and nodes.
          Diagram tab will be created if it does not exists
        * ``width`` (int) diagram width in pixels
        * ``height`` (int) diagram height in pixels
        * ``data`` (dict) dictionary with nodes and link/edges details, example::

            sample_graph = {
                'nodes': [
                    {
                        'id': 'a',
                        'label': 'R1'
                    },
                    {
                        'id': 'b',
                        'label': 'somelabel',
                        'data': {'description': 'some node description'}
                    },
                    {
                        'id': 'e',
                        'label': 'E'
                    }
                ],
                'edges': [
                    {
                        'source': 'a',
                        'label': 'DF',
                        'src_label': 'Gi1/1',
                        'trgt_label': 'Gi2/2',
                        'target': 'b',
                        'url': 'google.com'
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
        self.add_diagram(id=diagram_name, width=width, height=height)
        [self.add_node(**node) for node in data.get("nodes", [])]
        # add links
        for link in data.get("links", []):
            link["source"] = link["source"].replace("\n", "&lt;br&gt;")
            link["target"] = link["target"].replace("\n", "&lt;br&gt;")
            link["label"] = link.get("label", "").replace("\n", "&#xa;")
            link["src_label"] = link.get("src_label", "").replace("\n", "&#xa;")
            link["trgt_label"] = link.get("trgt_label", "").replace("\n", "&#xa;")
            self.add_link(**link)
        # add links
        [self.add_link(**edge) for edge in data.get("edges", [])]

    def from_list(self, data, diagram_name="Page-1", width=1360, height=864):
        """
        Method to build graph from list.

        **Parameters**

        * ``diagram_name`` (str) name of the diagram tab where to add links and nodes.
          Diagram tab will be created if it does not exists
        * ``width`` (int) diagram width in pixels
        * ``height`` (int) diagram height in pixels
        * ``data`` (list) list of link dictionaries, example::

            sample_graph = [
                {
                    'source': 'a',
                    'label': 'DF',
                    'src_label': 'Gi1/1',
                    'trgt_label': 'Gi2/2',
                    'target': 'b',
                    'data': {'vlans': 'vlans_trunked: 1,2,3\\nstate: up'}
                },
                {
                    'source': 'a',
                    'target': {
                            'id': 'e',
                            'label': 'somelabel',
                            'data': {'description': 'some node description'}
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

            By default drawio_diagram object ``node_duplicates`` action set to 'skip' meaning that node will be added on first occurrence
            and ignored after that. Set ``node_duplicates`` to 'update' if node with given id need to be updated by
            later occurrences in the list.
        """
        self.add_diagram(id=diagram_name, width=width, height=height)
        [self.add_link(**edge) for edge in data]

    def from_file(self, filename, file_load="xml"):
        """
        Method to load nodes and links from Drawio diagram file for
        further processing

        **Args**

            * filename - OS path to .drawio file to load
        """
        with open(filename, "r") as f:
            if file_load == "xml":
                self.from_xml(f.read())

    def from_xml(self, text_data):
        """
        Method to load graph from .drawio XML text produced by DrawIO

        **Args**

            * text_data - text data to load
        """
        self.drawing = ET.fromstring(text_data)
        # extract diagrams, nodes, edges IDs
        for diagram_elem in self.drawing.findall("./diagram"):
            self.nodes_ids.setdefault(diagram_elem.attrib["id"], [])
            self.edges_ids.setdefault(diagram_elem.attrib["id"], [])
            # iterate over mxcells to extract nodes and edges
            for object in diagram_elem.findall("./mxGraphModel/root/object"):
                object_id = object.attrib["id"]
                mxCell = object.find("./mxCell")
                # check if this is the edge
                if "source" in mxCell.attrib and "target" in mxCell.attrib:
                    self.edges_ids[diagram_elem.attrib["id"]].append(object_id)
                else:
                    self.nodes_ids[diagram_elem.attrib["id"]].append(object_id)
        self.go_to_diagram(diagram_index=0)

    def from_csv(self, text_data):
        """
        Method to build graph from CSV tables

        **Parameters**

        * ``text_data`` (str) CSV text with links or nodes details

        This method supports loading CSV text data that contains nodes or links
        information. If ``id`` in headers, ``from_dict`` method will be called for CSV
        processing, ``from_list`` method will be used otherwise.

        CSV data with nodes details should have headers matching ``add_node`` method
        arguments and rules.

        CSV data with links details should have headers matching ``add_link`` method
        arguments and rules.

        Sample CSV table with links details::

            "source","label","target","src_label","trgt_label"
            "a","DF","b","Gi1/1","Gi2/2"
            "b","Copper","c","Te2/1",
            "b","Copper","e","","GE3"
            "d","FW","e",,

        Sample CSV table with nodes details::

            "id","label","style","width","height"
            a,"R1,2","./Pics/cisco_router.txt",78,53
            "b","some",,,
            "c","somelabel",,,
            "d","somelabel1",,,
            "e","R1",,,

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

    def update_link(
        self,
        edge_id="",
        label="",
        source="",
        target="",
        data={},
        url="",
        style="",
        src_label="",
        trgt_label="",
        new_label=None,
        new_src_label=None,
        new_trgt_label=None,
        src_label_style="",
        trgt_label_style="",
        **kwargs
    ):
        """
        Method to update edge/link details.

        **Parameters**

        * ``edge_id`` (str) - md5 hash edge id, if not provided, will be generated
          based on link attributes
        * ``label`` (str) - existing edge label
        * ``src_label`` (str) - existing edge source label
        * ``trgt_label`` (str) - existing edge target label
        * ``source`` (str) - existing edge source node id
        * ``target`` (str) - existing edge target node id
        * ``new_label`` (str) - new edge label
        * ``data`` (str) - edge new data attributes
        * ``url`` (str) - edge new url attribute
        * ``style`` (str) - OS path to file or sting containing style to apply to edge
        * ``new_src_label`` (str) - new edge source label`
        * ``new_trgt_label`` (str) - new edge target label
        * ``src_label_style`` (str) - string with style to apply to source label
        * ``trgt_label_style`` (str) - strung with style to apply to target label

        Either of these must be provided to find link element to update:

        * ``edge_id`` MD5 hash or
        * ``label, source, target, src_label, trgt_label`` existing link attributes to calculate ``edge_id``

        ``edge_id`` calculated based on - ``label, source, target, src_label, trgt_label`` -
        attributes following this algorithm:

        1. Edge tuple produced: ``tuple(sorted([label, source, target, src_label, trgt_label]))``
        2. MD5 hash derived from tuple: ``hashlib.md5(",".join(edge_tup).encode()).hexdigest()``

        If no ``label, src_label, trgt_label`` provided, they substituted with empty values in
        assumption that values for existing link are empty as well.

        This method will replace existing or add new labels to the link.

        Existing data attribute will be amended with new values using dictionary
        like update method.

        New style will replace existing style.
        """
        link_data = {}
        # get new label
        new_label = new_label if new_label != None else label
        new_src_label = new_src_label if new_src_label != None else src_label
        new_trgt_label = new_trgt_label if new_trgt_label != None else trgt_label
        # create edge id
        edge_tup = tuple(sorted([label, source, target, src_label, trgt_label]))
        new_edge_tup = tuple(
            sorted([new_label, source, target, new_src_label, new_trgt_label])
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
        # update edge id
        if edge_id in self.edges_ids[self.current_diagram_id]:
            self.edges_ids[self.current_diagram_id].remove(edge_id)
            self.edges_ids[self.current_diagram_id].append(new_edge_id)
        else:
            log.warning(
                "update_link, link does not exist - source '{}', target '{}', label '{}'".format(
                    source, target, label
                )
            )
            return
        # find edge element
        edge = self.current_root.find("./object[@id='{}']".format(edge_id))
        # update labels and id
        edge.attrib.update({"id": new_edge_id, "label": new_label})
        if new_src_label:
            src_label_obj = self.current_root.find(
                "./mxCell[@id='{}']".format("{}-src".format(edge_id))
            )
            if not src_label_obj is None:
                src_label_obj.attrib.update(
                    {
                        "id": "{}-src".format(new_edge_id),
                        "value": new_src_label,
                        "parent": new_edge_id,
                    }
                )
                if src_label_style:
                    src_label_obj.attrib["style"] = src_label_style
            # create new src_label
            else:
                src_label_obj = ET.fromstring(
                    self.drawio_link_label_xml.format(
                        id="{}-src".format(new_edge_id),
                        label=new_src_label,
                        parent_id=new_edge_id,
                        style=src_label_style or self.default_link_label_style,
                        x="-0.5",
                        rel="1",
                    )
                )
                self.current_root.append(src_label_obj)
            kwargs["src_label"] = new_src_label
        if new_trgt_label:
            trgt_label_obj = self.current_root.find(
                "./mxCell[@id='{}']".format("{}-trgt".format(edge_id))
            )
            if not trgt_label_obj is None:
                trgt_label_obj.attrib.update(
                    {
                        "id": "{}-trgt".format(new_edge_id),
                        "value": new_trgt_label,
                        "parent": new_edge_id,
                    }
                )
                if trgt_label_style:
                    trgt_label_obj.attrib["style"] = trgt_label_style
            else:
                trgt_label_obj = ET.fromstring(
                    self.drawio_link_label_xml.format(
                        id="{}-trgt".format(new_edge_id),
                        label=new_trgt_label,
                        parent_id=new_edge_id,
                        style=trgt_label_style or self.default_link_label_style,
                        x="0.5",
                        rel="-1",
                    )
                )
                self.current_root.append(trgt_label_obj)
            kwargs["trgt_label"] = new_trgt_label
        # replace edge data and url
        link_data.update(data)
        link_data.update(kwargs)
        edge = self._add_data_or_url(edge, link_data, url)
        # update style
        mxCell_elem = edge.find("./mxCell")
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                mxCell_elem.attrib["style"] = style_file.read()
        elif style.strip():
            mxCell_elem.attrib["style"] = style

    def compare(
        self, data, diagram_name=None, missing_colour="#C0C0C0", new_colour="#00FF00"
    ):
        """
        Method to combine two graphs - existing and new - and produce resulting
        graph following these rules:

        * nodes and links present in new graph but not in existing graph considered
          as new and will be updated with ``new_colour`` style attribute by
          default highlighting them in green
        * nodes and links missing from new graph but present in existing graph considered
          as missing and will be updated with ``missing_colour`` style attribute
          by default highlighting them in gray
        * nodes and links present in both graphs will remain unchanged

        **Parameters**

        * ``data`` (dict) dictionary containing new graph data, dictionary format should be
          the same as for ``from_dict`` method.
        * ``missing_colour`` (str) colour to apply to missing elements
        * ``new_colour`` (str) colour to apply to new elements

        **Sample usage**::

            from N2G import drawio_diagram
            existing_graph = {
                "nodes": [
                    {"id": "node-1"},
                    {"id": "node-2"},
                    {"id": "node-3"}
            ],
                "links": [
                    {"source": "node-1", "target": "node-2", "label": "bla1"},
                    {"source": "node-2", "target": "node-3", "label": "bla2"},
                ]
            }
            new_graph = {
                "nodes": [
                    {"id": "node-99"},
                    {"id": "node-100", "style": "./Pics/router_1.txt", "width": 78, "height": 53},
                ],
                "links": [
                    {"source": "node-2", "target": "node-3", "label": "bla2"},
                    {"source": "node-99", "target": "node-3", "label": "bla99"},
                    {"source": "node-100", "target": "node-99", "label": "bla10099"},
                ]
            }
            drawing = drawio_diagram()
            drawing.from_dict(data=existing_graph)
            drawing.compare(new_graph)
            drawing.layout(algo="kk")
            drawing.dump_file(filename="compared_graph.drawio")

        """
        if diagram_name:
            self.go_to_diagram(diagram_name=diagram_name)
        else:
            self.go_to_diagram(diagram_index=0)
        if isinstance(data, dict):
            all_new_data_ids = set()
            new_elements = []
            # combine all edges under "links" key
            data.setdefault("links", [])
            data["links"] += data.pop("edges") if data.get("edges") else []
            # find new node elements and add them to graph
            for node in data.get("nodes", []):
                all_new_data_ids.add(node["id"])
                if not node["id"] in self.nodes_ids[self.current_diagram_id]:
                    new_elements.append(node["id"])
                    # add new node
                    self.add_node(**node)
            # find new link elements and add them to graph
            for link in data["links"]:
                link_tup = tuple(
                    sorted(
                        [
                            link.get("label", ""),
                            link["source"],
                            link["target"],
                            link.get("src_label", ""),
                            link.get("trgt_label", ""),
                        ]
                    )
                )
                id = hashlib.md5(",".join(link_tup).encode()).hexdigest()
                all_new_data_ids.add(id)
                if not id in self.edges_ids[self.current_diagram_id]:
                    new_elements.append(id)
                    # add new link
                    self.add_link(**link)
            # update new elements style attribute
            for id in new_elements:
                mxCell = self.current_root.find("./object[@id='{}']/mxCell".format(id))
                # convert style string to dictionary
                style_dict = {
                    i.split("=")[0]: i.split("=")[1]
                    for i in mxCell.attrib["style"].split(";")
                    if "=" in i
                }
                # update style colors
                if "fillColor" in style_dict:
                    style_dict["fillColor"] = new_colour
                else:
                    style_dict["strokeColor"] = new_colour
                style_dict["fontColor"] = new_colour
                # recreate style string
                mxCell.attrib["style"] = ";".join(
                    ["{}={}".format(k, v) for k, v in style_dict.items()]
                )
            # get all elements IDs set
            all_elements_ids = set(
                self.nodes_ids[self.current_diagram_id]
                + self.edges_ids[self.current_diagram_id]
            )
            # iterate over missing elements and update color for them
            for id in all_elements_ids.difference(all_new_data_ids):
                mxCell = self.current_root.find("./object[@id='{}']/mxCell".format(id))
                # convert style string to dictionary
                style_dict = {
                    i.split("=")[0]: i.split("=")[1]
                    for i in mxCell.attrib["style"].split(";")
                    if "=" in i
                }
                # update style colors
                if "fillColor" in style_dict:
                    style_dict["fillColor"] = missing_colour
                else:
                    style_dict["strokeColor"] = missing_colour
                style_dict["fontColor"] = missing_colour
                # recreate style string
                mxCell.attrib["style"] = ";".join(
                    ["{}={}".format(k, v) for k, v in style_dict.items()]
                )

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
            node = self.current_root.find("./object[@id='{}']".format(node_id))
            if not node is None:
                self.current_root.remove(node)
                self.nodes_ids[self.current_diagram_id].remove(node_id)
                # remove edges:
                # below xpath selects all parents - '..' - of children that
                # has source or target equal to node id
                for edge in self.current_root.iterfind(
                    ".//mxCell[@source='{}']/..".format(node_id)
                ):
                    self.edges_ids[self.current_diagram_id].remove(edge.get("id"))
                    self.current_root.remove(edge)
                for edge in self.current_root.iterfind(
                    ".//mxCell[@target='{}']/..".format(node_id)
                ):
                    self.edges_ids[self.current_diagram_id].remove(edge.get("id"))
                    self.current_root.remove(edge)

    def delete_link(self, id=None, ids=[], label="", source="", target="", **kwargs):
        """
        Method to delete link by its id. Bulk delete operation
        supported by providing list of link ids to delete.

        If link ``id`` or ``ids`` not provided, id calculated based on - ``label,
        source, target`` - attributes using this algorithm:

        1. Edge tuple produced: ``tuple(sorted([label, source, target]))``
        2. MD5 hash derived from tuple: ``hashlib.md5(",".join(edge_tup).encode()).hexdigest()``

        **Parameters**

        * ``id`` (str) id of single link to delete
        * ``ids`` (list) list of link ids to delete
        * ``label`` (str) link label to calculate id of single link to delete
        * ``source`` (str) link source to calculate id of single link to delete
        * ``target`` (str) link target to calculate id of single link to delete

        """
        if not id and not ids:
            # create edge id
            src_label = kwargs.get("src_label", "")
            trgt_label = kwargs.get("trgt_label", "")
            edge_tup = tuple(sorted([source, target, label, src_label, trgt_label]))
            ids.append(hashlib.md5(",".join(edge_tup).encode()).hexdigest())
        else:
            ids = ids + [id] if id else ids
        for edge_id in ids:
            edge = self.current_root.find("./object[@id='{}']".format(edge_id))
            if not edge is None:
                self.current_root.remove(edge)
                self.edges_ids[self.current_diagram_id].remove(edge_id)
