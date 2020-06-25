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
      <mxCell style="{style}" edge="1" parent="1" source="{source_id}" target="{target_id}">
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
        self.default_link_style = "endArrow=none;"

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

    def add_data_or_url(self, element, data, url):
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
                style=style if style else self.default_node_style
            )
        )
        # add data attributes and/or url to node
        node = self.add_data_or_url(node, data, url)
        self.current_root.append(node)

    def update_node(self, id, label=None, data={}, url=None, style="", width="", height=""):
        node = self.current_root.find("./object[@id='{}']".format(id))
        # update data and url attributes
        node = self.add_data_or_url(node, data, url)
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
        
    def add_link(self, source, target, style="", label="", data={}, url=""):    
        # check type of source and target attribute
        source_node_dict = source.copy() if isinstance(source, dict) else {"id": source}
        source = source_node_dict.pop("id")
        target_node_dict = target.copy() if isinstance(target, dict) else {"id": target}
        target = target_node_dict.pop("id")
        # check if target and source nodes exist, add it if not, 
        # self._node_exists method will update node
        # if self.node_dublicates set to update, by default its set to skip
        if not self._node_exists(source, **source_node_dict):
            self.add_node(id=source, **source_node_dict)
        if not self._node_exists(target, **target_node_dict):
            self.add_node(id=target, **target_node_dict)
        # create edge id
        edge_tup = tuple(sorted([label, source, target]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        if self._link_exists(edge_id, edge_tup):
            return
        # try to get style from file
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                style = style_file.read()
        # create link
        link = ET.fromstring(
            self.drawio_link_object_xml.format(
                id=edge_id,
                label=label,
                source_id=source,
                target_id=target,
                style=style if style else self.default_link_style
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
        self.add_diagram(id=diagram_name, width=width, height=height)
        [self.add_node(**node) for node in data.get("nodes", [])]            
        [self.add_link(**link) for link in data.get("links", [])]
        [self.add_link(**edge) for edge in data.get("edges", [])]

    def from_list(self, data, diagram_name="Page-1", width=1360, height=864):
        self.add_diagram(id=diagram_name, width=width, height=height)
        [self.add_link(**edge) for edge in data]
            
    def from_file(self, filename, file_load="xml"):
        """
        Method to load nodes and links from yed graphml file.
        
        **Args**
        
            * filename - OS path to .graphml file to load
        """
        with open(filename, "r") as f:
            if file_load == "xml":
                self.from_xml(f.read())
            
    def from_xml(self, text_data):
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

    def from_csv(self, data):
        """
        Method to load graph from csv data
        
        **Args**
        
            * data - csv data with links or nodes details
        """
        # import libs
        from io import StringIO
        import csv
        # need to handle text data as file like object for csv reader to work
        iostring = StringIO(newline='')
        iostring.write(data)
        iostring.seek(0)
        # load csv data
        dict_reader = csv.DictReader(iostring)
        data_list = list(dict_reader)
        # if id given - meaning it is nodes data
        if data_list[0].get("id"):
            self.from_dict({"nodes": data_list})
        else:
            self.from_list(data_list)  
        
        
    def update_link(self, 
        edge_id="",
        label="", 
        source="", 
        target="", 
        new_label=None, 
        data={}, 
        url="",
        style=""
        ):
        """
        Method to update edge/link. Element to update looked up by ID. IT calculated based on
        label, src_label, trgt_label, source, target attributes.
        
        **Kwargs**
            * edge_id - md5 hash edge id, if not provided, will be generated based on existing labels
            * label - existing edge label
            * source - existing edge source node ID 
            * target - existing edge target node id 
            * new_label - new edge label 
            * data - edge new data attributes 
            * url - edge new url attribute     
            * style - OS path to file or sting containing edge style
        """
        # get new label
        new_label = new_label if new_label != None else label
        # create edge id
        edge_tup = tuple(sorted([label, source, target]))
        new_edge_tup = tuple(sorted([new_label, source, target]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest() if not edge_id else edge_id
        new_edge_id = hashlib.md5(",".join(new_edge_tup).encode()).hexdigest() if not edge_id else edge_id
        # update edge id
        if edge_id in self.edges_ids[self.current_diagram_id]:
            self.edges_ids[self.current_diagram_id].remove(edge_id)
            self.edges_ids[self.current_diagram_id].append(new_edge_id)
        else:
            log.warning("update_link, link does not exist - source '{}', target '{}', label '{}'".format(
                    source, target, label
                )
            )            
            return
        # find edge element
        edge = self.current_root.find("./object[@id='{}']".format(edge_id))
        # update label and id
        edge.attrib.update({
            "id": new_edge_id,
            "label": new_label
        })
        # replace edge data and url
        edge = self.add_data_or_url(edge, data, url)
        # update style
        mxCell_elem = edge.find("./mxCell")
        if os.path.isfile(style[:5000]):
            with open(style, "r") as style_file:
                mxCell_elem.attrib["style"] = style_file.read()
        elif style.strip():
            mxCell_elem.attrib["style"] = style 

    def compare(
        self, 
        data,
        diagram_name=None,
        missing_colour="#C0C0C0",
        new_colour="#00FF00"
    ):
        """method to compare data graph with self.drawing and produce resulting graph
        applying new styles
        """
        if diagram_name:
            self.go_to_diagram(diagram_name=diagram_name)
        else:
            self.go_to_diagram(diagram_index=0)
        if isinstance(data, dict):
            all_new_data_ids = set()
            new_elements = []
            # combine all edges under "links" key
            if data.get("links"):
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
                link_tup = tuple(sorted([link.get("label", ""), link["source"], link["target"]]))
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
                style_dict = {i.split("=")[0]: i.split("=")[1] for i in mxCell.attrib["style"].split(";") if i.strip()}
                # update style colors
                if "fillColor" in style_dict:
                    style_dict["fillColor"] = new_colour 
                else:
                    style_dict["strokeColor"] = new_colour          
                style_dict["fontColor"] = new_colour
                # recreate style string
                mxCell.attrib["style"] = ";".join(["{}={}".format(k,v) for k,v in style_dict.items()]) 
            # get all elements IDs set
            all_elements_ids = set(self.nodes_ids[self.current_diagram_id] + self.edges_ids[self.current_diagram_id])
            # iterate over missing elements and update color for them
            for id in all_elements_ids.difference(all_new_data_ids):
                mxCell = self.current_root.find("./object[@id='{}']/mxCell".format(id))
                # convert style string to dictionary
                style_dict = {i.split("=")[0]: i.split("=")[1] for i in mxCell.attrib["style"].split(";") if i.strip()}
                # update style colors
                if "fillColor" in style_dict:
                    style_dict["fillColor"] = missing_colour
                else:
                    style_dict["strokeColor"] = missing_colour                    
                style_dict["fontColor"] = missing_colour
                # recreate style string
                mxCell.attrib["style"] = ";".join(["{}={}".format(k,v) for k,v in style_dict.items()])