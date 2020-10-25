"""
A collections of shared functions, classes or data structures used 
across N2G components.
"""

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