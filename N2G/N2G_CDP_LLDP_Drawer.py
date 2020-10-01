import logging
from ttp import ttp
import pprint
import os
import json
import re

# initiate logging
log = logging.getLogger(__name__)
LOG_LEVEL = "ERROR"


def logging_config(LOG_LEVEL):
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL.upper() in valid_log_levels:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [N2G_CDP_Drawer %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=LOG_LEVEL.upper(),
        )


logging_config(LOG_LEVEL)


# =============================================================================
# TTP PARSER TEMPLATES:
# =============================================================================

Cisco_IOS = """
<template name="Cisco_IOS" results="per_template">
<vars>local_hostname="gethostname"</vars>

<input>url = "./Cisco_IOS/"</input>

<group name="{{ local_hostname }}.interfaces**.{{ interface }}">
interface {{ interface | resuball(IfsNormalize) }}
 description {{ description | re(".+") }}
 switchport {{ is_l2 | set(True) }}
 switchport access vlan {{ access_vlan }}
 switchport mode {{ l2_mode }}
 vrf forwarding {{ vrf }}
 ip address {{ ip | PHRASE | joinmatches(",") }}
 ip address {{ ip | PHRASE | joinmatches(",") }} secondary
 switchport trunk allowed vlan {{ trunk_vlans | unrange("-", ",") | joinmatches(",") }}
 channel-group {{ lag_id }} mode {{ lag_mode }}
 mtu {{ mtu }}
</group>

<!--state group:
<group name="{{ local_hostname }}.interfaces**.{{ interface }}">

</group>
-->

<group name="{{ local_hostname }}.cdp_peers*" expand="">
Device ID: {{ target.id }}
  IP address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }},  Capabilities: {{ ignore(ORPHRASE) }}
Interface: {{ src_label | resuball(IfsNormalize) }},  Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
{{ source | set("local_hostname") }}
</group>
</template>
"""


# =============================================================================
# COMMON TTP PARSER Variables:
# =============================================================================

ttp_vars = {
    "IfsNormalize": {
        "Lo": ["^Loopback"],
        "Ge": ["^GigabitEthernet"],
        "LAG": ["^Eth-Trunk", "^port-channel", "^Port-channel", "^Bundle-Ether"],
        "Te": [
            "^TenGigabitEthernet",
            "^TenGe",
            "^10GE",
            "^TenGigE",
            "^XGigabitEthernet",
        ],
        "Fe": ["^FastEthernet"],
        "Eth": ["^Ethernet"],
        "Pt": ["^Port[^-]"],
        "100G": ["^HundredGigE"],
    }
}


# =============================================================================
# Main class:
# =============================================================================


class cdp_lldp_drawer:
    """
    Class to process CDP and LLDP neighbors together with
    running configuration and state to produce diagram out of it.

    **Features support matrix**

    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Platform      |    CDP     |   LLDP    |   config  |   state   |   LAG     | grouping  |
    +===============+============+===========+===========+===========+===========+===========+
    | Cisco_IOS     |    YES     |    ---    |    YES    |    ---    |    YES    |    YES    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_IOSXR   |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_NXOS    |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Cisco_ASA     |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Huawei        |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+
    | Juniper       |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |
    +---------------+------------+-----------+-----------+-----------+-----------+-----------+

    **Cisco Commands**

    * CDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show cdp neighbor details``
    * LLDP for Cisco IOS, IOS-XR, NXOS, ASA - ``show lldp neighbor details``
    * config, LAG, grouping for Cisco IOS, IOS-XR, NXOS, ASA - ``show running-configuration``
    * state for Cisco IOS, IOS-XR, NXOS - ``show interface``

    ** Huawei Commands**

    * LLDP - ``display lldp neighbor details``
    * config, LAG, grouping - ``display current-configuration``
    * state - ``display interface``

    **cdp_lldp_drawer attributes**

    * ``data`` dictionary or OS path string to directory with text files
    * ``drawing`` N2G drawing object instantiated using drawing module e.g. yed_diagram or drawio_diagram
    * ``config`` dictionary of configuration options to define processing behavior

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
             |_/Cisco_IOS-XR/<text files>
             |_/Huawei/<text files>
             |_/...etc...

    Supported ``config`` dictionary attributes::

    * add_interfaces_data -
    * group_links -
    * add_lag -
    """

    def __init__(self, drawing, config={}):
        # init attributes
        self.config = {
            "add_interfaces_data": True,
            "group_links": False,
            "add_lag": False,
        }
        self.config.update(config)
        self.drawing = drawing
        self.drawing.node_duplicates = "update"
        self.parsed_data = {}
        self.nodes_dict = {}
        self.links_dict = {}
        self.graph_dict = {"nodes": [], "links": []}
        self.lag_links_dict = {}  # used by add_lag method
        self.nodes_to_links_dict = {}  # used by group_links

    def work(self, data):
        self._parse(data)
        self._form_base_graph_dict()
        # go through config statements
        if self.config.get("add_lag"):
            self._add_lags_to_links_dict()
        if self.config.get("group_links"):
            self._group_links()
        # form graph dictionary and add it to drawing
        self._update_drawing()

    def _parse(self, data):
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=ttp_vars)
            for platform_name, text_list in data.items():
                try:
                    ttp_template = globals()[platform_name]
                except KeyError:
                    log.error(
                        "Cannot find template for '{}' platform".format(platform_name)
                    )
                    continue
                parser.add_template(template=ttp_template, template_name=platform_name)
                for item in text_list:
                    parser.add_input(item, template_name=platform_name)
        # process directories at OS path
        elif isinstance(data, str):
            parser = ttp(vars=ttp_vars, base_path=data)
            # get all sub-folders and load respective templates
            with os.scandir(data) as it:
                for entry in it:
                    if entry.is_dir():
                        try:
                            ttp_template = globals()[entry.name]
                        except KeyError:
                            log.error(
                                "Cannot find template for '{}' platform".format(
                                    entry.name
                                )
                            )
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
                    self._add_node({"id": item["source"]})
                    self._add_node(item["target"])
                    self._add_link(item, hosts, host_data)
                for item in host_data.get("lldp_peers", []):
                    self._add_node({"id": item["source"]})
                    self._add_node(item["target"])
                    self._add_link(item)

    def _add_node(self, item):
        if not item["id"] in self.nodes_dict:
            self.nodes_dict[item["id"]] = item
        else:
            node = self.nodes_dict[item["id"]]
            for k, v in item.items():
                if not k in node:
                    node[k] = v

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
        description = {
            src_if: host_data.get("interfaces", {}).get(item["src_label"], {}),
            tgt_if: hosts.get(tgt, {})
            .get("interfaces", {})
            .get(item["trgt_label"], {}),
        }
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

    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        self.drawing.from_dict(self.graph_dict)
