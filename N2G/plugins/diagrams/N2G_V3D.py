import hashlib
import os
import logging
import json

# initiate logging
log = logging.getLogger(__name__)


class v3d_diagramm:
    """
    Class to produce JSON data structure compatible with 
    `3D Force-Directed Graph <https://github.com/vasturiano/3d-force-graph>`_ 
    library `JSON input syntax <https://github.com/vasturiano/3d-force-graph#input-json-syntax>`_
    
    :param node_duplicates: (str) what to do with node duplicates - ``skip`` (default), ``update`` or ``log``
    :param link_duplicates: (str) what to do with link duplicates - ``skip`` (default), ``update`` or ``log``
    """

    def __init__(self, node_duplicates="skip", link_duplicates="skip"):
        self.drawing = {"nodes": [], "links": []}
        self.node_duplicates = node_duplicates
        self.link_duplicates = link_duplicates
        self.nodes_dict = {}
        self.links_dict = {}

    def _node_exists(self, id, **kwargs):
        # check if node with given id already exists
        if id in self.nodes_dict:
            if self.node_duplicates == "log":
                log.error("add_node: node '{}' already added to graph".format(id))
            elif self.node_duplicates == "skip":
                pass
            elif self.node_duplicates == "update":
                self.update_node(id=id, **kwargs)
            return True
        else:
            return False

    def _link_exists(self, id, **kwargs):
        """method, used to check duplicate edges"""
        # check if edge with given id already exists
        if id in self.links_dict:
            if self.link_duplicates == "log":
                log.error(
                    "_link_exists: '{}' edge already exists, data {}".format(id, kwargs)
                )
            elif self.link_duplicates == "skip":
                pass
            elif self.link_duplicates == "update":
                self.update_link(id=id, **kwargs)
            return True
        else:
            return False

    def add_node(
        self, id, label="", data=None, color="green", nodeResolution=8, **kwargs
    ):
        """
        Method to add node to the diagram.

        :param id: (str) mandatory, unique node identifier, usually equal to node name
        :param label: (str) node label, if not provided, set equal to id
        :param data: (dict) dictionary of key value pairs to add as node data
        :param fx: (int) node position on x axis
        :param fy: (int) node position on y axis
        :param fz: (int) node position on z axis
        :param color: (str) node color e.g. ``blue``, default is ``green``
        :param nodeResolution: (int) geometric resolution of the node, expressed in how 
          many slice segments to divide the circumference. Higher values yield smoother spheres.
        :param kwargs: (dict) any additional kwargs to add to node dictionary as per
          `node styling attributes <https://github.com/vasturiano/3d-force-graph#node-styling>`_
          such as ``nodeRelSize``, ``nodeOpacity``, ``nodeVal`` etc.
        """
        data = data or {}
        # process node
        if self._node_exists(id, label=label, data=data):
            return
        if not label.strip():
            label = id
        # create node element
        node = {
            "id": id,
            "label": label,
            "color": color,
            "nodeResolution": nodeResolution,
            "data": data,
            **kwargs,
        }
        # add node to nodes dictionary
        self.nodes_dict[id] = node

    def update_node(self, id, data=None, **kwargs):
        """
        Method to update node details. Uses node ``id`` to search for node to update

        :param id: (str) mandatory, unique node identifier
        :param data: (dict) data argument/key dictionary content to update existing values
        :param kwargs: (dict) any additional arguments to update node dictionary
        """
        data = data or {}
        node = self.nodes_dict.get(id)
        if not node:
            log.error("node_update: node {} not found".format(id))
            return

        # update node attributes
        node["data"].update(data)
        node.update(kwargs)

    def delete_node(self, id):
        """
        Method to delete node. Uses node ``id`` to search for node to delete.

        :param id: (str) mandatory, unique node identifier
        """
        _ = self.nodes_dict.pop(id, None)
        # delete all bound links
        for lid in list(self.links_dict.keys()):
            if (
                self.links_dict[lid]["source"] == id
                or self.links_dict[lid]["target"] == id
            ):
                _ = self.links_dict.pop(lid, None)

    def _make_edge_id(self, source, target, label="", src_label="", trgt_label=""):
        edge_tup = tuple(sorted([label, source, target, src_label, trgt_label]))
        return hashlib.md5(",".join(edge_tup).encode()).hexdigest()

    def add_link(
        self,
        source,
        target,
        label="",
        src_label="",
        trgt_label="",
        data=None,
        id=None,
        **kwargs
    ):
        """
        Method to add link between nodes.

        :param source: (str) mandatory, source node id
        :param source: (str) mandatory, target node id
        :param label: (str) link label to display at the center of the link
        :param data: (dict) dictionary of key value pairs to add as link data
        :param src_label: (str) link label to use next to source node
        :param trgt_label: (str) link label to use next to target node
        :param id: (str) explicit link identifier to use
        :param kwargs: (dict) any additional kwargs to add to link dictionary
        
        .. note:: If source or target nodes does not exists, they will be automatically
          created

        All labels are optional and substituted with empty values to calculate link id.
        
        By default V3D uses below code to produce MD5 hash digest for link id::
        
            link_tup = tuple(sorted([label, source, target, src_label, trgt_label]))
            link_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        """
        data = data or {}
        # check type of source and target attribute
        source_node_dict = source.copy() if isinstance(source, dict) else {"id": source}
        source = source_node_dict.pop("id")
        target_node_dict = target.copy() if isinstance(target, dict) else {"id": target}
        target = target_node_dict.pop("id")
        # check if target and source nodes exist, add it if not, self._node_exists method will update node
        # if self.node_duplicates set to update, by default its set to skip
        if not self._node_exists(source, **source_node_dict):
            self.add_node(id=source, **source_node_dict)
        if not self._node_exists(target, **target_node_dict):
            self.add_node(id=target, **target_node_dict)
        # create edge id
        edge_id = id or self._make_edge_id(source, target, label, src_label, trgt_label)
        if self._link_exists(
            id=edge_id,
            source=source,
            target=target,
            new_label=label,
            new_src_label=src_label,
            new_trgt_label=trgt_label,
            data=data,
            **kwargs
        ):
            return
        # create link
        link = {
            "id": edge_id,
            "label": label,
            "source": source,
            "target": target,
            "src_label": src_label,
            "trgt_label": trgt_label,
            "data": data,
            **kwargs,
        }
        # save link to graph
        self.links_dict[edge_id] = link

    def update_link(
        self,
        source=None,
        target=None,
        label="",
        src_label="",
        trgt_label="",
        new_label="",
        new_src_label="",
        new_trgt_label="",
        data=None,
        url="",
        id=None,
        **kwargs
    ):
        """
        Method to update link details. Uses link ``id`` to search for link to update, if no ``id`` 
        provided uses ``source, target, label, src_label, trgt_label`` to calculate edge id.
        
        :param source: (str) source node id
        :param target: (str) target node id
        :param label: (str) existing link label
        :param src_label: (str) existing link source label
        :param trgt_label: (str) existing link target label
        :param new_label: (str) new link label to replace existing label
        :param new_src_label: (str) new link source label to replace existing source label
        :param new_trgt_label: (str) new link target label to replace existing target label
        :param data: (dict) dictionary of key value pairs to update link data
        :param url: (str) url string to save as link ``url`` attribute
        :param id: (str) link identifier to find the link to update
        :param kwargs: (dict) any additional kwargs to update link dictionary
        """
        data = data or {}
        edge_id = id or self._make_edge_id(source, target, label, src_label, trgt_label)
        link = self.links_dict.get(edge_id)

        if not link:
            log.error("link_update: link {} not found".format(edge_id))
            return

        # update link attributes
        if data:
            link["data"].update(data)
        if url:
            link["url"] = url

        # update labels and edge_id
        if any([new_label, new_src_label, new_trgt_label]):
            link["label"] = new_label if new_label else link["label"]
            link["src_label"] = new_src_label if new_src_label else link["src_label"]
            link["trgt_label"] = (
                new_trgt_label if new_trgt_label else link["trgt_label"]
            )
            link["id"] = self._make_edge_id(
                source, target, link["label"], link["src_label"], link["trgt_label"]
            )

        # update remaining attributes
        link.update(kwargs)

    def delete_link(
        self, source=None, target=None, label="", src_label="", trgt_label="", id=None
    ):
        """
        Method to delete link. Uses link ``id`` to search for link to delete, if no ``id`` 
        provided uses ``source, target, label, src_label, trgt_label`` to calculate edge id.
        
        :param source: (str) source node id
        :param target: (str) target node id
        :param label: (str) existing link label
        :param src_label: (str) link source label
        :param trgt_label: (str) link target label
        :param id: (str) link identifier to find the link to delete
        """
        edge_id = id or self._make_edge_id(source, target, label, src_label, trgt_label)
        _ = self.links_dict.pop(edge_id, None)

    def layout(self, algo="kk3d", dx=100, dy=100, dz=100, **kwargs):
        """
        Method to calculate graph layout using Python
        `igraph <https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms>`_
        library

        :param algo: (str) name of igraph layout algorithm to use, default is 'kk3d'. Reference
          `Layout algorithms` table below for valid algo names
        :param kwargs: (dict) any additional kwargs to pass to igraph ``Graph.layout`` method

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
		
		.. note:: if 2d layout algorithm called, z axis coordinate set to 0
        """
        try:
            from igraph import Graph as ig
        except ImportError:
            raise SystemExit(
                "Failed to import igraph, install - pip install python-igraph"
            )
        igraph_graph = ig()
        # iterate over nodes
        for item in self.nodes_dict.values():
            igraph_graph.add_vertex(name=item["id"])
        # add edges
        for item in self.links_dict.values():
            igraph_graph.add_edge(source=item["source"], target=item["target"])
        # calculate layout
        layout = igraph_graph.layout(layout=algo, **kwargs)
        # scale layout to diagram size
        if "3d" in algo.lower().strip():
            layout.fit_into(bbox=(dx, dy, dz))
        else:
            layout.fit_into(bbox=(dx, dy))
        # add coordinates from layout to nodes
        for index, coord_item in enumerate(layout.coords):
            if "3d" in algo.lower().strip():
                x_coord, y_coord, z_coord = coord_item
            else:
                x_coord, y_coord, z_coord = (*coord_item, 0)
            node_id = igraph_graph.vs[index].attributes()["name"]
            node_element = self.nodes_dict[node_id]
            node_element["fx"] = round(x_coord)
            node_element["fy"] = round(y_coord)
            node_element["fz"] = round(z_coord)

    def from_dict(self, data):
        """
        Method to build graph from dictionary.

        :param data: (dict) dictionary with nodes and link/edges details
        
        Sample data dictionary::

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
        [self.add_node(**node) for node in data.get("nodes", [])]
        [self.add_link(**link) for link in data.get("links", [])]
        [self.add_link(**edge) for edge in data.get("edges", [])]

    def from_list(self, data):
        """
        Method to build graph from list.

        :param data: (list) list of link dictionaries
        
        Sample list data::

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

        .. note:: By default drawio_diagram object ``node_duplicates`` action set to 'skip' 
            meaning that node will be added on first occurrence and ignored after that. Set 
            ``node_duplicates`` to 'update' if node with given id need to be updated by later 
            occurrences in the list.
        """
        [self.add_link(**edge) for edge in data]

    def from_v3d_json(self, data):
        """
        Method to load `JSON input syntax <https://github.com/vasturiano/3d-force-graph#input-json-syntax>`_
        data into diagram plugin, presumably to perform various manipulations.
        
        :param data: (str) string of `JSON input syntax <https://github.com/vasturiano/3d-force-graph#input-json-syntax>`_ format
        """
        data_json = json.loads(data)

        # load nodes
        for node in data_json.get("nodes"):
            self.add_node(**node)

        # load links
        for link in data_json.get("links"):
            self.add_link(**link)

    def dump_dict(self):
        """
        Method to populate ``self.drawing`` dictionary with current links and nodes items,
        return ``self.drawing`` dictionary content after that.
        """
        self.drawing = {
            "nodes": list(self.nodes_dict.values()),
            "links": list(self.links_dict.values()),
        }
        return self.drawing

    def dump_json(self, **kwargs):
        """
        Method to transform graph data in a JSON formatted string.
        
        :param kwargs: (dict) kwargs to use with ``json.dumps`` method
        """
        gdict = self.dump_dict()
        return json.dumps(gdict, **kwargs)

    def dump_file(
        self,
        filename=None,
        folder="./Output/",
        json_kwargs={"sort_keys": True, "indent": 4},
    ):
        """
        Method to save current diagram to text file in a JSON format.

        :param filename: (str) name of the file to save diagram into
        :param folder: (str) OS path to folder where to save diagram file, default is ``./Output/``
        :param json_kwargs: (dict) kwargs to use with ``json.dumps`` method
        
        If no ``filename`` provided, timestamped format used to produce filename, 
        e.g.: ``Sun Jun 28 20-30-57 2020_output.txt``
        """
        import time

        # check output folder, if not exists, create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        # create file name
        if not filename:
            ctime = time.ctime().replace(":", "-")
            filename = "{}_output.txt".format(ctime)
        # save file to disk
        with open(folder + filename, "w") as outfile:
            outfile.write(self.dump_json(**json_kwargs))

    def run(self, ip="0.0.0.0", port=9000, dry_run=False):
        """
        Method to run FLASK web server using built-in browser app.
        
        :param ip: (str) IP address to bound WEB server to
        :param port: (int) port number to run WEB server on
        :dry_run: (bool) if True, do not start, return status info instead, 
          default is False
        """
        from flask import Flask, render_template_string, Markup
        from N2G.utils.V3D_web_server import graph_browser

        app = Flask(__name__)

        # based on https://stackoverflow.com/a/19269087/12300761 answer:
        app.jinja_env.filters["json"] = lambda v: Markup(json.dumps(v))

        @app.route("/")
        def home():
            return render_template_string(graph_browser, json_data=self.dump_json())

        print("Starting server on http://{}:{}".format(ip, port))
        if dry_run:
            return {
                "message": "would start flask development server using graph_browser app",
                "ip": ip,
                "port": port,
            }
        else:
            app.run(host=ip, port=port, debug=True)
