"""
Module to produce JSON structure compatible with vasturiano-3d-force-graph
library.

"""
import hashlib
import os
import logging
import json

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

class v3d_diagramm:
    
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
        color="red",
        nodeResolution=8,
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

        """
        if self._node_exists(id, label=label, data=data, url=url):
            return
        if not label.strip():
            label = id
        # create node element
        node = {
                "id": id,
                "label": label,
                "color": color,
                "nodeResolution": nodeResolution
            }
        # add data attributes and/or url to node
        node.update(data)
        node.update(kwargs)
        # add node to nodes dictionary
        self.nodes_dict[id] = node
        
    def update_node(
        self,
        id,
        data={},
        **kwargs
    ):
        """
        Method to update node details. Uses node ``id`` to search for node to update

        **Parameters**

        * ``id`` (str) mandatory, unique node identifier

        """
        node = self.nodes_dict.get(id)
        if not node:
            log.erorr("node_update: node {} not found".format(id))
        # update node attributes
        node.update(data)
        node.update(kwargs)
        
    def _link_exists(self, id, edge_tup):
        """method, used to check dublicate edges"""
        # check if edge with given id already exists
        if id in self.links_dict:
            if self.link_duplicates == "log":
                log.error(
                    "_link_exists: edge '{}' already added to graph".format(
                        ",".join(edge_tup)
                    )
                )
            elif self.link_duplicates == "skip":
                pass
            return True
        self.links_dict[id] = {}
        
    def add_link(
        self,
        source,
        target,
        label="",
        src_label="",
        trgt_label="",
        data={},
        url="",
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
        * ``src_label`` (str) link label to display next to source node
        * ``trgt_label`` (str) link label to display next to target node

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
        # create edge id
        edge_tup = tuple(sorted([label, source, target, src_label, trgt_label]))
        edge_id = hashlib.md5(",".join(edge_tup).encode()).hexdigest()
        if self._link_exists(edge_id, edge_tup):
            return
        # create link
        link = {
                "id": edge_id,
                "label": label,
                "source": source,
                "target": target,
                "src_label": src_label,
                "trgt_label": trgt_label
            }
        # add links data and url
        link_data.update(data)
        link_data.update(kwargs)
        # save link to graph
        self.links_dict[edge_id] = link
        
    def layout(self, algo="kk", dx=500, dy=500, dz=500, **kwargs):
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
        # iterate over nodes
        for id in self.nodes_dict.keys():
            igraph_graph.add_vertex(name=item.get("id"))
        # add edges
        for item in self.links_dict.values():
            igraph_graph.add_vertex(name=item.get("source"))
            igraph_graph.add_vertex(name=item.get("target"))
            igraph_graph.add_edge(
                source=item.get("source"), target=data.get("target")
            )
        # calculate layout
        layout = igraph_graph.layout(layout=algo, **kwargs)
        # scale layout to diagram size
        x = int(dx)
        y = int(dy)
        layout.fit_into(bbox=(x, y))
        # add coordinates from layout to diagram nodes
        for index, coord_item in enumerate(layout.coords):
            x_coord, y_coord = coord_item
            node_id = igraph_graph.vs[index].attributes()["name"]
            node_geometry_element = self.current_root.find(
                "./object[@id='{id}']/mxCell/mxGeometry".format(id=node_id)
            )
            node_geometry_element.set("x", str(round(x_coord)))
            node_geometry_element.set("y", str(round(y_coord)))
            
    def from_dict(self, data):
        """
        Method to build graph from dictionary.

        **Parameters**

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
        [self.add_node(**node) for node in data.get("nodes", [])]
        [self.add_link(**link) for link in data.get("links", [])]
        [self.add_link(**edge) for edge in data.get("edges", [])]

    def from_list(self, data):
        """
        Method to build graph from list.

        **Parameters**

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
        [self.add_link(**edge) for edge in data]

    def dump_dict(self):
        self.drawing = {
            "nodes": list(self.nodes_dict.values()), 
            "links": list(self.links_dict.values())
        }
        return self.drawing     
        
    def dump_json(self, **kwargs):
        return json.dumps(self.dump_dict(), **kwargs)

    def run(self, ip="0.0.0.0", port=9000):
        index_html = """
<head>
  <style> body { margin: 0; } </style>
  
  <script src="//unpkg.com/dat.gui"></script>
  <script src="//unpkg.com/3d-force-graph"></script>
  
</head>

<body>
  <div id="3d-graph"></div>
 
  <script type="module">    
    import { UnrealBloomPass } from '//unpkg.com/three/examples/jsm/postprocessing/UnrealBloomPass.js';
    
    const elem = document.getElementById("3d-graph");
    const json_data = `{{ json_data | json }}`;
    var gData = JSON.parse(json_data);
    
    // create graph
    const Graph = ForceGraph3D()(elem)
        .enableNodeDrag(true)
        .nodeLabel(node => node.label)
        .graphData(gData)
        .onNodeDragEnd(node => {
          node.fx = node.x;
          node.fy = node.y;
          node.fz = node.z;
        });
        
    // add bloom
    const bloomPass = new UnrealBloomPass();
    bloomPass.strength = 3;
    bloomPass.radius = 1;
    bloomPass.threshold = 0.1;
    Graph.postProcessingComposer().addPass(bloomPass);
    
    //Define GUI
    const Settings = function() {
      this.Distance = 20;
      this.isAnimationActive = true;
      this.isRotating = false;
    };
    var settings = new Settings();
    const gui = new dat.GUI();

    // link distance:
    const linkForce = Graph
      .d3Force('link')
      .distance(settings.Distance);

    const controllerOne = gui.add(settings, 'Distance', 0, 100);
    controllerOne.onChange(updateLinkDistance);
    function updateLinkDistance() {
      linkForce.distance(settings.Distance);
      Graph.numDimensions(3); // Re-heat simulation
    }
    
    // pause / resume animation
    const controllerAnim = gui.add(settings, 'isAnimationActive');
    controllerAnim.onChange(updateAnimation);
    function updateAnimation() {
      Settings.isAnimationActive ? Graph.resumeAnimation() : Graph.pauseAnimation() ;
      Settings.isAnimationActive = !Settings.isAnimationActive;
    }    

  </script>
</body>        
        """
        from flask import Flask, render_template_string, Markup

        app = Flask(__name__)
        
        # based on https://stackoverflow.com/a/19269087/12300761 answer:
        app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))
    
        @app.route('/')
        def home():
            return render_template_string(index_html, json_data=self.dump_dict())
            
        print("Starting server on http://{}:{}".format(ip, port))
        app.run(host=ip, port=port, debug=True)