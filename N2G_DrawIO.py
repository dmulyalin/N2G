import xml.etree.ElementTree as ET
import os
import hashlib
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


class drawio_diagram:

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
      <mxCell style="endArrow=none;" edge="1" parent="1" source="{source_id}" target="{target_id}">
          <mxGeometry relative="1" as="geometry"/>
      </mxCell>
    </object>
    """

    def __init__(self, node_dublicates="skip", link_dublicates="skip"):
        self.drawing = ET.fromstring(self.drawio_drawing_xml)
        self.nodes_ids = {} # dictionary of {diagram_name: [node_id1, node_id2]}
        self.edges_ids = {} # dictionary of {diagram_name: [edge_id1, edge_id2]}
        self.node_dublicates = node_dublicates
        self.link_dublicates = link_dublicates
        self.current_diagram = None
        self.current_diagram_id = ""
        self.default_node_style = "rounded=1;whiteSpace=wrap;html=1;"

    def go_to_diagram(self, diagram_name=None, diagram_index=None):
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

    def add_diagram(self, id, name="", width=1360, height=864):
        if id in self.nodes_ids or id in self.edges_ids:
            return
        if not name.strip():
            name = id
        diagram = ET.fromstring(
            self.drawio_diagram_xml.format(
                id=id, name=name, width=width, height=height
            )
        )
        self.nodes_ids[id] = []
        self.edges_ids[id] = []
        self.drawing.append(diagram)
        self.go_to_diagram(diagram_name=name)

    def add_data_or_url(self, element, data, link):
        # add data if any
        attribs = {k: str(v) for k, v in data.items()}
        # add URL link if any
        if link.strip():
            # check if link is another diagram name
            diagram_link = self.drawing.find("./diagram[@name='{}']".format(link))
            if diagram_link is not None:
                link = "data:page/id,{diagram_id}".format(
                    diagram_id=diagram_link.attrib["id"]
                )
            attribs["link"] = link
        element.attrib.update(attribs)
        return element
        
    def _node_exists(self, id, **kwargs):       
        # check if node with given id already exists
        if id in self.nodes_ids[self.current_diagram_id]:
            if self.node_dublicates == "log":
                log.error("add_shape_node: node '{}' already added to graph".format(id))
            elif self.node_dublicates == "skip":
                pass
            elif self.node_dublicates == "update":
                self.update_node(id, **kwargs)
            return True
        else:
            return False

    def add_node(self, id, label="", data={}, url="", style="", width=120, height=60, x_pos=200, y_pos=150):
        if self._node_exists(id, label=label, data=data, url=url):
            return
        self.nodes_ids[self.current_diagram_id].append(id)
        if not label.strip():
            label = id
        # get style
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                mxCell_elem = node.find("./mxCell")
                mxCell_elem.attrib["style"] = style_file.read()
        elif style.strip():
            mxCell_elem = node.find("./mxCell")
            mxCell_elem.attrib["style"] = style 
        # create node element    
        node = ET.fromstring(
            self.drawio_node_object_xml.format(
                id=id, 
                label=label,
                width=width,
                height=height,
                x_pos=x_pos,
                y_pos=y_pos,
                style=style if style else self.default_node_style
            )
        )
        # add data attributes and/or url to node
        node = self.add_data_or_url(node, data, url)
        self.current_root.append(node)

    def update_node(self, id, label="", data={}, url="", style="", width="", height=""):
        node = self.current_root.find("./object[@id='{}']".format(id))
        # update dat and url attributes
        node = self.add_data_or_url(node, data, url)
        # update label
        if label.strip():
            node.attrib["label"] = label
        # update style
        mxCell_elem = node.find("./mxCell")
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                mxCell_elem.attrib["style"] = style_file.read()
        elif style.strip():
            mxCell_elem.attrib["style"] = style    
        # update size
        mxGeometry_elem = node.find("./mxCell/mxGeometry")
        if width:
            mxGeometry_elem.attrib["width"] = str(width)
        if height:
            mxGeometry_elem.attrib["height"] = str(height)              
        
    def _link_exists(self, id, edge_tup):
        """method, used to check dublicate edges 
        """
        # check if edge with given id already exists
        if id in self.edges_ids[self.current_diagram_id]:
            if self.link_dublicates == "log":
                log.error(
                    "_link_exists: edge '{}' already added to graph".format(
                        ",".join(edge_tup)
                    )
                )
            elif self.link_dublicates == "skip":
                pass
            return True
        self.edges_ids[self.current_diagram_id].append(id)
        
    def add_link(self, source, target, label="", data={}, url=""):    
        # check if target and source nodes exist, add it if not, 
        # self._node_exists method will update node
        # if self.node_dublicates set to update, by default its set to skip
        if not self._node_exists(source):
            self.add_node(source)
        if not self._node_exists(target):
            self.add_node(target)
        # create edge id
        edge_tup = tuple(sorted([label, source, target]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        if self._link_exists(edge_id, edge_tup):
            return
        # create link
        link = ET.fromstring(
            self.drawio_link_object_xml.format(
                id=edge_id,
                label=label,
                source_id=source,
                target_id=target,
            )
        )
        # add links data and url
        link = self.add_data_or_url(link, data, url)
        # save link to graph
        self.current_root.append(link)

    def dump_xml(self):
        ret = ET.tostring(self.drawing, encoding="unicode")
        return ret

    def dump_file(self, filename=None, folder="./Output/"):
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
        Ref:: https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms
        
        Layout algorithms
        algo name                       description
        circle, circular                Deterministic layout that places the vertices on a circle
        drl                             The Distributed Recursive Layout algorithm for large graphs
        fr                              Fruchterman-Reingold force-directed algorithm
        fr3d, fr_3d                     Fruchterman-Reingold force-directed algorithm in three dimensions
        grid_fr                         Fruchterman-Reingold force-directed algorithm with grid heuristics for large graphs
        kk                              Kamada-Kawai force-directed algorithm
        kk3d, kk_3d                     Kamada-Kawai force-directed algorithm in three dimensions
        large, lgl, large_graph         The Large Graph Layout algorithm for large graphs
        random                          Places the vertices completely randomly
        random_3d                       Places the vertices completely randomly in 3D
        rt, tree                        Reingold-Tilford tree layout, useful for (almost) tree-like graphs
        rt_circular, tree               Reingold-Tilford tree layout with a polar coordinate post-transformation, useful for (almost) tree-like graphs
        sphere, spherical, circular_3d  Deterministic layout that places the vertices evenly on the surface of a sphere
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
            for item in self.current_root.findall("./object"):
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
        self.add_diagram(diagram_name, width, height)
        for node in data.get("nodes", []):
            self.add_node(**node)
        for link in data.get("links", []):
            self.add_link(**link)
        for edge in data.get("edges", []):
            self.add_link(**edge)
            
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

    def compare(self, old, new):
        """
        Method to produce diagram based on comparison of 
        old and new diagrams following these rules:
            - missing - update old node/link to grey colour
            - new - add node/link to old but in grey colour
            - same - keep unchanged
        """
        pass
        # # load old diagram
        # self.from_file(old)
        # # load new diagram
        # with open(new, "r") as f:
        #     new_drawing = ET.fromstring(f.read())
        # # iterate over nodes in new diagram
        # for old_diagram in self.drawing.findall("./diagram"):
        #     new_diagram = new_drawing.find("./diagram[@name='{}']".format(diagram.attrib["name"]))
        #     if new_diagram is None:
        #         continue
        #     for new_object in new_diagram.findall("./mxGraphModel/root/object"):
        #         old_object = old_diagram.find("./mxGraphModel/root/object[@label='{}']".format(new_object.attrib.get("label", "_None_")))
        #         # check if same object was found in old diagram, add it if not
        #         if not old_object:
        #             # add edges, item[0] refernece to object's mxCell child tag
        #             if new_object[0].get("source") and new_object[0].get("target"):
        #                 source_label = old_diagram.find("./mxGraphModel/root/object[@label='{}']"
        #                 igraph_graph.add_vertex(name=new_object[0].get("source"))
        #                 igraph_graph.add_vertex(name=new_object[0].get("target"))
        #                 igraph_graph.add_edge(
        #                     source=new_object[0].get("source"), target=new_object[0].get("target")
        #                 )
        #             # add nodes
        #             else:
        #                 igraph_graph.add_vertex(name=new_object.get("id"))
