"""
CLI OSPFv2 LSDB Data Plugin
***************************

CLI OSPFv2 LSDB Data Plugin can process network devices CLI output of OSPFv2 LSDB content to 
populate N2G drawing with OSPF topology nodes and links.

CLI output from devices parsed using TTP Templates into a dictionary structure.

After parsing, results processed further to form a dictionary of nodes and links keyed 
by unique nodes and links identifiers wit values being nodes dictionaries and for links
it is a list of dictionaries of links between same pair of nodes. For nodes OSPF RID 
used as a unique ID, for links it is sorted tuple of ``source``, ``target`` and ``label`` 
keys' values. This structure helps to eliminate duplicates.

Next step is post processing, such as packing links between nodes. By default cli_ospf_data
tries to match and pack nodes based on the IP addresses and their subnets, it checks
if IP addresses are part of same subnet using prefix lengths - 31, 30, 29, ... 22 - if
IP addresses happens to be part of same subnet, link packed in one link.

Last step is to populate N2G drawing with new nodes and links using ``from_dict`` method.

Features Supported
------------------

**Support matrix**

+---------------+------------+------------+------------+------------+-----------+-----------+
| Platform      | Router     | OSPF       | External   | Summary    | interface | interface |
| Name          | LSA        | Peers      | LSA        | LSA        | config    | state     |
+===============+============+============+============+============+===========+===========+
| cisco_ios     |     YES    |     ---    |     ---    |     ---    |    ---    |    ---    |
+---------------+------------+------------+------------+------------+-----------+-----------+
| cisco_xr      |     YES    |     ---    |     ---    |     ---    |    ---    |    ---    |
+---------------+------------+------------+------------+------------+-----------+-----------+
| cisco_nxos    |     ---    |     ---    |     ---    |     ---    |    ---    |    ---    |
+---------------+------------+------------+------------+------------+-----------+-----------+
| huawei        |     YES    |     ---    |     ---    |     ---    |    ---    |    ---    |
+---------------+------------+------------+------------+------------+-----------+-----------+

Required Commands output
------------------------

cisco_ios:

* ``show ip ospf database router`` - mandatory, used to source nodes and links for topology
* ``show ip ospf database summary``
* ``show ip ospf database external``

cisco_xr:

* ``show ospf database router`` - mandatory, used to source nodes and links for topology
* ``show ospf database summary``
* ``show ospf database external``

huawei:

* ``display ospf lsdb router`` - mandatory, used to source nodes and links for topology

Sample usage
------------

Code to populate yEd diagram object with OSPF LSDB sourced nodes and links::

    from N2G import cli_l2_data, yed_diagram

    data = {"cisco_xr": ['''
    RP/0/RP0/CPU0:router-1#show ospf database router 
    
                OSPF Router with ID (10.0.1.1) (Process ID 1)
    
                    Router Link States (Area 0.0.0.0)
    
      LS age: 406
      Options: (No TOS-capability, DC)
      LS Type: Router Links
      Link State ID: 10.0.1.1
      Advertising Router: 10.0.1.1
      LS Seq Number: 8000010c
      Checksum: 0x24dd
      Length: 132
       Number of Links: 9
    
        Link connected to: another Router (point-to-point)
         (Link ID) Neighboring Router ID: 10.0.1.4
         (Link Data) Router Interface address: 0.0.0.12
          Number of TOS metrics: 0
           TOS 0 Metrics: 1100
    
        Link connected to: another Router (point-to-point)
         (Link ID) Neighboring Router ID: 10.0.1.2
         (Link Data) Router Interface address: 0.0.0.10
          Number of TOS metrics: 0
           TOS 0 Metrics: 1100    
    
      Routing Bit Set on this LSA
      LS age: 1604
      Options: (No TOS-capability, DC)
      LS Type: Router Links
      Link State ID: 10.0.1.2
      Advertising Router: 10.0.1.2
      LS Seq Number: 8000010b
      Checksum: 0xdc96
      Length: 132
       Number of Links: 9
    
        Link connected to: another Router (point-to-point)
         (Link ID) Neighboring Router ID: 10.0.1.3
         (Link Data) Router Interface address: 0.0.0.52
          Number of TOS metrics: 0
           TOS 0 Metrics: 1100
    
        Link connected to: another Router (point-to-point)
         (Link ID) Neighboring Router ID: 10.0.1.4
         (Link Data) Router Interface address: 0.0.0.53
          Number of TOS metrics: 0
           TOS 0 Metrics: 1100
        ''']
    }

    drawing = yed_diagram()
    drawer = cli_ospf_data(drawing)
    drawer.work(data)
    drawer.drawing.dump_file()
    
API Reference
-------------

.. autoclass:: N2G.plugins.data.cli_ospf_data.cli_ospf_data
   :members:
"""
import logging
import json
import os
import csv
import ipaddress
from fnmatch import fnmatchcase

try:
    from ttp import ttp
    from ttp_templates import get_template

    HAS_TTP = True
except ImportError:
    HAS_TTP = False

# initiate logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Main class:
# -----------------------------------------------------------------------------


class cli_ospf_data:
    """
    Main class to instantiate OSPFv2 LSDB CLI Data Plugin object.

    :param drawing: (obj) N2G Diagram object
    :param ttp_vars: (dict) Dictionary to use as vars attribute while instantiating TTP parser object
    :param ip_lookup_data: (dict or str) IP Lookup dictionary or OS path to CSV file
    :param add_connected: (bool) if True, will add connected subnets as nodes, default is False    
    :param ptp_filter: (list) list of glob patterns to filter point-to-point links based on link IP
    :param add_data: (bool) if True (default) adds data information to nodes and links
    
    ``ip_lookup_data`` dictionary must be keyed by OSPF RID IP address, with values
    being dictionary which must contain ``hostname`` key with optional additional keys 
    to use for N2G diagram module node, e.g. ``label``, ``top_label``, ``bottom_label``, 
    ``interface``etc. If ``ip_lookup_data`` is an OS path to CSV file, that file's first 
    column header must be ``ip`` , file must contain ``hostname`` column, other columns 
    values set to N2G diagram module node attributes, e.g. ``label``, ``top_label``, 
    ``bottom_label``, ``interface`` etc. 
    
    If lookup data contains ``interface`` key, it will be added to link label.
        
    Sample ip_lookup_data dictionary::
    
        {
            "1.1.1.1": {
                "hostname": "router-1",
                "bottom_label": "1 St address, City X",
                "interface": "Gi1"
            }
        }

    Sample ip_lookup_data CSV file::

        ip,hostname,bottom_label,interface
        1.1.1.1,router-1,"1 St address, City X",Gi1
        
    ``ptp_filter`` default list of patterns are:
    
    * ``0*`` - Cisco MPLS TE forwarding adjacencies links
    * ``112*`` - huawei DCN OSPF links
    """

    def __init__(
        self,
        drawing,
        ttp_vars: dict = None,
        ip_lookup_data: dict = None,
        add_connected: bool = False,
        ptp_filter: list = None,
        add_data: bool = True,
    ):
        self.ttp_vars = ttp_vars or {}
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.add_connected = add_connected
        self.ptp_filter = ptp_filter or ["0*", "112*"]
        self.add_data = add_data
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.ip_lookup_data = ip_lookup_data or {}
        self._load_ip_lookup_data()

    def _load_ip_lookup_data(self) -> None:
        """
        Helper function to load CSV table in a dictionary keyed
        by values in first column. This dictionary further used
        to perform IP to node details lookup for OSPF router ID.
        """
        # load lookup data
        if self.ip_lookup_data and isinstance(self.ip_lookup_data, str):
            with open(self.ip_lookup_data) as f:
                reader = csv.DictReader(f)
                self.ip_lookup_data = {r["ip"]: r for r in reader if "ip" in r}

    def work(self, data):
        """
        Method to parse OSPF LSDB data and add nodes and links to N2G drawing.

        :param data: (dict or str) dictionary keyed by platform name or OS path
            string to directories with text files

        If data is dictionary, keys must correspond to "Platform" column in
        *Supported platforms* table, values are lists of text items to
        process.

        Data dictionary sample::

            data = {
                "cisco_ios" : ["h1", "h2"],
                "cisco_ios": ["h3", "h4"],
                "cisco_nxos": ["h5", "h6"],
                ...etc...
            }

        Where ``hX`` device's show commands output.

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
        self._pack_links()
        if self.ip_lookup_data:
            self._lookup_rid()
            self._lookup_ip_interfaces()
        self._update_drawing()

    def _make_hash_tuple(self, data: dict) -> tuple:
        """
        Helper function to form Edge tuple to use as a hash to
        identify all the links between same pair of nodes using
        ``source``, ``target`` and ``label`` keys' values.

        :param data: (dict) link dictionary with source, target and label keys
        """
        return tuple(sorted([data["source"], data["target"], data.get("label", "")]))

    def _parse(self, data: [dict, str]) -> None:
        """
        Method to parse data using TTP Templates

        :param data: (dict or str) dictionary of data items or OS
            path to folders with data to parse
        :return: None
        """
        if not HAS_TTP:
            raise ModuleNotFoundError(
                "N2G:cli_ospf_data failed importing TTP, is it installed?"
            )
        parser = ttp(vars=self.ttp_vars, log_level="ERROR")
        # process data dictionary
        if isinstance(data, dict):
            for platform_name, text_list in data.items():
                ttp_template = get_template(
                    misc="N2G/cli_ospf_data/{}.txt".format(platform_name)
                )
                parser.add_template(template=ttp_template, template_name=platform_name)
                for item in text_list:
                    parser.add_input(item, template_name=platform_name)
        # process directories at OS path
        elif isinstance(data, str):
            # get all sub-folders and load respective templates
            with os.scandir(data) as dirs:
                for entry in dirs:
                    if entry.is_dir():
                        platform_name = entry.name
                        ttp_template = get_template(
                            misc="N2G/cli_ospf_data/{}.txt".format(platform_name)
                        )
                        parser.add_template(
                            template=ttp_template, template_name=platform_name
                        )
                        parser.add_input(
                            data=os.path.abspath(entry), template_name=platform_name
                        )
        else:
            raise TypeError(
                "Expecting dictionary or string, but '{}' given".format(type(data))
            )
        parser.parse(one=True)
        self.parsed_data = parser.result(structure="flat_list")
        # import pprint; pprint.pprint(self.parsed_data, width = 100)

    def _process_router_lsa(
        self, router_lsa: dict, ospf_pid: str, ospf_data: dict, device: dict
    ) -> None:
        """"""
        # make node out of router LSA
        self._add_node(
            node={
                "id": router_lsa["originator_rid"],
                "label": router_lsa["originator_rid"],
                "bottom_label": "Node",
            },
            node_data={
                "lsdb_source": {
                    "hostname": self.ip_lookup_data.get(ospf_data["local_rid"], {}).get(
                        "hostname"
                    ),
                    "ospf_rid": ospf_data["local_rid"],
                    "ospf_pid": ospf_pid,
                },
                **router_lsa,
            },
        )
        # go over PTP peers
        for ptp_peer in router_lsa.get("ptp_peers", []):
            # ignore OSPF adjacencies
            if any([fnmatchcase(ptp_peer["link_data"], p) for p in self.ptp_filter]):
                continue
            self._add_link(
                link={
                    "source": router_lsa["originator_rid"],
                    "src_label": "{}:{}".format(
                        ptp_peer["link_data"], ptp_peer["metric"]
                    ),
                    "label": "A:{}".format(router_lsa["area"]),
                    "target": ptp_peer["link_id"],
                    "source_ip": ptp_peer["link_data"],
                }
            )
        # go over BMA peers
        for bma_peer in router_lsa.get("bma_peers", []):
            # find BMA subnet
            bma_ip = ipaddress.IPv4Address(bma_peer["link_id"])
            bma_subnet = ""
            for connet in router_lsa.get("connected_stub", []):
                net = ipaddress.IPv4Network(
                    "{}/{}".format(connet["link_id"], connet["link_data"])
                )
                if bma_ip in net:
                    bma_subnet = str(net)
                    break
            # add BMA DR Node
            self._add_node(
                node={
                    "id": "DR {}".format(bma_peer["link_id"]),
                    "label": "DR {}".format(bma_peer["link_id"]),
                    "bottom_label": "DR Node",
                    "top_label": bma_subnet,
                }
            )
            self._add_link(
                link={
                    "source": router_lsa["originator_rid"],
                    "src_label": "{}:{}".format(
                        bma_peer["link_data"], bma_peer["metric"]
                    ),
                    "label": "A:{}".format(router_lsa["area"]),
                    "target": "DR {}".format(bma_peer["link_id"]),
                }
            )
        # go over connected subnets
        if self.add_connected:
            # form a list of IP address for router ptp links and BMA subnets
            node_peering_ip = [
                ipaddress.IPv4Address(i["link_data"])
                for i in router_lsa.get("ptp_peers", [])
                if not i["link_data"].startswith("0.")
            ]
            node_peering_ip.extend(
                [
                    ipaddress.IPv4Address(i["link_id"])
                    for i in router_lsa.get("bma_peers", [])
                ]
            )
            for connet in router_lsa.get("connected_stub", []):
                net = ipaddress.IPv4Network(
                    "{}/{}".format(connet["link_id"], connet["link_data"])
                )
                # filter networks that already formed ptp links
                for ip in node_peering_ip:
                    if ip in net:
                        break
                else:
                    # add subnet node and links if its not used to form ptp or BMA peering
                    self._add_node(
                        node={
                            "id": str(net),
                            "label": str(net),
                            "bottom_label": "Subnet",
                        }
                    )
                    self._add_link(
                        link={
                            "source": router_lsa["originator_rid"],
                            "src_label": "M:{}".format(connet["metric"]),
                            "label": "A:{}".format(router_lsa["area"]),
                            "target": str(net),
                        }
                    )

    def _process_external_lsa(
        self, external_lsa: dict, ospf_pid: str, ospf_data: dict, device: dict
    ) -> None:
        pass

    def _process_summary_lsa(
        self, summry_lsa: dict, ospf_pid: str, ospf_data: dict, device: dict
    ) -> None:
        pass

    def _form_base_graph_dict(self) -> None:
        for device in self.parsed_data:
            # go over all OSPF processes on the box
            for ospf_pid, ospf_data in device.get("ospf_processes", {}).items():
                # process LSA
                for router_lsa in ospf_data.get("router_lsa", []):
                    self._process_router_lsa(router_lsa, ospf_pid, ospf_data, device)
                for external_lsa in ospf_data.get("external_lsa", []):
                    self._process_external_lsa(
                        external_lsa, ospf_pid, ospf_data, device
                    )
                for summry_lsa in ospf_data.get("summry_lsa", []):
                    self._process_summary_lsa(summry_lsa, ospf_pid, ospf_data, device)

    def _add_node(self, node: dict, node_data: dict = {}) -> None:
        # add new node
        if not node["id"] in self.nodes_dict:
            if node_data and self.add_data:
                node["description"] = json.dumps(
                    node_data, sort_keys=True, indent=4, separators=(",", ": ")
                )
            self.nodes_dict[node["id"]] = node
        # update node attributes if they do not exists already
        else:
            stored_node = self.nodes_dict[node["id"]]
            for key, value in node.items():
                if not key in stored_node:
                    stored_node[key] = value
            if not "description" in stored_node and node_data and self.add_data:
                stored_node["description"] = json.dumps(
                    node_data, sort_keys=True, indent=4, separators=(",", ": ")
                )

    def _add_link(self, link: dict, link_data: dict = {}) -> None:
        link_hash = self._make_hash_tuple(link)
        self.links_dict.setdefault(link_hash, [])
        if link not in self.links_dict[link_hash]:
            if link_data and self.add_data:
                link["description"] = json.dumps(
                    link_data, sort_keys=True, indent=4, separators=(",", ": ")
                )
            self.links_dict[link_hash].append(link)

    def _pack_links(self) -> None:
        """
        Method to iterate over links between node pairs and pack links based
        on these criteria:
          - combine links for /30 or /29 subnets
        """
        for hash in self.links_dict.keys():
            links = self.links_dict[hash]
            # continue if only one link between node pairs
            if len(links) <= 1:
                continue
            self.links_dict[hash] = []
            while links:
                link = links.pop()
                pair_link_index = None
                link_ip_addr = link.pop("source_ip")
                # try to match on subnets
                for m in [31, 30, 29, 28, 27, 26, 25, 24, 23, 22]:
                    link_ip = ipaddress.IPv4Interface("{}/{}".format(link_ip_addr, m))
                    for link_2 in links:
                        link_2_ip = ipaddress.IPv4Interface(
                            "{}/30".format(link_2["source_ip"])
                        )
                        if link_2_ip in link_ip.network:
                            link["trgt_label"] = link_2["src_label"]
                            self._add_link(
                                link=link,
                                link_data={
                                    "subnet": str(link_ip.network),
                                    "ospf_area": link["label"].split(":")[1],
                                    "source_rid": link["source"],
                                    "target_rid": link["target"],
                                    "source_ip": str(link_ip.ip),
                                    "target_ip": str(link_2_ip.ip),
                                },
                            )
                            pair_link_index = links.index(link_2)
                            break
                    if pair_link_index:
                        break
                # remove link from links if it was combined
                if pair_link_index is not None:
                    _ = links.pop(pair_link_index)
                # add link back to links if have not found a match for it
                else:
                    self._add_link(link)

    def _lookup_rid(self):
        """
        Method to lookup RID in lookup data and use hostname as label and ID,
        this method also updates all the links with hostnames as source and target
        node IDs
        """
        for node in self.nodes_dict.values():
            if node["id"] in self.ip_lookup_data:
                node_id = node["id"]
                node["id"] = self.ip_lookup_data[node_id].get("hostname", node_id)
                node["label"] = self.ip_lookup_data[node_id].get(
                    "hostname", node["label"]
                )
                node.update(
                    {
                        k: v
                        for k, v in self.ip_lookup_data[node_id].items()
                        if k != "interface"
                    }
                )
        for links in self.links_dict.values():
            for link in links:
                if link["source"] in self.ip_lookup_data:
                    link["source"] = self.ip_lookup_data[link["source"]].get(
                        "hostname", link["source"]
                    )
                if link["target"] in self.ip_lookup_data:
                    link["target"] = self.ip_lookup_data[link["target"]].get(
                        "hostname", link["target"]
                    )

    def _lookup_ip_interfaces(self):
        """
        Method to search for link IP addresses in lookup table and add 
        interface details to the link labels.
        """
        for links in self.links_dict.values():
            for link in links:
                # modify source label
                if link.get("src_label"):
                    link_src_ip, link_src_metric = link["src_label"].split(":")
                    if self.ip_lookup_data.get(link_src_ip, {}).get("interface"):
                        link["src_label"] = "{}:{}:{}".format(
                            self.ip_lookup_data[link_src_ip]["interface"],
                            link_src_ip,
                            link_src_metric,
                        )
                # modify target label
                if link.get("trgt_label"):
                    link_trgt_ip, link_trgt_metric = link["trgt_label"].split(":")
                    if self.ip_lookup_data.get(link_trgt_ip, {}).get("interface"):
                        link["trgt_label"] = "{}:{}:{}".format(
                            self.ip_lookup_data[link_trgt_ip]["interface"],
                            link_trgt_ip,
                            link_trgt_metric,
                        )

    def _update_drawing(self):
        """
        Method to add formed links and nodes to the drawing object
        """
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        for i in self.links_dict.values():
            self.graph_dict["links"].extend(i)
        # import pprint; pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)
