"""
A collections of shared functions, classes or data structures used 
across N2G components.
"""
import os
import logging

# initiate logging
log = logging.getLogger(__name__)


ttp_variables = {
    # IfsNormalize helps to normalize interface names across
    # various platforms to uniform values
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
        "SVI": ["^Vlan", "^Vlanif", "^BDI"]
    },
    # used by L2 drawer to identify if is_physical_port, that used by
    # add all connected nodes feature
    "physical_ports": ["Ge", "Te", "Fe", "Eth", "100G", "mgmt", "40G"]
}

def make_hash_tuple(item):
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
    
def open_ttp_template(config, template_name, templates_path):
    path_to_n2g = os.path.dirname(__file__)
    try:
        if (
            "_all_" not in config["platforms"]
            and not template_name in config["platforms"]
        ):
            return False
        path = templates_path.format(
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
