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
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    
import logging
import pprint
import os
import json
from ttp import ttp
from N2G import N2G_utils
import ipaddress

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
    """
    
    **Parameters**

    * ``drawing`` - N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    * ``config`` - dictionary of configuration options to define processing behavior
    * ``ttp_vars`` - dictionary to use for TTP parser object template variables
    """
    def __init__(self, drawing, config={}, ttp_vars=None):
        self.config = {
            "group_links": False,
            "add_arp": False,
            "label_interface": False,
            "label_vrf": False,
            "subnet_bt": False,
            "platforms": [
                "_all_"
            ],  # or platforms name, e.g. ["Cisco_IOS", "Cisco_IOSXR"]
        }
        self.ttp_vars = ttp_vars or N2G_utils.ttp_variables
        self.config.update(config)
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.nodes_to_links_dict = {}  # used by group_links
        self.add_arp_networks = {} # used by add_arp

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
        if self.config.get("add_arp"):
            self._add_arp()
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
                    # form link description
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
                    # add networks to add_arp_networks dict - used by add_arp feature
                    if self.config.get("add_arp"):
                        self.add_arp_networks.setdefault(hostname_1, {}).setdefault(interface_1, set()).add(network)
                        self.add_arp_networks.setdefault(hostname_2, {}).setdefault(interface_2, set()).add(network)
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
                    # form link dictionary
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
                    # add networks to add_arp_networks dict - used by add_arp feature
                    if self.config.get("add_arp"):
                        self.add_arp_networks.setdefault(hostname, {}).setdefault(interface, set()).add(network)  
                # add bottom label to subnet out of last port description
                if self.config.get("subnet_bt"):
                    network_node["bottom_label"] = "{}..".format(ip_data["port_description"][:19])
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
            
    def _add_arp(self):
        """
        Method to process ARP entries, uses self.add_arp_networks dictionary
        to find network arp entry belongs to and find already added IPs.
        
        self.add_arp_networks sample content::
        
            {'switch_1': {'SVI123': {'ips': {'10.123.111.1',
                                            '10.123.222.1',
                                            '10.123.233.1'},
                                    'networks': {'10.123.111.0/24',
                                                '10.123.222.0/24',
                                                '10.123.233.0/24'}},
                        'Te1/1/5': {'ips': {'10.1.33.1'}, 'networks': {'10.1.33.0/24'}},
                        'Te1/1/7': {'ips': {'10.1.234.1'},
                                    'networks': {'10.1.234.0/24'}}},
            'switch_2': {'SVI11': {'ips': {'10.11.11.1'}, 'networks': {'10.11.11.0/24'}},
                        'SVI22': {'ips': {'10.22.22.1'}, 'networks': {'10.22.22.0/24'}},
                        'Te1/1/71': {'ips': {'10.1.234.2'},
                                    'networks': {'10.1.234.0/24'}}}}
        """
        for platform, results in self.parsed_data.items():
            # add devices nodes
            for arp_entry in results["arp"]:
                hostname = arp_entry.pop("hostname")
                interface = arp_entry.pop("interface")
                ip = arp_entry["ip"]            
                # find network ARP entry IP belongs to
                if len(self.add_arp_networks[hostname][interface])  == 1:
                    network = list(self.add_arp_networks[hostname][interface])[0]
                elif len(self.add_arp_networks[hostname][interface]) > 1:
                    nets = self.add_arp_networks[hostname][interface]
                    self.add_arp_networks[hostname][interface] = [
                        ipaddress.ip_network(net) for net in nets
                    ]
                    ip_obj = ipaddress.ip_address(ip)
                    for net in self.add_arp_networks[hostname][interface]:
                        # check if arp entry IP is part of given network
                        if ip_obj in net:
                            network = str(net)
                            break
                # skip IP addresses already added from config
                already_added = False
                for added_ip in results["networks"][network]:
                    if ip == added_ip["ip"].split("/")[0]:
                        already_added = True
                        break
                if already_added:
                    continue    
                # add IP address node
                node_id = "{}:{}".format(network, ip)
                description = {
                    "{}:{}".format(hostname, interface): arp_entry
                }
                self._add_node({
                    "id": node_id,
                    "top_label": "ARP entry",
                    "label": ip,
                    "description": json.dumps(
                        description, sort_keys=True, indent=4, separators=(",", ": ")
                    )
                })
                # add link to network
                link_dict = {
                        "source": node_id,
                        "target": network
                    }
                self._add_link(link_dict)
                
                    
    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
