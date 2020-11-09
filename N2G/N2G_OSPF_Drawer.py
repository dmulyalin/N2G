"""

**Support matrix**

+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
|  Platform     |   CDP      |   LLDP    | interface | interface |   LAG     | links     |   node    | Add all   | Combine   |
|  Name         |   peers    |   peers   | config    | state     |   links   | grouping  |   facts   | connected | peers     |
+===============+============+===========+===========+===========+===========+===========+===========+===========+===========+
| Cisco_IOS     |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_IOSXR   |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Cisco_NXOS    |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Huawei        |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Juniper       |    ---     |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |    ---    |
+---------------+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+

"""
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    
import logging
import pprint
import json
import os
from ttp import ttp
from N2G import N2G_utils

# initiate logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Main class:
# -----------------------------------------------------------------------------


class ospf_drawer:
    """
    """
    def __init__(self, drawing, config={}, ttp_vars=None):
        # init attributes
        self.config = {
            "group_links": False,
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
        
    def _parse(self, data):
        templates_path = "{}/ttp_templates/L2_Drawer/{}.txt"
        # process data dictionary
        if isinstance(data, dict):
            parser = ttp(vars=self.ttp_vars)
            for platform_name, text_list in data.items():
                ttp_template = N2G_utils.open_ttp_template(self.config, platform_name, templates_path)
                if not ttp_template:
                    continue
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
                        ttp_template = N2G_utils.open_ttp_template(self.config, entry.name, templates_path)
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
        
    def _form_base_graph_dict(self):
        pass
        
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
        if self.config["skip_lag"] and ( 
            "LAG" in item.get("src_label", "") or
            "LAG" in item.get("trgt_label", "")       
        ):
            return
        link_hash = N2G_utils.make_hash_tuple(item)
        if link_hash not in self.links_dict:
            self.links_dict[link_hash] = {
                "source": item["source"],
                "target": item["target"]["id"],
                "src_label": item["src_label"],
                "trgt_label": item["trgt_label"],
            }
        # check if need to pre-process nodes_to_links_dict used by group_links
        if self.config.get("group_links"):
            self._update_nodes_to_links_dict(item, link_hash)
            
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
                grouped_link_hash = N2G_utils.make_hash_tuple(grouped_link)
                self.links_dict[grouped_link_hash] = grouped_link
        del self.nodes_to_links_dict
        
    def _update_drawing(self):
        self.graph_dict["nodes"] = list(self.nodes_dict.values())
        self.graph_dict["links"] = list(self.links_dict.values())
        # pprint.pprint(self.graph_dict, width =100)
        self.drawing.from_dict(self.graph_dict)