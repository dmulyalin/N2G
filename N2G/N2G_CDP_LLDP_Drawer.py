"""

To implement:
- add mac addresses nodes to the diagram based on show mac addr table output, logic - if interface is edge - connected to uncknown or last device, add mac addresses as nodes behind that device
- add invetnry to node facts
- add software version to node facts out of CDP output
"""
import logging
from ttp import ttp
import pprint
import os
import json
import re

# initiate logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Main class:
# -----------------------------------------------------------------------------


class cdp_lldp_drawer:
    """
    Class to process CDP and LLDP neighbors together with
    running configuration and state to produce diagram out of it.

    **Parameters**

    * ``drawing`` - N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    * ``config`` - dictionary of configuration options to define processing behavior

    Supported ``config`` dictionary attributes:

    * ``add_interfaces_data`` - boolean, default ``True``, add interfaces configuration and state data to links
    * ``group_links`` - boolean, default ``False``, group links between nodes
    * ``add_lag`` - boolean, default ``False``, add LAG/MLAG links to diagram
    * ``add_all_connected`` - boolean, default ``False``, add all nodes connected to devices based on interfaces state
    * ``combine_peers`` - boolean, default ``False``, combine CDP/LLDP peers behind same interface by adding L2 node
    * ``platforms`` - list of platforms to work with, by default it is ["_all_"]
    
    **Features support matrix**

    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    |  Platform     |   CDP      |   LLDP    | interface | interface |   LAG     | links     |   node    | MAC       | Add all   |
    |  Name         |   peers    |   peers   | config    | state     |   links   | grouping  |   facts   | addresses | connected |
    +===============+============+===========+===========+===========+===========+===========+===========+===========+===========+
    | Cisco_IOS     |    YES     |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    ---    |    YES    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_IOSXR   |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_NXOS    |    YES     |    YES    |    YES    |    YES    |    YES    |    YES    |    YES    |    ---    |    YES    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_ASA     |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Huawei        |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Juniper       |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+

    **Features description**
    
    * ``CDP peers`` - adds links and nodes out of CDP neighbors
    * ``LLDP peers`` - adds links and nodes out of LLDP neighbors
    * ``interface config`` - adds interfaces configuration to links data
    * ``interface state`` - add links state information to links data
    * ``LAG links`` - combines links based on LAG membership
    * ``links grouping`` - groups links between nodes
    * ``node facts`` - adds information to nodes for vlans, etc
    * ``MAC addresses`` - adds mac addresses nodes to diagram
    * ``Add all connected`` - adds all connected nodes that are not visible on CDP or LLDP

    **Cisco Commands**

    * CDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show cdp neighbor details``
    * LLDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show lldp neighbor details``
    * config, LAG, grouping for Cisco IOS, IOS-XR, NXOS, ASA - ``show running-configuration``
    * state for Cisco IOS, IOS-XR, NXOS - ``show interface``

    **Huawei Commands**

    * LLDP - ``display lldp neighbor details``
    * config, LAG, grouping - ``display current-configuration``
    * state - ``display interface``
    """

    def __init__(self, drawing, config={}):
        # init attributes
        self.config = {
            "add_interfaces_data": True,
            "group_links": False,
            "add_lag": False,
            "add_all_connected": False,
            "combine_peers": False,
            "platforms": ["_all_"] # or platforms name, e.g. ["Cisco_IOS", "Cisco_IOSXR"]
        }
        self.ttp_vars = {
            "IfsNormalize": {
                "Lo": ["^Loopback"],
                "Ge": ["^GigabitEthernet", "^Gi"],
                "LAG": [
                    "^Eth-Trunk",
                    "^port-channel",
                    "^Port-channel",
                    "^Bundle-Ether",
                ],
                "Te": [
                    "^TenGigabitEthernet",
                    "^TenGe",
                    "^10GE",
                    "^TenGigE",
                    "^XGigabitEthernet",
                ],
                "Fe": ["^FastEthernet"],
                "Eth": ["^Ethernet", "^eth"],
                "Pt": ["^Port[^-]"],
                "100G": ["^HundredGigE"],
            },
            "physical_ports": ["Ge", "Te", "Fe", "Eth", "100G"],
        }
        self.config.update(config)
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.lag_links_dict = {} # used by add_lag method
        self.nodes_to_links_dict = {} # used by group_links
        self.combine_peers_dict = {} # used by combine_peers

    def work(self, data):
        """
        Method to parse text data and add nodes and links
        to drawing dictionary
        
        **Parameteres**
        
        * ``data`` dictionary or OS path string to directory with text files
        
        If data is dictionary, keys must correspond to "Platform" column in
        *Supported platforms* table, values are lists of text items to
        process.
        
        Data dictionary sample::
        
            data = {
                "Cisco_IOS" : ["h1", "h2"],
                "Cisco_IOS-XR": ["h3", "h4"],
                "Cisco_NXOS": ["h5", "h6"],
                ...etc...
            }
        
        Where ``hX`` devices show commands output.
        
        If data is a string with OS path to directory, child directories names
        must correspond to "Platform" column in *Supported platforms* table.
        Each child directory should contain text files with show commands output
        for each device.
        
        Directories structure sample::
        
            /data/
                 |_/Cisco_IOS/<text files>
                 |_/Cisco_IOSXR/<text files>
                 |_/Huawei/<text files>
                 |_/...etc...
        """
        self._parse(data)
        self._form_base_graph_dict()
        # go through config statements
        if self.config.get("add_lag"):
            self._add_lags_to_links_dict()
        if self.config.get("group_links"):
            self._group_links()
        if self.config.get("add_all_connected"):
            self._add_all_connected()
        if self.config.get("combine_peers"):
            self._combine_peers()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _open_ttp_template(self, template_name):
        path_to_n2g = os.path.dirname(__file__)
        try:
            if not "_all_" in self.config["platforms"] and not template_name in self.config["platforms"]:
                return False
            path = "{}/ttp_templates/CDP_LLDP_Drawer/{}.txt".format(
                path_to_n2g, template_name
            )
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            log.error(
                "Cannot find template for '{}' platform, error - '{}'".format(
                    template_name, e
                )
            )        
            return False

    def _parse(self, data):
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=self.ttp_vars)
            for platform_name, text_list in data.items():
                ttp_template = self._open_ttp_template(platform_name)
                if not ttp_template:
                    continue
                parser.add_template(template=ttp_template, template_name=platform_name)
                for item in text_list:
                    parser.add_input(item, template_name=platform_name)
        # process directories at OS path
        elif isinstance(data, str):
            parser = ttp(vars=self.ttp_vars, base_path=data)
            # get all sub-folders and load respective templates
            with os.scandir(data) as it:
                for entry in it:
                    if entry.is_dir():
                        ttp_template = self._open_ttp_template(entry.name)
                        if not ttp_template:
                            continue
                        parser.add_template(
                            template=ttp_template, template_name=entry.name
                        )
        else:
            log.error(
                "Expecting dictionary or string, but '{}' given".format(type(data))
            )
            return
        parser.parse(one=True)
        self.parsed_data = parser.result(structure="dictionary")
        # pprint.pprint(self.parsed_data, width = 100)

    def _make_hash_tuple(self, item):
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
            for k, v in item.items():
                if not k in node:
                    node[k] = v
            if not "description" in node and host_data.get("node_facts"):
                node["description"] = json.dumps(
                    host_data["node_facts"],
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )

    def _add_link(self, item, hosts, host_data):
        link_hash = self._make_hash_tuple(item)
        if not link_hash in self.links_dict:
            self.links_dict[link_hash] = {
                "source": item["source"],
                "target": item["target"]["id"],
                "src_label": item["src_label"],
                "trgt_label": item["trgt_label"],
            }
        # check if need to add interfaces data
        if self.config.get("add_interfaces_data"):
            self._add_interfaces_data(item, hosts, host_data, link_hash)
        # check if need to pre-process lag_links_dict used by add_lag
        if self.config.get("add_lag"):
            self._update_lag_links_dict(item, hosts, host_data, link_hash)
        # check if need to pre-process nodes_to_links_dict used by group_links
        if self.config.get("group_links"):
            self._update_nodes_to_links_dict(item, link_hash)
        # check if need to combine peers, preprocess combine_peers_dict
        if self.config.get("combine_peers"):
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

    def _update_lag_links_dict(self, item, hosts, host_data, link_hash):
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
        # add lag link to links dictionary
        if lag_link:
            lag_link_hash = self._make_hash_tuple(lag_link)
            src_member_intf_name = "{}:{}".format(src, src_intf_name)
            tgt_member_intf_name = "{}:{}".format(tgt, tgt_intf_name)
            member_link = {src_member_intf_name: tgt_member_intf_name}
            if not lag_link_hash in self.lag_links_dict:
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
                    if "lag_id" in intf_data and self.config["add_lag"]:
                        lag_intf_name = "LAG{}".format(intf_data["lag_id"])
                        src_if = "{}:{}".format(hostname, lag_intf_name)                      
                        lag_intf_data = host_data["interfaces"].get(lag_intf_name, {})
                        if "mlag_id" in lag_intf_data:
                            lag_intf_name = "MLAG{}".format(lag_intf_data["mlag_id"])
                        link["src_label"] = lag_intf_name
                        link["description"] = json.dumps(
                                {
                                    src_if: lag_intf_data,
                                    "lag_members": {"{}:{}".format(hostname, intf_name): ""}
                                },
                                sort_keys=True,
                                indent=4,
                                separators=(",", ": "),
                            )
                        # update node bottom label as per lag interface description
                        node["bottom_label"] = "{}..".format(
                            lag_intf_data["description"][:20]
                        ) if lag_intf_data else node["bottom_label"]
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
                    if not link_hash in self.links_dict:
                        self.links_dict[link_hash] = link
                    else:
                        link_data = json.loads(self.links_dict[link_hash]["description"])
                        if "lag_members" in link_data:
                            link_data["lag_members"].update({"{}:{}".format(hostname, intf_name): ""})
                        self.links_dict[link_hash]["description"] = json.dumps(
                                link_data,
                                sort_keys=True,
                                indent=4,
                                separators=(",", ": "),
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
            self._add_node(
                item={
                    "id": l2_node_id,
                    "label": "L2",
                    "shape_type": "ellipse",
                    "height": 40,
                    "width": 40
                }, 
                host_data={}
            )
            # add link to L2 node
            link_to_l2_node = {
                "source": port_id[0],
                "target": l2_node_id,
                "src_label": port_id[1]
            }
            for platform, hosts in self.parsed_data.items():
                try:
                    link_to_l2_node_data = {
                        "{}:{}".format(*port_id): hosts[port_id[0]]["interfaces"][port_id[1]]
                    }
                    link_to_l2_node["description"] = json.dumps(
                        link_to_l2_node_data,
                        sort_keys=True,
                        indent=4,
                        separators=(",", ": "),                        
                    )
                    break
                except:
                    continue
            link_to_l2_node_hash = self._make_hash_tuple(link_to_l2_node)
            self.links_dict[link_to_l2_node_hash] = link_to_l2_node
            # connect CDP/LLDP peers to L2 node
            for link_hash in links_hashes:
                old_link = self.links_dict.pop(link_hash)
                _ = old_link.pop("src_label")
                old_link["source"] = l2_node_id
                new_link_hash = self._make_hash_tuple(old_link)
                self.links_dict[new_link_hash] = old_link
        del self.combine_peers_dict
                
    
    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
