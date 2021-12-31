"""
CLI L2 Data Plugin
******************

CLI L2 Data Plugin can produce diagrams based on `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_ 
layer 2 information, hence the name "layer 2". This plugin builds network diagrams with relationships 
and nodes using CDP and LLDP protocols neighbors information. In addition, adding L1/L2 related data to 
diagram elements.

CLI L2 Data Plugin uses TTP templates to parse show commands output and transform them in Python dictionary structure. 
That structure processed further to build a dictionary compatible with N2G's diagram plugins ``from_dict`` 
method. That method used to populate diagrams with devices and links information.

In addition to parsing relationships for CDP and LLDP protocols, L2 Data Plugin can help to manipulate diagrams by 
combining links based on certain criteria, adding additional information to elements meta data and adding 
unknown (to CDP and LLDP) but connected nodes to diagram.

Features Supported
------------------

**Support matrix**

+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
|  Platform     |   CDP      |   LLDP    | interface | interface |   LAG     | links     |   node    | Add all   | Combine   |
|  Name         |   peers    |   peers   | config    | state     |   links   | grouping  |   facts   | connected | peers     |
+===============+============+===========+===========+===========+===========+===========+===========+===========+===========+
| cisco_ios     |    YES     |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| cisco_xr      |    YES     |    YES    |    YES    |    YES    |    YES    |    YES    |    ---    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| cisco_nxos    |    YES     |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| huawei        |    ---     |    YES    |    YES    |    ---    |    YES    |    YES    |    YES    |    ---    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+

**Features Description**

* ``CDP peers`` - adds links and nodes for CDP neighbors
* ``LLDP peers`` - adds links and nodes for LLDP neighbors
* ``interface config`` - adds interfaces configuration to links data
* ``interface state`` - add links state information to links data
* ``LAG links`` - combines links based on LAG membership
* ``links grouping`` - groups links between nodes
* ``node facts`` - adds information to nodes for vlans configuration
* ``Add all connected`` - add nodes for connected interfaces that has no peers via CDP or LLDP
* ``Combine peers`` - groups CDP/LLDP peers behind same port by adding "L2" node

Required Commands output
------------------------

cisco_ios, cisco_xr, cisco_nxos:

* ``show cdp neighbor details`` and/or ``show lldp neighbor details`` - mandatory
* ``show running-configuration`` - optional, used for LAG and interfaces config 
* ``show interface`` - optional, used for interfaces state and to add all connected nodes

huawei:

* ``display lldp neighbor details`` - mandatory
* ``display current-configuration`` - optional, used for LAG and interfaces config 
* ``display interface`` - optional, used for interfaces state and to add all connected nodes

Sample Usage 
------------

Code to populate yEd diagram object with CDP and LLDP sourced nodes and links::

    from N2G import cli_l2_data, yed_diagram
    
    data = {"cisco_ios": ['''
    switch-1#show cdp neighbors detail
    -------------------------
    Device ID: switch-2
    Entry address(es):
      IP address: 10.2.2.2
    Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
    Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5
    
    -------------------------
    Device ID: switch-3
    Entry address(es):
      IP address: 10.3.3.3
    Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
    Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1
    
    -------------------------
    Device ID: switch-4
    Entry address(es):
      IP address: 10.4.4.4
    Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP
    Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10
    
    switch-1#show run
    interface GigabitEthernet4/6
     description switch-2: access
     switchport
     switchport access vlan 2150
     switchport mode access
     spanning-tree portfast edge
    !
    interface GigabitEthernet1/1
     description switch-3:Gi0/1
     switchport
     switchport trunk allowed vlan 1771,1887
     switchport mode trunk
     mtu 9216
    !
    interface GigabitEthernet1/2
     description SW4 Routing Peering
     vrf forwarding VRF1
     ip address 10.0.0.1 255.255.255.0
        ''',
        '''
    switch-2#show cdp neighbors detail
    -------------------------
    Device ID: switch-1
    Entry address(es):
      IP address: 10.1.1.1
    Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP
    Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6
    
    switch-2#show run
    interface GigabitEthernet1/5
     description switch-1: access
     switchport
     switchport access vlan 2150
     switchport mode access
     spanning-tree portfast edge
        ''']
        }
        
    config = {
        "add_interfaces_data": True,
        "group_links": False,
        "add_lag": False,
        "add_all_connected": False,
        "combine_peers": False,
        "platforms": ["_all_"]    
    }

    drawing_l2 = yed_diagram()
    drawer = cli_l2_data(drawing_l2, **config)
    drawer.work(data)
    drawer.drawing.dump_file()
    
API Reference
-------------

.. autoclass:: N2G.plugins.data.cli_l2_data.cli_l2_data
   :members:
"""
if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

import logging
import pprint
import json
import os

try:
    from ttp import ttp
    from ttp_templates import ttp_vars as ttp_templates_vars
    from ttp_templates import get_template

    HAS_TTP = True
except ImportError:
    HAS_TTP = False

# initiate logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Main class:
# -----------------------------------------------------------------------------


class cli_l2_data:
    """
    Class to instantiate L2 (layer two) data plugin to process CDP and LLDP neighbors
    together with devices' running configuration and state and produce
    diagram out of it.

    :param drawing: (obj) N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    :param ttp_vars: (dict) dictionary to use as TTP parser object template variables
    :param platforms: (list) - list of platform names to process e.g. ``cisco_ios``, ``cisco_xr`` etc, default is ``_all_``
    :param add_interfaces_data: (bool) default ``True``, add interfaces configuration and state data to links
    :param group_links: (bool) default ``False``, group links between nodes
    :param add_lag: (bool) default ``False``, add LAG/MLAG links to diagram
    :param add_all_connected: (bool) default ``False``, add all nodes connected to devices based on interfaces state
    :param combine_peers`: (bool) default ``False``, combine CDP/LLDP peers behind same interface by adding L2 node
    :param skip_lag: (bool) default ``True``, skip CDP peers for LAG, some platforms send CDP/LLDP PDU from LAG ports
    """

    def __init__(
        self,
        drawing,
        ttp_vars=None,
        add_interfaces_data=True,
        group_links=False,
        add_lag=False,
        add_all_connected=False,
        combine_peers=False,
        skip_lag=True,
        platforms=None,
    ):
        # init attributes
        self.add_interfaces_data = add_interfaces_data
        self.group_links = group_links
        self.add_lag = add_lag
        self.add_all_connected = add_all_connected
        self.combine_peers = combine_peers
        self.skip_lag = skip_lag
        self.platforms = platforms or ["_all_"]
        self.ttp_vars = ttp_vars or {
            "IfsNormalize": ttp_templates_vars.short_interface_names,
            "physical_ports": ttp_templates_vars.physical_ports,
        }
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.lag_links_dict = {}  # used by add_lag method
        self.nodes_to_links_dict = {}  # used by group_links
        self.combine_peers_dict = {}  # used by combine_peers

    def _make_hash_tuple(self, item):
        """
        Method to create link hash tuple out of source, target, src_label
        and trgt_label values
        
        :param item: (dict) link dictionary
        """
        target = (
            item["target"]["id"] if isinstance(item["target"], dict) else item["target"]
        )
        return tuple(
            sorted(
                [
                    item["source"],
                    target,
                    item.get("src_label", ""),
                    item.get("trgt_label", ""),
                ]
            )
        )

    def work(self, data):
        """
        Method to parse text data and add nodes and links to N2G drawing.

        :param data: (dict or str) dictionary or OS path string to directories with text files

        If data is dictionary, keys must correspond to "Platform" column in
        `Features Supported`_ section table, values are lists of text items to
        process.

        Data dictionary sample::

            data = {
                "cisco_ios" : ["h1", "h2"],
                "cisco_ios": ["h3", "h4"],
                "cisco_nxos": ["h5", "h6"],
                ...etc...
            }

        Where ``hX`` devices show commands output.

        If data is an OS path directory string, child directories' names must correspond
        to **Platform** column in `Features Supported`_ section table. Each child directory 
        should contain text files with show commands output for each device, names of files 
        are arbitrary, but output should contain device prompt to extract device hostname.

        Directories structure sample::

            ├───folder_with_data
                ├───cisco_ios
                │       switch1.txt
                │       switch2.txt
                └───cisco_nxos
                        nxos_switch_1.txt
                        nxos_switch_2.txt
                        
        To point N2G to above location ``data`` attribute string can be ``/var/data/n2g/folder_with_data/``
        """
        self._parse(data)
        self._form_base_graph_dict()
        # go through config statements
        if self.add_lag:
            self._add_lags_to_links_dict()
        if self.group_links:
            self._group_links()
        if self.add_all_connected:
            self._add_all_connected()
        if self.combine_peers:
            self._combine_peers()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _parse(self, data):
        """
        Function to parse text data using TTP templates
        
        :param data: (dict or str) data to parse
        """
        if not HAS_TTP:
            raise ModuleNotFoundError(
                "N2G:cli_l2_data failed importing TTP, is it installed?"
            )
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=self.ttp_vars)
            for platform_name, text_list in data.items():
                if (
                    "_all_" not in self.platforms
                    and not platform_name in self.platforms
                ):
                    continue
                ttp_template = get_template(
                    misc="N2G/cli_l2_data/{}.txt".format(platform_name)
                )
                parser.add_template(template=ttp_template, template_name=platform_name)
                for item in text_list:
                    parser.add_input(item, template_name=platform_name)
        # process directories at OS path
        elif isinstance(data, str):
            parser = ttp(vars=self.ttp_vars, base_path=data)
            # get all sub-folders and load respective templates
            with os.scandir(data) as dirs:
                for entry in dirs:
                    if entry.is_dir():
                        platform_name = entry.name
                        if (
                            "_all_" not in self.platforms
                            and not platform_name in self.platforms
                        ):
                            continue
                        ttp_template = get_template(
                            misc="N2G/cli_l2_data/{}.txt".format(platform_name)
                        )
                        parser.add_template(
                            template=ttp_template, template_name=entry.name
                        )
                        parser.add_input(
                            data=os.path.abspath(entry), template_name=platform_name
                        )
        else:
            log.error(
                "Expecting dictionary or string, but '{}' given".format(type(data))
            )
            return
        parser.parse(one=True)
        self.parsed_data = parser.result(structure="dictionary")
        # pprint.pprint(self.parsed_data, width = 100)

    def _form_base_graph_dict(self):
        for platform, hosts in self.parsed_data.items():
            for hostname, host_data in hosts.items():
                for item in host_data.get("cdp_peers", []):
                    self._add_node({"id": item["source"]}, host_data)
                    self._add_node(item["target"], hosts.get(item["target"]["id"], {}))
                    self._add_link(item, hosts, host_data)
                for item in host_data.get("lldp_peers", []):
                    self._add_node({"id": item["source"]}, host_data)
                    self._add_node(item["target"], hosts.get(item["target"]["id"], {}))
                    self._add_link(item, hosts, host_data)

    def _add_node(self, item, host_data):
        # add new node
        if not item["id"] in self.nodes_dict:
            if host_data.get("node_facts"):
                item["description"] = json.dumps(
                    host_data["node_facts"],
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )
            self.nodes_dict[item["id"]] = item
        # update node attributes if they do not exists already
        else:
            node = self.nodes_dict[item["id"]]
            for key, value in item.items():
                if not key in node:
                    node[key] = value
            if not "description" in node and host_data.get("node_facts"):
                node["description"] = json.dumps(
                    host_data["node_facts"],
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )

    def _add_link(self, item, hosts, host_data):
        # skip LAG or MLAG interfaces
        if self.skip_lag and (
            "LAG" in item.get("src_label", "") or "LAG" in item.get("trgt_label", "")
        ):
            return
        link_hash = self._make_hash_tuple(item)
        if link_hash not in self.links_dict:
            self.links_dict[link_hash] = {
                "source": item["source"],
                "target": item["target"]["id"],
                "src_label": item["src_label"],
                "trgt_label": item["trgt_label"],
            }
        # check if need to add interfaces data
        if self.add_interfaces_data:
            self._add_interfaces_data(item, hosts, host_data, link_hash)
        # check if need to pre-process lag_links_dict used by add_lag
        if self.add_lag:
            self._update_lag_links_dict(item, hosts, host_data)
        # check if need to pre-process nodes_to_links_dict used by group_links
        if self.group_links:
            self._update_nodes_to_links_dict(item, link_hash)
        # check if need to combine peers, preprocess combine_peers_dict
        if self.combine_peers:
            self._update_combine_peers_dict(item, link_hash)

    def _add_interfaces_data(self, item, hosts, host_data, link_hash):
        """
        Method to add description meta data to links containing information about
        interface configuration and state.
        """
        src = item["source"]
        tgt = item["target"]["id"]
        src_if = "{}:{}".format(src, item["src_label"])
        tgt_if = "{}:{}".format(tgt, item["trgt_label"])
        # form description data for link
        if not "description" in self.links_dict[link_hash]:
            description = {
                src_if: host_data.get("interfaces", {}).get(item["src_label"], {}),
                tgt_if: hosts.get(tgt, {})
                .get("interfaces", {})
                .get(item["trgt_label"], {}),
            }
            description[src_if].update(item.get("data", {}))
            # update item in graph data
            self.links_dict[link_hash]["description"] = json.dumps(
                description, sort_keys=True, indent=4, separators=(",", ": ")
            )

    def _update_lag_links_dict(self, item, hosts, host_data):
        """
        Method to form and add LAG link to lag_links_dict
        """
        lag_link = {}
        src = item["source"]
        tgt = item["target"]["id"]
        src_intf_name = item["src_label"]
        src_intf_data = host_data.get("interfaces", {}).get(src_intf_name, {})
        tgt_intf_name = item["trgt_label"]
        tgt_intf_data = hosts.get(tgt, {}).get("interfaces", {}).get(tgt_intf_name, {})
        if "lag_id" in src_intf_data:
            src_lag_name = "LAG{}".format(src_intf_data["lag_id"])
            src_lag_data = host_data.get("interfaces", {}).get(src_lag_name, {})
            if "mlag_id" in src_lag_data:
                src_lag_name = "MLAG{}".format(src_lag_data["mlag_id"])
            lag_link.update(
                {
                    "source": src,
                    "target": tgt,
                    "src_label": src_lag_name,
                    "description": {"{}:{}".format(src, src_lag_name): src_lag_data},
                }
            )
        if "lag_id" in tgt_intf_data:
            tgt_lag_name = "LAG{}".format(tgt_intf_data["lag_id"])
            tgt_lag_data = (
                hosts.get(tgt, {}).get("interfaces", {}).get(tgt_lag_name, {})
            )
            if "mlag_id" in tgt_lag_data:
                tgt_lag_name = "MLAG{}".format(tgt_lag_data["mlag_id"])
            lag_link.update({"source": src, "target": tgt, "trgt_label": tgt_lag_name})
            lag_link.setdefault("description", {})
            lag_link["description"].update(
                {"{}:{}".format(tgt, tgt_lag_name): tgt_lag_data}
            )
        # add lag link to links dictionary and remove members from links_dict
        if lag_link:
            lag_link_hash = self._make_hash_tuple(lag_link)
            src_member_intf_name = "{}:{}".format(src, src_intf_name)
            tgt_member_intf_name = "{}:{}".format(tgt, tgt_intf_name)
            member_link = {src_member_intf_name: tgt_member_intf_name}
            if lag_link_hash not in self.lag_links_dict:
                lag_link["description"]["lag_members"] = member_link
                self.lag_links_dict[lag_link_hash] = lag_link
            else:
                added_lag_members = self.lag_links_dict[lag_link_hash]["description"][
                    "lag_members"
                ]
                # only update members if opposite end not added already
                if not tgt_member_intf_name in added_lag_members:
                    self.lag_links_dict[lag_link_hash]["description"][
                        "lag_members"
                    ].update(member_link)
            # remove member interfaces from links dictionary
            members_hash = self._make_hash_tuple(item)
            _ = self.links_dict.pop(members_hash, None)
            # check if need to combine peers, add lag to combine_peers_dict
            if self.combine_peers:
                self._update_combine_peers_dict(item=lag_link, link_hash=lag_link_hash)

    def _add_lags_to_links_dict(self):
        """
        Method to merge lag_links_dict with links_dict
        """
        # convert description to json
        for link_hash, link_data in self.lag_links_dict.items():
            link_data["description"] = json.dumps(
                link_data["description"],
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        self.links_dict.update(self.lag_links_dict)
        del self.lag_links_dict

    def _update_nodes_to_links_dict(self, item, link_hash):
        """
        Method to update nodes_to_links_dict, used by group_links
        """
        src = item["source"]
        tgt = item["target"]["id"]
        nodes_hash = tuple(sorted([src, tgt]))
        self.nodes_to_links_dict.setdefault(nodes_hash, [])
        if not link_hash in self.nodes_to_links_dict[nodes_hash]:
            self.nodes_to_links_dict[nodes_hash].append(link_hash)

    def _update_combine_peers_dict(self, item, link_hash):
        port_id = (item["source"], item.get("src_label", ""))
        self.combine_peers_dict.setdefault(port_id, [])
        if not link_hash in self.combine_peers_dict[port_id]:
            self.combine_peers_dict[port_id].append(link_hash)

    def _group_links(self):
        """
        Method to group links between nodes and update links_dict
        """
        # find nodes that have more then 1 link in between, group links
        for node_pair, link_hashes in self.nodes_to_links_dict.items():
            if len(link_hashes) < 2:
                continue
            grouped_link = {"source": node_pair[0], "target": node_pair[1]}
            description = {"grouped_links": {}}
            links_to_group_count = 0
            for link_hash in link_hashes:
                if link_hash in self.links_dict:
                    links_to_group_count += 1
                    link_data = self.links_dict[link_hash]
                    src_label = "{}:{}".format(
                        link_data["source"], link_data.get("src_label", "")
                    )
                    trgt_label = "{}:{}".format(
                        link_data["target"], link_data.get("trgt_label", "")
                    )
                    description["grouped_links"][src_label] = trgt_label
                    description["link-{}".format(links_to_group_count)] = json.loads(
                        link_data["description"]
                    )
            # skip grouping links that does not have any members left in self.links_dict
            # happens when add_lag pops links or only one link between nodes left
            if links_to_group_count >= 2:
                # remove grouped links from links_dict
                for link_hash in link_hashes:
                    _ = self.links_dict.pop(link_hash, None)
                # form grouped links description and label
                grouped_link["description"] = json.dumps(
                    description, sort_keys=True, indent=4, separators=(",", ": ")
                )
                grouped_link["label"] = "x{}".format(links_to_group_count)
                grouped_link_hash = self._make_hash_tuple(grouped_link)
                self.links_dict[grouped_link_hash] = grouped_link
        del self.nodes_to_links_dict

    def _add_all_connected(self):
        """
        Method to iterate over all interfaces and fine theones that are
        in up state but having no CDP/LLDP peers, add nodes connected
        to such interfaces to graph
        """
        for platform, hosts in self.parsed_data.items():
            for hostname, host_data in hosts.items():
                for intf_name, intf_data in host_data["interfaces"].items():
                    # skip links that are not up
                    line = intf_data.get("state", {}).get("line", "").lower()
                    if not "up" in line:
                        continue
                    # skip non-physical ports
                    if not intf_data["state"].get("is_physical_port"):
                        continue
                    # check if interface has CDP or LLDP peers:
                    has_cdp_or_lldp_peer = False
                    for item in host_data.get("cdp_peers", []):
                        if item["src_label"] == intf_name:
                            has_cdp_or_lldp_peer = True
                    if has_cdp_or_lldp_peer:
                        continue
                    for item in host_data.get("lldp_peers", []):
                        if item["src_label"] == intf_name:
                            has_cdp_or_lldp_peer = True
                    if has_cdp_or_lldp_peer:
                        continue
                    # create new node and add it to graph
                    node_id = "{}:{}".format(hostname, intf_name)
                    node = {"id": node_id, "label": "Unknown"}
                    if intf_data.get("description"):
                        node["bottom_label"] = "{}..".format(
                            intf_data["description"][:20]
                        )
                    self._add_node(node, host_data={})
                    # add link to graph
                    link = {"source": hostname}
                    if "lag_id" in intf_data and self.add_lag:
                        lag_intf_name = "LAG{}".format(intf_data["lag_id"])
                        src_if = "{}:{}".format(hostname, lag_intf_name)
                        lag_intf_data = host_data["interfaces"].get(lag_intf_name, {})
                        if "mlag_id" in lag_intf_data:
                            lag_intf_name = "MLAG{}".format(lag_intf_data["mlag_id"])
                        link["src_label"] = lag_intf_name
                        link["description"] = json.dumps(
                            {
                                src_if: lag_intf_data,
                                "lag_members": {
                                    "{}:{}".format(hostname, intf_name): ""
                                },
                            },
                            sort_keys=True,
                            indent=4,
                            separators=(",", ": "),
                        )
                        # update node bottom label as per lag interface description
                        node["bottom_label"] = (
                            "{}..".format(lag_intf_data["description"][:20])
                            if lag_intf_data
                            else node["bottom_label"]
                        )
                        # remove previous node that had ID based on lag member interface
                        node = self.nodes_dict.pop(node_id, {})
                        new_node_id = "{}:{}".format(hostname, lag_intf_name)
                        node["id"] = new_node_id
                        link["target"] = new_node_id
                        self._add_node(node, host_data={})
                    else:
                        src_if = "{}:{}".format(hostname, intf_name)
                        link["target"] = node_id
                        link["src_label"] = intf_name
                        link["description"] = json.dumps(
                            {src_if: intf_data},
                            sort_keys=True,
                            indent=4,
                            separators=(",", ": "),
                        )
                    link_hash = self._make_hash_tuple(link)
                    if link_hash not in self.links_dict:
                        self.links_dict[link_hash] = link
                    else:
                        link_data = json.loads(
                            self.links_dict[link_hash]["description"]
                        )
                        if "lag_members" in link_data:
                            link_data["lag_members"].update(
                                {"{}:{}".format(hostname, intf_name): ""}
                            )
                        self.links_dict[link_hash]["description"] = json.dumps(
                            link_data, sort_keys=True, indent=4, separators=(",", ": ")
                        )

    def _combine_peers(self):
        """
        self.combine_peers_dict is a dictionary of {("hostname", "interface"): [links_hashes]}
        if length of [links_hashes] is more than 1, wehave several LLDP/CDP
        peers behind that port, usually happens with VMs sitting on host
        or some form of VPLS transport - we have L2 domain in between this port
        and CDP/LLDP peer.

        This method will add new node to diagram with "L2" label and
        "hostname:interface" id, connecting all CDP/LLDP peers to it.

        That is to reduce cluttering and improve readability.
        """
        for port_id, links_hashes in self.combine_peers_dict.items():
            # port_id - tuple of ("hostname", "interface")
            if len(links_hashes) < 2:
                continue
            # add L2 node
            l2_node_id = "{}:{}:L2_Node".format(*port_id)
            l2_node_port_id = "{}:{}".format(*port_id)
            self._add_node(
                item={
                    "id": l2_node_id,
                    "label": "L2",
                    "shape_type": "ellipse",
                    "height": 40,
                    "width": 40,
                },
                host_data={},
            )
            # add link to L2 node
            link_to_l2_node = {
                "source": port_id[0],
                "target": l2_node_id,
                "src_label": port_id[1],
                "description": {l2_node_port_id: {}},
            }
            # get interface data from parsing results to add it to description
            for platform, hosts in self.parsed_data.items():
                try:
                    if port_id[1].startswith("MLAG"):
                        link_to_l2_node["description"] = {
                            l2_node_port_id: hosts[port_id[0]]["interfaces"][
                                port_id[1].replace("MLAG", "LAG")
                            ]
                        }
                    else:
                        link_to_l2_node["description"] = {
                            l2_node_port_id: hosts[port_id[0]]["interfaces"][port_id[1]]
                        }
                    break
                except:
                    continue
            link_to_l2_node["description"] = json.dumps(
                link_to_l2_node["description"],
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
            link_to_l2_node_hash = self._make_hash_tuple(link_to_l2_node)
            self.links_dict[link_to_l2_node_hash] = link_to_l2_node
            # connect CDP/LLDP peers to L2 node
            for link_hash in links_hashes:
                # link might be deleted from links_dict by add_lag
                if link_hash in self.links_dict:
                    old_link = self.links_dict.pop(link_hash)
                    _ = old_link.pop("src_label", None)
                    # remove upstream peer interface details from description
                    old_link_data = json.loads(old_link.get("description", {}))
                    _ = old_link_data.pop(l2_node_port_id, None)
                    old_link["description"] = json.dumps(
                        old_link_data, sort_keys=True, indent=4, separators=(",", ": ")
                    )
                    # form new link
                    old_link["source"] = l2_node_id
                    new_link_hash = self._make_hash_tuple(old_link)
                    self.links_dict[new_link_hash] = old_link
                # need to remove this L2 node and links to it as it
                # turned out links are part of LAG, as a result node
                # will be added for LAG together with links to peers
                elif self.add_lag:
                    _ = self.links_dict.pop(link_to_l2_node_hash)
                    _ = self.nodes_dict.pop(l2_node_id)
                    break

        del self.combine_peers_dict

    def _update_drawing(self):
        """
        Method to add formed links and nodes to the drawing object
        """
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
