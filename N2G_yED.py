try:
    from lxml import etree
except ImportError:
    raise SystemExit("ERROR: 'lxml' module not installed. Install: 'python -m pip install lxml'; Exiting")
    
from time import ctime
from json import dumps as json_dumps  # need it to dump metadata for edges/nodes
from json import loads as json_loads  # need it to load metadata for edges/nodes
import os

# Initiate global variables:
ctime = ctime().replace(':','-')

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
""".encode('utf8') #need to add encoding as "encoding="UTF-8"" specified in text

shape_node_xml = """
<node id="nNodeID" xmlns:y="http://www.yworks.com/xml/graphml">
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
<node id="nNodeID" xmlns:y="http://www.yworks.com/xml/graphml">
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
<edge xmlns:y="http://www.yworks.com/xml/graphml" id="eEdgeID" source="nNodeID" target="nNodeID">
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
        
  
class yed_diagram():

    def __init__(self, graph_data = ''):
        """    
        Vars:
        graph_data - string, xml formatted data to load graph from
        """        
        if graph_data == '':                                # create empty graph_root element:
            self.GRAPH = etree.fromstring(graph_xml)
        elif os.path.exists(graph_data[:3000]):                # check that os path to file given:
            with open (graph_data, 'r') as g:
                self.GRAPH = etree.fromstring(g.read().encode('utf8'))
        elif type(graph_data) == str:                       # create graph from string:
            self.GRAPH = etree.fromstring(graph_data)
        else:                                               # raise error:
            raise SystemExit("Error: Cannot create graph from '{}'".format(graph_data))
                
        # initialize ID counters and misceleneous dictionaries to store auxilary data:
        self.ids_dict = {'edges': [-1], 'resources': [-1]}
                
        self.nodes_dict = {}    # dictionary, {id: 'node_id'} mapping id - node name string, n{node_id} digit string
        self.edges_dict = {}    # dictionary, {sorted((source,target,label,src_label,trgt_label,)): e{edge_id}} mapping
        self.svg_pics_dict = {} # dictionary, {pic_path+pic:[pic_reference_id, pic_width, pic_height]} mappings
        self.y_attr={}          # dictionary, contains:
                                #     "edge": 
                                #         "description": "d12",
                                #         "edgegraphics": "d13",
                                #         "emetadata": "d10",
                                #         "url": "d11"
                                #     "graph": 
                                #         "Description": "d0",
                                #         "gmetadata": "d1"
                                #     "graphml": 
                                #         "resources": "d9"
                                #     "node": 
                                #         "description": "d7",
                                #         "nmetadata": "d5",
                                #         "nodegraphics": "d8",
                                #         "url": "d6"
                                #     "port": 
                                #         "portgeometry": "d3",
                                #         "portgraphics": "d2",
                                #         "portuserdata": "d4"
                                
        # extract namespaces and prefix default namespace, as lxml do not support it:
        self.ns_dict = self.GRAPH.nsmap
        self.ns_dict['default_ns'] = self.ns_dict[None]
        self.ns_dict.pop(None)                
        
        # load nodes and edges from self.GRAPH if any:
        self.__load_graph()
        

    def __load_graph(self):
        """
        function to load nodes and edges from graph
        """        
        # find all keys and load graph attributes identifiers:
        keys = self.GRAPH.findall('.//default_ns:key', namespaces=self.ns_dict)
        for key in keys:
            if 'attr.name' in key.attrib:
                attrname = key.attrib['attr.name']
            elif 'yfiles.type' in key.attrib:
                attrname = key.attrib['yfiles.type']
            if not key.attrib['for'] in self.y_attr:
                self.y_attr[key.attrib['for']] = {}
            self.y_attr[key.attrib['for']][attrname] = key.attrib['id']
        # load all nodes:
        nodes = self.GRAPH.findall('.//default_ns:node', namespaces=self.ns_dict)        
        for node in nodes:    
            # get node metadata:
            try:
                nmetadata = json_loads(
                        node.xpath('.//default_ns:data[@key="{}"]'.format(self.y_attr['node']['nmetadata']), 
                        namespaces = self.ns_dict)[0].text)
            except IndexError:
                raise SystemExit("Error: Failed load graph. Node {} metadata not found.".format(node.attrib['id']))
            # fill in nodes dict:
            self.nodes_dict[nmetadata['id']]=node.attrib['id']
        # load all edges:
        edges = self.GRAPH.findall('.//default_ns:edge', namespaces=self.ns_dict)
        for edge in edges:
            # try to extract source label:
            try: src_label = edge.xpath('.//y:EdgeLabel[@preferredPlacement="source_on_edge"]', namespaces = self.ns_dict)[0].text
            except IndexError: src_label = ''
            # try to extract target label:
            try: trgt_label = edge.xpath('.//y:EdgeLabel[@preferredPlacement="target_on_edge"]', namespaces = self.ns_dict)[0].text
            except IndexError: trgt_label = ''
            # try to extract label:
            try: label = edge.xpath('.//y:EdgeLabel[@preferredPlacement="center_on_edge"]', namespaces = self.ns_dict)[0].text
            except IndexError: label = ''                
            # get edge metadata:
            try:
                emetadata = json_loads(
                        edge.xpath('.//default_ns:data[@key="{}"]'.format(self.y_attr['edge']['emetadata']), 
                        namespaces = self.ns_dict)[0].text)            
            except IndexError:
                raise SystemExit("Error: Failed load graph. Edge {} metadata not found.".format(edge.attrib['id']))
            # add edge id to ids_dict:
            edge_id = int(edge.attrib['id'].lstrip('e'))
            self.ids_dict['edges'].append(edge_id)
            # fill in edges dict:
            self.edges_dict[tuple(sorted([
            emetadata['sid'], 
            emetadata['tid'],
            label,src_label,trgt_label,]))] = 'e{}'.format(str(edge_id))
                
    
    def _create_label_element(self, 
        xml_template_name,  # string, name of XML label template
        label = '',         # string, center label of edge/nodes
        path = '',          # string, xpath formatted 'path', if empty, work with element tag
        **kwargs            # attributes to ".set()" for edge/node label lement for "path" tag 
        ):
        """
        function to create label elemnts forappending to edge/nodes' elements
        """
        element = etree.fromstring(xml_template_name) # create  element
        if label != '':
            element.text = label
        if kwargs:
            if path == '':
                for k, v in kwargs.items():
                    element.set(k, v)
            else:
                for k, v in kwargs.items():
                    element.xpath(path, namespaces = self.ns_dict)[0].set(k, v)
        return element    
        
        
    def __create_data_element(self,
        id,   # string, id of data element, e,g, d11, d4, d1 etc.
        text  # string, text to add to data element
        ):
        elem = etree.fromstring('<data key="{}"/>'.format(id))
        elem.text=text.strip()
        return elem
        
        
    def _addshapenode(self, 
        id,                 # string, name of the node
        label = '',         # string, label at the center of the node
        top_label = '',     # string, label at the top of the node
        bottom_label = '',  # string, label at the bottom of the node
        attributes = {},    # dictionary, contains node attributes
        description = '',   # string, data to add in node description
        dublicates = 'exit',# string, action if node dublicate found
        url = ''            # string, data to add tonode URL
        ):
        """
        method to add node of type "shape", by default shape is "rectangle"
        """
        # check for node dublicates:
        if id in self.nodes_dict: 
            if dublicates == 'exit':
                raise SystemExit("Error: NodeDublicate. Cannot create node named '{}', label '{}', node already exists".format(id, label))
            elif dublicates == 'skip':
                return            
            elif dublicates == 'update':
                self.update_node(self.nodes_dict[id], label, top_label, bottom_label,
                                attributes, description)
                return

        # create node element:
        node = etree.fromstring(shape_node_xml.format(attrib_id=self.y_attr['node']['nodegraphics'])) 
        self.nodes_dict[id] = id
        node.set('id', id)    
        
        # add labels and description data to the node:
        ShapeNode = node.xpath('./data/y:ShapeNode', namespaces = self.ns_dict)[0]
        if label == '':
            ShapeNode.append(self._create_label_element(node_label_xml, id, modelPosition = 'c'))
        if label != '':
            ShapeNode.append(self._create_label_element(node_label_xml, label, modelPosition = 'c'))
        if top_label != '':
            ShapeNode.append(self._create_label_element(node_label_xml, top_label, modelPosition = 't'))
        if bottom_label != '':
            ShapeNode.append(self._create_label_element(node_label_xml, bottom_label, modelPosition = 'b'))        
        if description != '':
            node.append(self.__create_data_element(id=self.y_attr['node']['description'], text=description))
        if url != '':
            node.append(self.__create_data_element(id=self.y_attr['node']['url'], text=url))
            
        # save original id in node custom attribute:
        node.append(self.__create_data_element(
            id=self.y_attr['node']['nmetadata'],
            text = json_dumps({'id': id}, 
                        sort_keys=True, indent=4, separators=(',', ': '))))
            
        # set attributes for the node:    
        if attributes:
            self.set_attributes(ShapeNode, attributes)
        
        self.GRAPH.xpath("//default_ns:graph", namespaces = self.ns_dict)[0].append(node)
        
        
    def _addsvgnode(self, 
        pic,                  # string, name of SVG picture file to use
        id,                   # string, name of the node
        pic_path = './Pics/', # string, OS path to SVG picture file
        label = '',           # string, label to display above the top of the node
        attributes = {},      # dictionary, contains node attributes
        description = '',     # string, data to add in node description
        dublicates = 'exit',  # string, action if node dublicate found
        url = ''              # string, data to add tonode URL        
        ):
        """
        method to add svg picture node. This method loads SVG picture as resource content into the XML graph file.
        """
        # check if node with given name already exists, if so, raise error and stop programm:
        if id in self.nodes_dict: 
            if dublicates == 'exit':
                raise SystemExit("Error: Dublicate. Cannot create node named '{}', label '{}', node already exists".format(id, label))
            elif dublicates == 'skip':
                return        
            elif dublicates == 'update':
                self.update_node(self.nodes_dict[id], label,
                                attributes, description)
                return
            
        # sanitize pic:
        if not pic.endswith('.svg'):
            pic += '.svg'
    
        # create svg_node element:
        svg_node = etree.fromstring(svg_node_xml.format(attrib_id=self.y_attr['node']['nodegraphics']))
        self.nodes_dict[id] = id
        svg_node.set('id', id)
        
        # check wether svg pic with given name already been loaded, if yes, use it:
        svg_pic_already_loaded = False
        for path, params in self.svg_pics_dict.items():
            if path == pic_path + pic: # hence svg pic already been loaded
                svg_node.xpath('./data/y:SVGNode/y:SVGModel/y:SVGContent', namespaces = self.ns_dict)[0].set('refid', str(params[0]))
                svg_node.xpath('./data/y:SVGNode/y:Geometry', namespaces = self.ns_dict)[0].set('width', str(params[1]))
                svg_node.xpath('./data/y:SVGNode/y:Geometry', namespaces = self.ns_dict)[0].set('height', str(params[2]))
                svg_pic_already_loaded = True
                break
            
        # load svg pic resource into graph resources section if not yet loaded:        
        if svg_pic_already_loaded == False:             
            with open(pic_path + pic) as pic_file:
                pic_xml = pic_file.read()
                # extract pic width and height that can be containedin viewBox attribute as well:
                pic_element = etree.fromstring(pic_xml.encode('utf8'))
                pic_viewbox = pic_element.get("viewBox")
                if pic_viewbox:
                    pic_width = pic_viewbox.split(' ')[3]
                    pic_height = pic_viewbox.split(' ')[2]
                else:
                    pic_width = pic_element.get("width")
                    pic_height = pic_element.get("height")
                del(pic_element)
                # modify pic_xml for inclusion into resource element
                pic_xml = pic_xml.replace('\<', '&lt;').replace('\>', '&gt;')
            resource_id = self.ids_dict['resources'][-1] + 1
            self.ids_dict['resources'].append(resource_id)
            
            # save pic and it's params into sgv_pics_dict dictionary:
            self.svg_pics_dict[pic_path + pic] = [resource_id, pic_width, pic_height]
            
            # create resource element:
            svg_resource_element = etree.fromstring(resource_xml) 
            svg_resource_element.set('id', str(resource_id))
            svg_resource_element.text = pic_xml
            self.GRAPH.xpath('//default_ns:data/y:Resources', namespaces = self.ns_dict)[0].append(svg_resource_element)
            del(svg_resource_element)
            
            # add svg resource refid, width, height parametrs to svg_node element:
            svg_node.xpath('./data/y:SVGNode/y:SVGModel/y:SVGContent', namespaces = self.ns_dict)[0].set('refid', str(resource_id))
            svg_node.xpath('./data/y:SVGNode/y:Geometry', namespaces = self.ns_dict)[0].set('width', pic_width)
            svg_node.xpath('./data/y:SVGNode/y:Geometry', namespaces = self.ns_dict)[0].set('height', pic_height)
            
        # add label and description data to the node:
        if label == '':
            svg_node.xpath('./data/y:SVGNode', namespaces = self.ns_dict)[0].append(
                    self._create_label_element(node_label_xml, id, modelName='sandwich', modelPosition='n'))
        elif label != '':
            svg_node.xpath('./data/y:SVGNode', namespaces = self.ns_dict)[0].append(
                    self._create_label_element(node_label_xml, label, modelName='sandwich', modelPosition='n'))
        if description != '':
            svg_node.append(self.__create_data_element(id=self.y_attr['node']['description'], text=description))
        if url != '':
            svg_node.append(self.__create_data_element(id=self.y_attr['node']['url'], text=url))
            
        # save original id in node custom attribute:
        svg_node.append(self.__create_data_element(
            id=self.y_attr['node']['nmetadata'],
            text = json_dumps({
            'id': id
            }, sort_keys=True, indent=4, separators=(',', ': '))
            ))        
        
        # add node to the graph and delete node_element:
        self.GRAPH.xpath("//default_ns:graph", namespaces = self.ns_dict)[0].append(svg_node)

        
    def _addgroupnode(self,
            id,                 # string, name of the node
            label = '',         # string, label at the center of the node
            top_label = '',     # string, label at the top of the node
            bottom_label = '',  # string, label at the bottom of the node
            attributes = {},    # dictionary, contains node attributes
            description = '',   # string, data to add in node description
            dublicates = 'exit',# string, action if node dublicate found
            url = ''            # string, data to add tonode URL
            ):        
        """
        method to add node of type "shape", by default shape is "rectangle"
        """
        # check for node dublicates:
        if id in self.nodes_dict: 
            if dublicates == 'exit':
                raise SystemExit("Error: NodeDublicate. Cannot create node named '{}', label '{}', node already exists".format(id, label))
            elif dublicates == 'skip':
                return            
            elif dublicates == 'update':
                return

        # create node element:
        node = etree.fromstring(group_node_xml.format(attrib_id=self.y_attr['node']['nodegraphics'])) 
        self.nodes_dict[id] = id
        node.set('id', id)    
        # set id for groupnode graph:
        node.xpath('./graph', namespaces = self.ns_dict)[0].set('id', '{}:'.format(id))
        
        # add labels and description data to the node:
        GroupNode = node.xpath('./data/y:ProxyAutoBoundsNode/y:Realizers/y:GroupNode', namespaces = self.ns_dict)[0]
        if label != '':
            GroupNode.append(self._create_label_element(node_label_xml, label, modelPosition = 'c'))
        if top_label != '':
            GroupNode.append(self._create_label_element(node_label_xml, top_label, modelPosition = 't'))
        if bottom_label != '':
            GroupNode.append(self._create_label_element(node_label_xml, bottom_label, modelPosition = 'b'))        
        if description != '':
            node.append(self.__create_data_element(id=self.y_attr['node']['description'], text=description))
        if url != '':
            node.append(self.__create_data_element(id=self.y_attr['node']['url'], text=url))
            
        # save original id in node custom attribute:
        node.append(self.__create_data_element(
            id=self.y_attr['node']['nmetadata'],
            text = json_dumps({'id': id}, 
                        sort_keys=True, indent=4, separators=(',', ': '))))
            
        # set attributes for the node:    
        if attributes:
            self.set_attributes(GroupNode, attributes)
        
        self.GRAPH.xpath("//default_ns:graph", namespaces = self.ns_dict)[0].append(node)
        
        
    def addnode(self, 
        id,                    # string, name of the node
        label = '',            # string, label at the center of shape node or above the top of svg node
        top_label = '',        # string, label at the top of the node, ignored if pic is present
        bottom_label = '',     # string, label at the bottom of the node, ignored if pic is present
        pic = '',              # string, name of SVG picture file to use
        pic_path = './Pics/',  # string, OS path to SVG picture file
        attributes = {},       # 
        description = '',      # 
        url = '',              # string, data to add to node URL
        dublicates = 'exit',   # 
        group = False          # boolean, to indicate if node is a group if True or relation to group
        ):
        """
        method to add node, by calling one of internal methods, decision made based on presence of 
        'pic', e.g., if present, create svg node, if not, create shape node
        """
        if group == True:
            self._addgroupnode(
                        id = id, 
                        label = label, 
                        top_label = top_label, 
                        bottom_label = bottom_label, 
                        attributes = attributes, 
                        description = description, 
                        dublicates = dublicates,
                        url = url)
        elif pic == '':
            self._addshapenode(
                        id = id, 
                        label = label, 
                        top_label = top_label, 
                        bottom_label = bottom_label, 
                        attributes = attributes, 
                        description = description, 
                        dublicates = dublicates,
                        url = url)
        else:
            self._addsvgnode(
                        id = id, 
                        pic = pic, 
                        pic_path = pic_path, 
                        label = label, 
                        attributes = attributes, 
                        description=description, 
                        dublicates = dublicates,
                        url = url)
        

    def check_edge_dublicate(self, source, target, src_label, trgt_label, edge_tup):
        """method, used to check dublicate edges 
        """
        # check full match:
        if edge_tup in self.edges_dict: 
            return True
        
        # check 3 out of 4 matches - to find dublicates if new edge been added:
        for edge in self.edges_dict.keys():
            if self.nodes_dict[source] in edge and self.nodes_dict[target] in edge:
                if src_label in edge or trgt_label in edge:
                    return True        

        # return False by default:
        return False
            
            
    def addedge(self, 
        source,                   # string, name of the source node
        target,                   # string, name of the terget node
        label = '',               # string, label to display in the center of the edge
        src_label = '',           # string, label to display at source end of the edge
        trgt_label = '',          # string, label to display at target end of the edge
        description = '',         # string, text to add as description data to the edge
        label_attribs = {},       # 
        src_label_attribs = {},   # 
        trgt_label_attribs = {},  # 
        attributes = {},          # dict, edge attributes             
        dublicates = 'skip',      # 
        url = ''                  # string, data to add to edge URL        
        ):
        """method to add edge
        """
        # create edge tuple hash:
        edge_tup = tuple(sorted([
            source, target,  # have to use provided node ids to be able properly update graph
            label,src_label,trgt_label,]))

        # check dublicates:
        if self.check_edge_dublicate(source, target, src_label, trgt_label, edge_tup) == True:
            if dublicates == 'skip': 
                return
            if dublicates == 'update':
                return
        
        # create edge element:
        edge = etree.fromstring(edge_xml.format(attrib_id=self.y_attr['edge']['edgegraphics'])) 
        edge_id = self.ids_dict['edges'][-1] + 1
        self.ids_dict['edges'].append(edge_id)
        edge.set('id', 'e{}'.format(str(edge_id)))

        # fill in edges dict:
        self.edges_dict[edge_tup] = 'e{}'.format(str(edge_id))
        
        # find source and target node ID of the edge in self.nodes_dict:
        edge.set('source', self.nodes_dict[source])
        edge.set('target', self.nodes_dict[target])
        
        # fill labels and description:
        PolyLineEdge = edge.xpath('./data/y:PolyLineEdge', namespaces = self.ns_dict)[0]
        if label != '':
            PolyLineEdge.append(self._create_label_element(edge_label_xml, label, 
                    path = 'y:PreferredPlacementDescriptor', placement = 'center'))
        if src_label != '':
            PolyLineEdge.append(self._create_label_element(edge_label_xml, src_label, 
                    path = 'y:PreferredPlacementDescriptor', placement = 'source'))
        if trgt_label != '':
            PolyLineEdge.append(self._create_label_element(edge_label_xml, trgt_label, 
                    path = 'y:PreferredPlacementDescriptor', placement = 'target'))
        if description != '':
            edge.append(self.__create_data_element(id=self.y_attr['edge']['description'], text=description))
        if url != '':
            edge.append(self.__create_data_element(id=self.y_attr['edge']['url'], text=url))
            
        # save source and target original nodes' id in edge custom attributes:
        edge.append(self.__create_data_element(
            id=self.y_attr['edge']['emetadata'],
            text = json_dumps({
            'sid': source,
            'tid': target
            }, sort_keys=True, indent=4, separators=(',', ': '))
            ))            

        # set edge labels' attributes:
        if label_attribs:
            for attr_name, attr_value in src_label_attribs.items():
                edge.xpath('./data/y:PolyLineEdge/y:EdgeLabel[y:PreferredPlacementDescriptor[@placement="center"]]', 
                namespaces = self.ns_dict)[0].set(attr_name, attr_value)            
        if src_label_attribs:
            for attr_name, attr_value in src_label_attribs.items():
                edge.xpath('./data/y:PolyLineEdge/y:EdgeLabel[y:PreferredPlacementDescriptor[@placement="source"]]', 
                namespaces = self.ns_dict)[0].set(attr_name, attr_value)
        if trgt_label_attribs:
            for attr_name, attr_value in trgt_label_attribs.items():
                edge.xpath('./data/y:PolyLineEdge/y:EdgeLabel[y:PreferredPlacementDescriptor[@placement="target"]]', 
                namespaces = self.ns_dict)[0].set(attr_name, attr_value)
        
        # fill in edge attributes:
        if attributes:
            self.set_attributes(PolyLineEdge, attributes)
                    
        # append edge element to graph:
        self.GRAPH.xpath("//default_ns:graph", namespaces = self.ns_dict)[0].append(edge)
        
        
    def fromdict(self, 
        graph_dictionary,   # dictionary, structure: {nodes:[{node1 kwargs}], edges:[{edge1 kwargs}]}
        dublicates = 'exit' # string, action to do with dublicates
        ):
        """
        method to load graph from dictionary structured data.
        """
        # have to search edges and nodes keys first, as order shouldbe createNodes->addEdges, but dictionaryacn be hased in such a way that edges will appear before keys
        for key in graph_dictionary.keys(): 
            if 'NODES' in key.upper(): nodes_key = key
            elif 'EDGES' in key.upper() or 'LINKS' in key.upper(): edges_key = key
        for item in graph_dictionary[nodes_key]:
            self.addnode(dublicates=dublicates, **item)
        for item in graph_dictionary[edges_key]:
            self.addedge(dublicates=dublicates, **item)
    
    
    def save(self, 
        display = False,                   # boolean, if True output data to cli, if False, do not output to cli
        to_file = True,                    # boolean, if True save data to file
        file = ctime + '_result.graphml',  # string, name of the output file
        out_folder = './Output/'           # string, os path to the output folder
        ):
        """
        method to dump parsing result to graphml XML formatted file
        """
        if display == True:
            print(str(etree.tostring(self.GRAPH, pretty_print=True), 'ascii'))
                
        if to_file == True:
            # check output folder, if not exists, create it
            if not os.path.exists(out_folder):    
                os.makedirs(out_folder)    
            with open(out_folder + file, 'w') as outfile:
                print(str(etree.tostring(self.GRAPH, pretty_print=True), 'ascii'), file = outfile)
        
        
    def set_attributes(self, 
        element,      # lxml object to update attributes in
        attributes={} # dictionary of attributes to update
        ):
        """method to update attributes into element"""
        children = element.getchildren()
        for tag, attribs in attributes.items():
            tag_exists = False
            for child in children:
                if tag in child.tag:
                    child.attrib.update(attribs)
                    tag_exists = True
                
            if tag_exists == False: # create tag element:
                tag_elem = etree.fromstring('<y:{} xmlns:y="http://www.yworks.com/xml/graphml"/>'.format(tag))
                tag_elem.attrib.update(attribs)
                element.append(tag_elem)
        
        
    def update_node(self, 
            node_id,            # string, name of the node
            label = '',         # string, label at the center of the node
            top_label = '',     # string, label at the top of the node
            bottom_label = '',  # string, label at the bottom of the node
            attributes = {},    # dictionary, contains node attributes
            description = '',   # string, data to add in node description
            ):
        # get node element:    
        node = self.GRAPH.xpath('.//default_ns:node[@id="{}"]'.format(node_id), namespaces=self.ns_dict)[0]
        ShapeNode = node.xpath('./default_ns:data/y:ShapeNode', namespaces = self.ns_dict)
        SVGNode = node.xpath('./default_ns:data/y:SVGNode', namespaces = self.ns_dict)
        if ShapeNode: NODE = ShapeNode[0]
        elif SVGNode: NODE = SVGNode[0]
        
        # update node attributes:
        self.set_attributes(NODE, attributes)            
        
        # update node labels:
        labels = NODE.findall('.//y:NodeLabel', namespaces=self.ns_dict)
        for l in labels:
            if not 'modelPosition' in l.attrib: continue
            if l.attrib['modelPosition'] == 'c':
                if label: l.text = label
            elif l.attrib['modelPosition'] == 't':
                if top_label: l.text = top_label
            elif l.attrib['modelPosition'] == 'b':
                if bottom_label: l.text = bottom_label
            # update label for SVG node
            elif l.attrib['modelPosition'] == 'n':
                if label: l.text = label
        
            
    def update_edge(self, edge_id='', attributes={}):
        edge = self.GRAPH.xpath('.//default_ns:edge[@id="{}"]'.format(edge_id), namespaces=self.ns_dict)[0]
        PolyLineEdge = edge.xpath('./default_ns:data/y:PolyLineEdge', namespaces = self.ns_dict)[0]
        
        self.set_attributes(PolyLineEdge, attributes)
                        
            
    def compare(self, 
        data,             # N2G dictionary data to compare against
        missing_nodes={   # dict, attributes to apply to missing nodes
        'BorderStyle': {'color': '# C0C0C0',    'width': '2.0'},
        'NodeLabel'  : {'textColor': '# C0C0C0'}}, 
        new_nodes={       # dict, attributes to apply to new nodes 
        'BorderStyle': {'color': '# 00FF00',    'width': '5.0'},
        'NodeLabel'  : {'textColor': '# 00FF00'}},
        missing_edges={   # dict, attributes to apply to missing edges
        'LineStyle'  : {'color':'# C0C0C0', 'width': '1.0'},
        'EdgeLabel'  : {'textColor': '# C0C0C0'}},
        new_edges={       # dict, attributes to apply to new edges
        'LineStyle'  : {'color':'# 00FF00', 'width': '1.0'},
        'EdgeLabel'  : {'textColor': '# 00FF00'}}
        ):
        """method to compare data graph with self.GRAPH producing third, resulting graph
        """
        # create results_graph object based on self.GRAPH, that will used to produce 
        # compare results graph:
        results_graph = graph(str(etree.tostring(self.GRAPH), 'ascii'))

        if type(data) == dict:
            # find new nodes:
            not_missing_nodes = []
            for node in data['nodes']:
                if not node['id'] in self.nodes_dict:
                    if 'attributes' in node:
                        node['attributes'].update(new_nodes)
                    else:
                        node['attributes'] = new_nodes
                    results_graph.addnode(**node)
                elif node['id'] in self.nodes_dict:
                    not_missing_nodes.append(self.nodes_dict[node['id']])
            
            # find missing nodes:
            for id in self.nodes_dict.values():
                if not id in not_missing_nodes:
                    results_graph.update_node(node_id=id, attributes=missing_nodes)
                    
            # find new edges:
            not_missing_edges = []
            for edge in data['edges']:
                # create edge tuple:
                edge_tup = []
                
                # try to find source node:
                if edge['source'] in self.nodes_dict: 
                    edge_tup.append(edge['source'])
                # if no such node, means we have new edge, add it:
                else: 
                    if 'attributes' in edge:
                        edge['attributes'].update(new_edges)
                    else:
                        edge['attributes'] = new_edges
                    results_graph.addedge(**edge)
                    continue
                
                # try to find target node:
                if edge['target'] in self.nodes_dict: 
                    edge_tup.append(edge['target'])
                # if no such node, means we have new edge, add it:
                else: 
                    if 'attributes' in edge:
                        edge['attributes'].update(new_edges)
                    else:
                        edge['attributes'] = new_edges
                    results_graph.addedge(**edge)
                    continue
                    
                # fill in the rest of labels to form tuple:
                if 'label' in edge: edge_tup.append(edge['label'])
                else: edge_tup.append('')
                if 'src_label' in edge: edge_tup.append(edge['src_label'])
                else: edge_tup.append('')                
                if 'trgt_label' in edge: edge_tup.append(edge['trgt_label'])
                else: edge_tup.append('')                    

                edge_tup = tuple(sorted(edge_tup))
                
                # if no edge_tup in self_edges_dict - means new edge:
                if not edge_tup in self.edges_dict:
                    if 'attributes' in edge:
                        edge['attributes'].update(new_edges)
                    else:
                        edge['attributes'] = new_edges
                    results_graph.addedge(**edge)
                # if edge_tup in self_edges_dict - means existing edge:
                elif edge_tup in self.edges_dict:
                    not_missing_edges.append(self.edges_dict[edge_tup])

            # find missing edges:
            for id in self.edges_dict.values():
                if not id in not_missing_edges:
                    results_graph.update_edge(edge_id=id, attributes=missing_edges)        
        
        results_graph.save(file = ctime + '_compare_result.graphml')

        
    # additional methods not yet done:                    
    def del_node(self, id = '', node_id = ''):
        pass
        
    def del_edge(self, source = '', target = '', edge_id = ''):
        pass