"""
CLI IP Data Plugin
******************

This module populates diagram with IP related information, such as subnets and IP addresses.

How it works
------------

IP data plugin mainly useful in networking domain, it can take command line show commands
output from networking devices, parse it with TTP templates and 


Features supported
------------------

**Support matrix**

+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
|  Platform     | IP/Subnets |   ARP     | interface | interface | links     | FHRP      | Reverse   |
|  Name         |            |           | config    | state     | grouping  | Protocols | DNS       |
+===============+============+===========+===========+===========+===========+===========+===========+
| Cisco_IOS     |    YES     |    YES    |    YES    |    ---    |    YES    |    YES    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_IOSXR   |    YES     |    ---    |    YES    |    ---    |    YES    |    YES    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_NXOS    |    YES     |    YES    |    YES    |    ---    |    YES    |    YES    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Huawei        |    YES     |    YES    |    YES    |    ---    |    YES    |    YES    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Fortigate     |    YES     |    YES    |    YES    |    ---    |    YES    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+

Required Commands output
------------------------

Cisco IOS, IOSXR, NXOS:

* 

Huawei:

* 

Fortigate:

* 

Sample Usage 
------------

TBD

API Reference
-------------

.. autoclass:: N2G.plugins.data.cli_ip_data.cli_ip_data
   :members:
"""
if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

import logging
import pprint
import os
import json
import ipaddress

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


class cli_ip_data:
    """

    **Parameters**

    * ``drawing`` - N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    * ``config`` - dictionary of configuration options to define processing behavior
    * ``ttp_vars`` - dictionary to use for TTP parser object template variables

    **config options**

    * ``blbl`` - integer, bottom label length (blbl) of interface description to use for subnet nodes, 
      if False or 0, bottom label will not be set
    * ``lbl_next_to_subnet`` - boolean, put link port:vrf:ip label next to subnet node
    """

    def __init__(
        self,
        drawing,
        config={},
        ttp_vars=None,
        group_links=False,
        add_arp=False,
        label_interface=False,
        label_vrf=False,
        collapse_ptp=True,
        add_fhrp=False,
        blbl=0,
        lbl_next_to_subnet=False,
        platforms=None,
    ):
        self.group_links = group_links
        self.add_arp = add_arp
        self.label_interface = label_interface
        self.label_vrf = label_vrf
        self.collapse_ptp = collapse_ptp
        self.add_fhrp = add_fhrp
        self.blbl = blbl
        self.lbl_next_to_subnet = lbl_next_to_subnet
        self.platforms = platforms or ["_all_"]
        self.ttp_vars = ttp_vars or {
            "IfsNormalize": ttp_templates_vars.short_interface_names
        }
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.nodes_to_links_dict = {}  # used by group_links
        self.collapse_ptp_dict = {}  # used by collapse_ptp

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
        if self.collapse_ptp:
            self._collapse_ptp()
        if self.group_links:
            self._group_links()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _parse(self, data):
        if not HAS_TTP:
            raise ModuleNotFoundError(
                "N2G:cli_ip_data failed importing TTP, is it installed?"
            )
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=self.ttp_vars)
            parser.add_function(
                add_network, scope="group", name="add_network", add_ttp=True
            )
            for platform_name, text_list in data.items():
                if (
                    "_all_" not in self.platforms
                    and not platform_name in self.platforms
                ):
                    continue
                ttp_template = get_template(
                    misc="N2G/cli_ip_data/{}.txt".format(platform_name)
                )
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
                        platform_name = entry.name
                        if (
                            "_all_" not in self.platforms
                            and not platform_name in self.platforms
                        ):
                            continue
                        ttp_template = get_template(
                            misc="N2G/cli_ip_data/{}.txt".format(platform_name)
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
        interfaces_ip = {}  # need this dict to skip ARP entries
        for platform, hosts_data in self.parsed_data.items():
            for hostname, host_data in hosts_data.items():
                self._add_node({"id": hostname, "top_label": "Device"}, host_data)
                for interface, interface_data in host_data["interfaces"].items():
                    interface_networks = []
                    for ip in interface_data.get("ip_addresses", []):
                        network = ip["network"]
                        if self.add_arp or self.add_fhrp:
                            interface_networks.append(network)
                            interfaces_ip.setdefault(network, []).append(ip["ip"])
                        network_node = {"id": network, "top_label": "Subnet"}
                        # add bottom lable to node
                        if interface_data.get("port_description") and self.blbl:
                            if len(interface_data["port_description"]) > self.blbl:
                                network_node["bottom_label"] = "{}..".format(
                                    interface_data["port_description"][: self.blbl]
                                )
                            else:
                                network_node["bottom_label"] = "{}".format(
                                    interface_data["port_description"]
                                )
                        link_description_data = {
                            k: v
                            for k, v in interface_data.items()
                            if not k in ["arp", "ip_addresses"]
                        }
                        link_description_data.update(ip)
                        link_description = {
                            "{}:{}".format(hostname, interface): link_description_data
                        }
                        link_dict = {
                            "source": network,
                            "target": hostname,
                            "description": json.dumps(
                                link_description,
                                sort_keys=True,
                                indent=4,
                                separators=(",", ": "),
                            ),
                        }
                        if ip["netmask"] in ["32", "128"]:
                            network_node["top_label"] = interface
                            network_node["bottom_label"] = interface_data.get(
                                "vrf", "global"
                            )
                        else:
                            link_label = "{}/{}".format(ip["ip"], ip["netmask"])
                            if self.label_vrf:
                                link_label = "{}:{}".format(
                                    interface_data.get("vrf", "global"), link_label
                                )
                            if self.label_interface:
                                link_label = "{}:{}".format(interface, link_label)
                            if self.lbl_next_to_subnet:
                                link_dict["src_label"] = link_label
                            else:
                                link_dict["trgt_label"] = link_label
                        # add new node and link to graph
                        self._add_node(network_node)
                        self._add_link(link_dict, network)
                    # check if need to add FHRP IPs
                    if self.add_fhrp:
                        interface_network_objects = [
                            ipaddress.ip_network(i) for i in interface_networks
                        ]
                        for fhrp_entry in interface_data.get("fhrp", []):
                            # get ip entry network
                            ip = fhrp_entry["ip"]
                            ip_obj = ipaddress.ip_address(ip)
                            network = str(
                                [i for i in interface_network_objects if ip_obj in i][0]
                            )
                            # add IP address node
                            node_id = "{}:{}".format(network, ip)
                            description = {
                                "FHRP:{}:{}".format(hostname, interface): fhrp_entry
                            }
                            self._add_node(
                                {
                                    "id": node_id,
                                    "top_label": "{} VIP".format(fhrp_entry["type"]),
                                    "label": ip,
                                    "description": json.dumps(
                                        description,
                                        sort_keys=True,
                                        indent=4,
                                        separators=(",", ": "),
                                    ),
                                }
                            )
                            # add link to network
                            link_dict = {"source": node_id, "target": network}
                            self._add_link(link_dict)
                    # check if need to add ARP to diagram
                    if self.add_arp:
                        interface_network_objects = [
                            ipaddress.ip_network(i) for i in interface_networks
                        ]
                        for arp_entry in interface_data.get("arp", []):
                            # get arp entry network
                            ip = arp_entry["ip"]
                            ip_obj = ipaddress.ip_address(ip)
                            network = str(
                                [i for i in interface_network_objects if ip_obj in i][0]
                            )
                            # add IP address node
                            node_id = "{}:{}".format(network, ip)
                            description = {
                                "ARP:{}:{}".format(hostname, interface): arp_entry
                            }
                            self._add_node(
                                {
                                    "id": node_id,
                                    "top_label": "ARP entry",
                                    "label": ip,
                                    "description": json.dumps(
                                        description,
                                        sort_keys=True,
                                        indent=4,
                                        separators=(",", ": "),
                                    ),
                                }
                            )
                            # add link to network
                            link_dict = {"source": node_id, "target": network}
                            self._add_link(link_dict)
        # clean up ARP entries that duplicate interface IPs
        if self.add_arp:
            for network, ips in interfaces_ip.items():
                for ip in ips:
                    arp_node_id = "{}:{}".format(network, ip)
                    link_hash = self._make_hash_tuple(
                        {"source": arp_node_id, "target": network}
                    )
                    _ = self.nodes_dict.pop(arp_node_id, None)
                    _ = self.links_dict.pop(link_hash, None)

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
            # merge descriptions
            if "description" in node and "description" in item:
                node["description"] = json.loads(node["description"])
                item["description"] = json.loads(item["description"])
                node["description"].update(item["description"])
                node["description"] = json.dumps(
                    node["description"],
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )

    def _add_link(self, item, network=None):
        link_hash = self._make_hash_tuple(item)
        if link_hash not in self.links_dict:
            self.links_dict[link_hash] = item
        # check if need to pre-process nodes_to_links_dict used by group_links
        if self.group_links:
            self._update_nodes_to_links_dict(item, link_hash)
        if self.collapse_ptp and network:
            if (network.split("/")[1] in ["30", "31"] and "." in network) or (
                network.split("/")[1] in ["127"] and ":" in network
            ):
                self.collapse_ptp_dict.setdefault(network, []).append(link_hash)

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

    def _collapse_ptp(self):
        """
        self.collapse_ptp_dict - mapping of ptp networks to link hashes

        Sample::

            {'10.123.2.2/31': [('', '10.123.2.2/31', '10.123.2.3/31', 'switch_1'),
                            ('', '10.123.2.2/31', '10.123.2.2/31', 'switch_2')],
            '10.123.2.4/31': [('', '10.123.2.4/31', '10.123.2.4/31', 'switch_1'),
                            ('', '10.123.2.4/31', '10.123.2.5/31', 'switch_2')]}
        """
        for network, links in self.collapse_ptp_dict.items():
            if not len(links) == 2:
                continue
            # remove ptp network node
            _ = self.nodes_dict.pop(network)
            # remove old links to ptp network
            # and create new link between devices
            link_1 = self.links_dict.pop(links[0])
            link_2 = self.links_dict.pop(links[1])
            description = {
                **json.loads(link_1.get("description", {})),
                **json.loads(link_2.get("description", {})),
            }
            link_dict = {
                "source": link_1["target"],
                "target": link_2["target"],
                "src_label": link_1["trgt_label"]
                if link_1.get("trgt_label")
                else link_1["src_label"],
                "trgt_label": link_2["trgt_label"]
                if link_2.get("trgt_label")
                else link_2["src_label"],
                "description": json.dumps(
                    description, sort_keys=True, indent=4, separators=(",", ": ")
                ),
            }
            self._add_link(link_dict)

    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
