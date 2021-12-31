"""
CLI IP Data Plugin
******************

This plugin populates diagram with IP related information, such as subnets and IP addresses.

IP data plugin mainly useful in networking domain, it can take show commands output from 
network devices, parse it with TTP templates in a structure that processed further to 
load into one of diagram plugin objects using ``from_dict`` method

Features Supported
------------------

**Support matrix**

+---------------+------------+-----------+-----------+-----------+-----------+
|  Platform     | IP/Subnets |   ARP     | interface | links     | FHRP      |
|  Name         |            |           | config    | grouping  | Protocols |
+===============+============+===========+===========+===========+===========+
| cisco_ios     |    YES     |    YES    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+
| cisco_xr      |    YES     |    ---    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+
| cisco_nxos    |    YES     |    YES    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+
| huawei        |    YES     |    YES    |    YES    |    YES    |    YES    |
+---------------+------------+-----------+-----------+-----------+-----------+
| fortinet      |    YES     |    YES    |    YES    |    YES    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+

Required Commands output
------------------------

cisco_ios:

* ``show running-configuration`` or ``show running-configuration | section interface`` - mandatory output, used to parse interfaces IP addresses
* ``show ip arp`` and/or ``show ip arp vrf xyz`` - required by ARP visualization feature

cisco_xr:

* ``show running-configuration`` or ``show running-configuration interface`` - mandatory output, used to parse interfaces IP addresses
* ``show arp`` and/or ``show arp vrf xyz/all`` - required by ARP visualization feature

cisco_nxos:

* ``show running-configuration`` or ``show running-configuration | section interface`` - mandatory output, used to parse interfaces IP addresses
* ``show ip arp`` - required by ARP visualization feature

huawei:

* ``display current-configuration interface`` - mandatory output, used to parse interfaces IP addresses
* ``display arp all`` - required by ARP visualization feature

fortinet:

* ``get system config``  - mandatory output, used to parse interfaces IP addresses
* ``get system arp`` - required by ARP visualization feature

Sample Usage 
------------

Code to populate yEd diagram object with IP and subnet nodes using data dictionary::

    data = {"huawei": ['''
    <hua_sw1>dis current-configuration interface
    #
    interface Vlanif140
     ip binding vpn-instance VRF_MGMT
     ip address 10.1.1.2 255.255.255.0
     vrrp vrid 200 virtual-ip 10.1.1.1
    #
    interface Eth-Trunk5.123
     vlan-type dot1q 123
     description hua_sw2 BGP  peering
     ip binding vpn-instance VRF_MGMT
     ip address 10.0.0.1 255.255.255.252
     ipv6 address FD00:1::1/126
    #
    interface Eth-Trunk5.200
     vlan-type dot1q 200
     description hua_sw3 OSPF  peering
     ip address 192.168.2.2 255.255.255.252
     
    <hua_sw1>dis arp all
    10.1.1.2        a008-6fc1-1101        I         Vlanif140       VRF_MGMT
    10.1.1.1        a008-6fc1-1102   0    D         Vlanif140       VRF_MGMT
    10.1.1.3        a008-6fc1-1103   10   D/200     Vlanif140       VRF_MGMT
    10.1.1.9        a008-6fc1-1104   10   D/200     Vlanif140       VRF_MGMT
    10.0.0.2        a008-6fc1-1105   10   D/200     Eth-Trunk5.123  VRF_MGMT
        ''',
        '''
    <hua_sw2>dis current-configuration interface
    #
    interface Vlanif140
     ip binding vpn-instance VRF_MGMT
     ip address 10.1.1.3 255.255.255.0
     vrrp vrid 200 virtual-ip 10.1.1.1
    #
    interface Eth-Trunk5.123
     vlan-type dot1q 123
     description hua_sw1 BGP  peering
     ip binding vpn-instance VRF_MGMT
     ip address 10.0.0.2 255.255.255.252
     ipv6 address FD00:1::2/126
        ''',
        '''
    <hua_sw3>dis current-configuration interface
    #
    interface Vlanif200
     ip binding vpn-instance VRF_CUST1
     ip address 192.168.1.1 255.255.255.0
    #
    interface Eth-Trunk5.200
     vlan-type dot1q 200
     description hua_sw1 OSPF  peering
     ip address 192.168.2.1 255.255.255.252
     
    <hua_sw3>dis arp
    192.168.1.1         a008-6fc1-1111       I      Vlanif200 
    192.168.1.10        a008-6fc1-1110   30  D/300  Vlanif200 
        '''],
    "cisco_nxos": ['''
    switch_1# show run | sec interface
    interface Vlan133
      description OOB
      vrf member MGMT_OOB
      ip address 10.133.137.2/24
      hsrp 133
        preempt 
        ip 10.133.137.1
    !
    interface Vlan134
      description OOB-2
      vrf member MGMT_OOB
      ip address 10.134.137.2/24
      vrrpv3 1334 address-family ipv4
        address 10.134.137.1 primary
    !
    interface Vlan222
      description PTP OSPF Routing pat to  siwtch2
      ip address 10.222.137.1/30
    !
    interface Vlan223
      description PTP OSPF Routing pat to siwtch3
      ip address 10.223.137.1/30
     
    switch_1# show ip arp vrf all 
    10.133.137.2    -  d094.7890.1111  Vlan133
    10.133.137.1    -  d094.7890.1111  Vlan133
    10.133.137.30   -  d094.7890.1234  Vlan133
    10.133.137.91   -  d094.7890.4321  Vlan133
    10.134.137.1    -  d094.7890.1111  Vlan134
    10.134.137.2    -  d094.7890.1111  Vlan134
    10.134.137.3   90  d094.7890.2222  Vlan134
    10.134.137.31  91  d094.7890.beef  Vlan134
    10.134.137.81  81  d094.7890.feeb  Vlan134
    10.222.137.2   21  d094.7890.2222  Vlan222
    '''
    }
    
    drawing = create_yed_diagram()
    drawer = cli_ip_data(drawing, add_arp=True, add_fhrp=True)
    drawer.work(data)
    drawer.drawing.dump_file(filename="ip_graph_dc_1.graphml", folder="./Output/")

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
    Class to instantiate IP Data Plugin.

    :param drawing: (obj) - N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    :param ttp_vars: (dict) - dictionary to use as TTP parser object template variables
    :param platforms: (list) - list of platform names to process e.g. ``cisco_ios``, ``cisco_xr`` etc, default is ``_all_``
    :param group_links: (bool) - if True, will group links between same nodes, default is False
    :param add_arp: (bool) - if True, will add IP nodes from ARP parsing results, default is False
    :param label_interface: (bool) - if True, will add interface name to the link's source and target labels, default is False
    :param label_vrf: (bool) - if True, will add VRF name to the link's source and target labels, default is False
    :param collapse_ptp: (bool) - if True (default) combines links for ``/31`` and ``/30`` IPv4 and ``/127`` IPv6 
      subnets into a single ink
    :param add_fhrp: (bool) - if True adds HSRP and VRRP IP addresses to the diagram, default is False
    :param bottom_label_length: (int) - bottom label length of interface description to use for subnet nodes, 
      if False or 0, bottom label will not be set for subnet nodes
    :param lbl_next_to_subnet: (bool) - if True, put link ``port:vrf:ip`` label next to subnet node, default is False
    """

    def __init__(
        self,
        drawing,
        ttp_vars=None,
        group_links=False,
        add_arp=False,
        label_interface=False,
        label_vrf=False,
        collapse_ptp=True,
        add_fhrp=False,
        bottom_label_length=0,
        lbl_next_to_subnet=False,
        platforms=None,
    ):
        self.group_links = group_links
        self.add_arp = add_arp
        self.label_interface = label_interface
        self.label_vrf = label_vrf
        self.collapse_ptp = collapse_ptp
        self.add_fhrp = add_fhrp
        self.bottom_label_length = bottom_label_length
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
        Method to parse text data and add nodes and links to drawing object.

        :param data: (dict or str) dictionary or OS path string to directories with data files

        If data is dictionary, keys must correspond to **Platform** column in
        `Features Supported`_ section table, values are lists of text items to
        process.

        Data dictionary sample::

            data = {
                "cisco_ios" : ["h1", "h2"],
                "cisco_xr": ["h3", "h4"],
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
        if self.collapse_ptp:
            self._collapse_ptp()
        if self.group_links:
            self._group_links()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _parse(self, data):
        """
        Function to parse text data using TTP templates
        
        :param data: (dict or str) data to parse
        """
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
        """
        Method to form graph dictionaries of nodes and links out of parsing results.
        """
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
                        if (
                            interface_data.get("port_description")
                            and self.bottom_label_length
                        ):
                            if (
                                len(interface_data["port_description"])
                                > self.bottom_label_length
                            ):
                                network_node["bottom_label"] = "{}..".format(
                                    interface_data["port_description"][
                                        : self.bottom_label_length
                                    ]
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

    def _add_node(self, item, host_data=None):
        """
        Method to add single node to nodes dictionary if it does not exist or
        update existing node.
        
        :param item: (dict) node dictionary to process
        :param host_data: (dict) dictionary with network device details
        """
        host_data = host_data or {}
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
        """
        Method to add single link to links dictionary.
        
        :param item: (dict) link dictionary to process
        :param network: (str) link subnet value e.g. "10.0.0.0/30"
        """
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
        Method to update nodes_to_links_dict, used by group_links feature.
        
        :param item: (dict) link dictionary
        :param link_hash: (tuple) link identifier hash tuple
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
        Method to combine ptp link into a single link, by default this plugin adds ptp
        subnets as nodes with links to devices that have IP addresses out of that subnet,
        this method deleted ptp subnet node and adds a link between devices instead.
        
        self.collapse_ptp_dict - mapping of ptp networks to link hashes used to combine 
        ptp links.

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
        """
        Method to populate drawing object with processed nodes and links using from_dict method.
        """
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
