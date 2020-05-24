import xml.etree.ElementTree as ET
import uuid

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
    <diagram id="{id}" name="{diagram_name}">
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
      <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="200" y="150" width="120" height="60" as="geometry"/>
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

    def __init__(self):
        self.drawing = ET.fromstring(self.drawio_drawing_xml)

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

    def add_diagram(self, diagram_name, width=1360, height=864):
        id = str(uuid.uuid1())
        diagram = ET.fromstring(
            self.drawio_diagram_xml.format(
                id=id, diagram_name=diagram_name, width=width, height=height
            )
        )
        self.drawing.append(diagram)
        self.go_to_diagram(diagram_name)

    def add_data_or_url(self, element, data, link):
        # add data if any
        attribs = {k: str(v) for k, v in data.items()}
        # add URL link if any
        if link:
            # check if link is another diagram name
            diagram_link = self.drawing.find("./diagram[@name='{}']".format(link))
            if diagram_link is not None:
                link = "data:page/id,{diagram_id}".format(
                    diagram_id=diagram_link.attrib["id"]
                )
            attribs["link"] = link
        element.attrib.update(attribs)
        return element

    def add_node(self, id="", data={}, url=""):
        node = ET.fromstring(
            self.drawio_node_object_xml.format(
                id=str(uuid.uuid1()), 
                label=id
            )
        )
        node = self.add_data_or_url(node, data, url)
        self.current_root.append(node)

    def add_link(self, source, target, label="", data={}, url=""):
        # search node object with given name
        source_node = self.current_root.find(
            "./object[@label='{}']".format(source)
        )
        target_node = self.current_root.find(
            "./object[@label='{}']".format(target)
        )
        # run checks
        if source_node is None:
            log.error("add_link: no source node '{}' found".format(source))
            return
        if target_node is None:
            log.error("add_link: no target node '{}' found".format(target))
            return
        link = ET.fromstring(
            self.drawio_link_object_xml.format(
                id=str(uuid.uuid1()),
                label=label,
                source_id=source_node.get("id"),
                target_id=target_node.get("id"),
            )
        )
        link = self.add_data_or_url(link, data, url)
        self.current_root.append(link)

    def dump_xml(self):
        ret = ET.tostring(self.drawing)  # return bytes string
        return ret.decode(encoding="utf-8")  # return decoded string

    def dump_file(self, filename=None, folder="./Output/"):
        import os
        import time

        # check output folder, if not exists, create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        # create file name
        if not filename:
            ctime = time.ctime().replace(":", "-")
            filename = "{}_output.xml".format(ctime)
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

    def from_file(self, filename):
        with open(filename, "r") as f:
            self.drawing = ET.fromstring(f.read())
        self.go_to_diagram(diagram_index=0)

    def from_dict(self, data, diagram_name="Page-1", width=1360, height=864):
        self.add_diagram(diagram_name, width, height)
        for node in data.get("nodes", []):
            self.add_node(**node)
        for link in data.get("links", []):
            self.add_link(**link)
        for edge in data.get("edges", []):
            self.add_link(**edge)

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
