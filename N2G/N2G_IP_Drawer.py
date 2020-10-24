"""
This module can draw diagrams with IP related information, such as subnets and IP
addresses.

**Support matrix**

+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
|  Platform     | IP/Subnets |   ARP     | interface | interface | links     |   node    | FHRP      |
|  Name         |            |           | config    | state     | grouping  |   facts   | Protocols |
+===============+============+===========+===========+===========+===========+===========+===========+
| Cisco_IOS     |    YES     |    ---    |    YES    |    ---    |    YES    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_IOSXR   |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_NXOS    |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Huawei        |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Juniper       |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+

"""
import logging
import pprint
import os
import json
from ttp import ttp

# initiate logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Custom TTP functions to use in templates:
# -----------------------------------------------------------------------------


def add_network(data):
    if "netmask" in data:
        ip_obj, _ = _ttp_["match"]["to_ip"]("{}/{}".format(data["ip"], data["netmask"]))
    else:
        ip_obj, _ = _ttp_["match"]["to_ip"](data["ip"])
    data["network"] = str(ip_obj.network)
    data["netmask"] = str(ip_obj.network.prefixlen)
    return data, None


# -----------------------------------------------------------------------------
# Main class:
# -----------------------------------------------------------------------------


class ip_drawer:
    """"""

    def __init__(self, drawing, config={}):
        self.config = {
            "group_links": False,
            "add_arp": True,
            "label_interface": False,
            "label_vrf": False,
            "platforms": [
                "_all_"
            ],  # or platforms name, e.g. ["Cisco_IOS", "Cisco_IOSXR"]
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
                "40G": ["^40GE"],
                "Fe": ["^FastEthernet"],
                "Eth": ["^Ethernet", "^eth"],
                "Pt": ["^Port[^-]"],
                "100G": ["^HundredGigE", "^100GE"],
                "mgmt": ["^MgmtEth", "^MEth"],
            }
        }
        self.config.update(config)
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.nodes_to_links_dict = {}  # used by group_links

    def work(self, data):
        """
        Method to parse text data and add nodes and links
        to drawing dictionary

        **Parameters**

        * ``data`` dictionary or OS path string to directories with text files

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

            /path/to/data/
                         |__/Cisco_IOS/<text files>
                         |__/Cisco_IOSXR/<text files>
                         |__/Huawei/<text files>
                         |__/...etc...
        """
        self._parse(data)
        self._form_base_graph_dict()
        # go through config statements
        if self.config.get("group_links"):
            self._group_links()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _open_ttp_template(self, template_name):
        path_to_n2g = os.path.dirname(__file__)
        try:
            if (
                "_all_" not in self.config["platforms"]
                and not template_name in self.config["platforms"]
            ):
                return False
            path = "{}/ttp_templates/IP_Drawer/{}.txt".format(
                path_to_n2g, template_name
            )
            with open(path, "r") as file:
                return file.read()
        except Exception as excptn:
            log.error(
                "Cannot find template for '{}' platform, error - '{}'".format(
                    template_name, excptn
                )
            )
            return False

    def _parse(self, data):
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=self.ttp_vars)
            parser.add_function(
                add_network, scope="group", name="add_network", add_ttp=True
            )
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
            parser.add_function(
                add_network, scope="group", name="add_network", add_ttp=True
            )
            # get all sub-folders and load respective templates
            with os.scandir(data) as dirs:
                for entry in dirs:
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
        for platform, results in self.parsed_data.items():
            # add devices nodes
            for hostname, host_data in results["nodes"].items():
                self._add_node({"id": hostname, "top_label": "Device"}, host_data)
            # add networks and IPs from interfaces configuration
            for network, ips in results["networks"].items():
                is_ptp_net = ips[0]["netmask"] in ["30", "31", "127"]
                # add point-to-point link
                if is_ptp_net and len(ips) == 2:
                    hostname_1 = ips[0].pop("hostname")
                    interface_1 = ips[0].pop("interface")
                    ip_1_data = results["nodes"][hostname_1]["interfaces"][interface_1]
                    ip_1_data.update(ips[0])
                    hostname_2 = ips[1].pop("hostname")
                    interface_2 = ips[1].pop("interface")
                    ip_2_data = results["nodes"][hostname_2]["interfaces"][interface_2]
                    ip_2_data.update(ips[1])
                    description = {
                        "{}:{}".format(hostname_1, interface_1): ip_1_data,
                        "{}:{}".format(hostname_2, interface_2): ip_2_data,
                    }
                    # form labels
                    src_label = "{}/{}".format(
                        ips[0]["ip"], 
                        ips[0]["netmask"]
                    )
                    trgt_label = "{}/{}".format(
                        ips[1]["ip"], 
                        ips[1]["netmask"]
                    )
                    if self.config["label_vrf"]:
                        src_label = "{}:{}".format(
                            ip_1_data.get("vrf", "global"),
                            src_label
                        )
                        trgt_label = "{}:{}".format(
                            ip_2_data.get("vrf", "global"), 
                            trgt_label
                        )
                    if self.config["label_interface"]:
                        src_label = "{}:{}".format(
                            interface_1, 
                            src_label
                        ) 
                        trgt_label = "{}:{}".format(
                            interface_2, 
                            trgt_label
                        )  
                    self._add_link(
                        {
                            "source": hostname_1,
                            "target": hostname_2,
                            "src_label": src_label,
                            "trgt_label": trgt_label,
                            "description": json.dumps(
                                description,
                                sort_keys=True,
                                indent=4,
                                separators=(",", ": "),
                            ),
                        }
                    )
                    continue
                # add network node and links to devices
                network_node = {
                    "id": network, "top_label": "Subnet"
                }
                # add links to devices
                for ip in ips:
                    hostname = ip.pop("hostname")
                    interface = ip.pop("interface")
                    ip_data = results["nodes"][hostname]["interfaces"][interface]
                    ip_data.update(ip)
                    description = {"{}:{}".format(hostname, interface): ip_data}
                    link_dict = {
                        "source": network,
                        "target": hostname,
                        "description": json.dumps(
                            description,
                            sort_keys=True,
                            indent=4,
                            separators=(",", ": "),
                        ),
                    }
                    if ip["netmask"] in ["32", "128"]:
                        network_node["top_label"] = interface
                        network_node["bottom_label"] = ip_data.get("vrf", "global")
                    else:
                        trgt_label = "{}/{}".format(
                            ip["ip"], ip["netmask"]
                        )
                        if self.config["label_vrf"]:
                            trgt_label = "{}:{}".format(
                                ip_data.get("vrf", "global"), trgt_label
                            )                            
                        if self.config["label_interface"]:   
                            trgt_label = "{}:{}".format(
                                interface, trgt_label
                            )                          
                        link_dict["trgt_label"] = trgt_label
                    self._add_link(link_dict)
                self._add_node(network_node)

    def _add_node(self, item, host_data={}):
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

    def _add_link(self, item):
        link_hash = self._make_hash_tuple(item)
        if link_hash not in self.links_dict:
            self.links_dict[link_hash] = item
        # check if need to pre-process nodes_to_links_dict used by group_links
        if self.config.get("group_links"):
            self._update_nodes_to_links_dict(item, link_hash)

    def _update_nodes_to_links_dict(self, item, link_hash):
        """
        Method to update nodes_to_links_dict, used by group_links
        """
        src = item["source"]
        tgt = item["target"]
        nodes_hash = tuple(sorted([src, tgt]))
        self.nodes_to_links_dict.setdefault(nodes_hash, [])
        if not link_hash in self.nodes_to_links_dict[nodes_hash]:
            self.nodes_to_links_dict[nodes_hash].append(link_hash)

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

    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
