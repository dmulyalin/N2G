"""
This tool allows to use N2G module capabilities from command line interface.

To produce diagram, N2G will need source data to work with, for drawer
modules source data usually comes in the form of directories structure with 
text files containing show commands output for devices.

After source data provided, CLI tool need to know what it needs to do, hence 
next comes the options of various drawers, such as L2 - layer 2 drawer.

And finally, results need to be saved somewhere on the local file system using 
filename and folder options.

*Sample Usage*::

    n2g -d ./path/to/data/ -L2 -L2-group-links -fn diagram_1.graphml -f ./Output/
    
*Supported options*::   

    Parsing order is: CDP/LLDP (L2)  => IP => OSPF => ISIS
    
    -d,   --data         OS path to data folder with files or file
    -of,  --out-folder   Folder where to save result, default ./Output/
    -fn,  --filename     Results filename, by default filename based on current time
    -m,   --module       Module to use - yed, drawio or v3d
    -ipl, --ip_lookup    Path to CSV file for IP lookups, first column header must be ``ip``
    --no-data            Do not add any data to links or nodes  
    --layout             Name of iGraph layout algorithm to run for the diagram e.g. "kk", "tree" etc.
    
    V3D Module arguments:
    --run                Run built in test web server to display topology instead of saving to file
    --port               Port number to run server on
        
    XLSX data adapter. -d should point to ".xlsx" spreadsheet file.      
    -nt,     --node-tabs           Comma separate list of tabs with nodes data
    -lt,     --link-tabs           Comma separate list of tabs with links data
    -nm,     --node-headers-map    JSON dictionary structure for node headers translation           
    -lm,     --link-headers-map    JSON dictionary structure for link headers translation
    
    CDP and LLDP L2 drawer options:
    -L2                 Parse CDP and LLDP data
    -L2-add-lag         Add LAG/M-LAG information and delete member links
    -L2-group-links     Group links between nodes
    -L2-add-connected   Add all connected nodes
    -L2-combine-peers   Combine CDP/LLDP peers behind same interface
    -L2-platforms       Comma separated list of platforms to parse
    
    IP network drawer:
    -IP                 Parse IP subnets
    -IP-group-links     Group links between nodes
    -IP-lbl-intf        Add interfaces names to link labels
    -IP-lbl-vrf         Add VRF names to link labels
    -IP-add-arp         Add ARP cache IPs to the diagram
    
    OSPF LSDB Drawer:
    -OSPF               Diagram OSPFv2 LSDB data
    -OSPF-add-con       Add connected subnets to diagram
    
    ISIS LSDB Drawer:
    -ISIS               Diagram ISIS LSDB data
    -ISIS-add-con       Add connected subnets to diagram
"""
import argparse
import time
import os

# if run as a script, inject N2G folder in system path
if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from N2G import (
    drawio_diagram,
    yed_diagram,
    v3d_diagramm,
    xlsx_data,
    cli_l2_data,
    cli_ip_data,
    cli_ospf_data,
    cli_isis_data,
)

__version__ = "0.2.0"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

cli_help = """
Parsing order is: CDP/LLDP (L2)  => IP => OSPF => ISIS

-d,   --data         OS path to data folder with files or file
-of,  --out-folder   Folder where to save result, default ./Output/
-fn,  --filename     Results filename, by default filename based on current time
-m,   --module       Module to use - yed, drawio or v3d
-ipl, --ip_lookup    Path to CSV file for IP lookups, first column header must be ``ip``
--no-data            Do not add any data to links or nodes  
--layout             Name of iGraph layout algorithm to run for the diagram e.g. "kk", "tree" etc.

V3D Module arguments:
--run                Run built in test web server to display topology instead of saving to file
--port               Port number to run server on
    
XLSX data adapter. -d should point to ".xlsx" spreadsheet file.      
-nt,     --node-tabs           Comma separate list of tabs with nodes data
-lt,     --link-tabs           Comma separate list of tabs with links data
-nm,     --node-headers-map    JSON dictionary structure for node headers translation           
-lm,     --link-headers-map    JSON dictionary structure for link headers translation

CDP and LLDP L2 drawer options:
-L2                 Parse CDP and LLDP data
-L2-add-lag         Add LAG/M-LAG information and delete member links
-L2-group-links     Group links between nodes
-L2-add-connected   Add all connected nodes
-L2-combine-peers   Combine CDP/LLDP peers behind same interface
-L2-platforms       Comma separated list of platforms to parse

IP network drawer:
-IP                 Parse IP subnets
-IP-group-links     Group links between nodes
-IP-lbl-intf        Add interfaces names to link labels
-IP-lbl-vrf         Add VRF names to link labels
-IP-add-arp         Add ARP cache IPs to the diagram

OSPF LSDB Drawer:
-OSPF               Diagram OSPFv2 LSDB data
-OSPF-add-con       Add connected subnets to diagram

ISIS LSDB Drawer:
-ISIS               Diagram ISIS LSDB data
-ISIS-add-con       Add connected subnets to diagram
"""


def cli_tool():
    # form argparser menu:
    description_text = """Version: {}{}""".format(__version__, cli_help)

    argparser = argparse.ArgumentParser(
        description="N2G CLI, version {}".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_options = argparser.add_argument_group(description=description_text)
    # -----------------------------------------------------------------------------
    # General options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-d",
        "--data",
        action="store",
        dest="DATA",
        default="",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-of",
        "--out-folder",
        action="store",
        dest="OUT_FOLDER",
        default="./Output/",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-fn",
        "--filename",
        action="store",
        dest="FILENAME",
        default=None,
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-m",
        "--module",
        action="store",
        dest="MODULE",
        default="yed",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-ipl",
        "--ip_lookup",
        action="store",
        dest="IP_LOOKUP",
        default={},
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "--no-data",
        action="store_false",
        dest="NO_DATA",
        default=True,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "--layout",
        action="store",
        dest="LAYOUT",
        default="",
        type=str,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # V3D options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "--run", action="store_true", dest="RUN", default=False, help=argparse.SUPPRESS
    )
    run_options.add_argument(
        "--port",
        action="store",
        dest="PORT",
        default=9000,
        type=int,
        help=argparse.SUPPRESS,
    )

    # -----------------------------------------------------------------------------
    # XLSX data adapter options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-nt",
        "--node-tabs",
        action="store",
        dest="XLSX_NODE_TABS",
        default="",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-lt",
        "--link-tabs",
        action="store",
        dest="XLSX_LINK_TABS",
        default="",
        type=str,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # CDP and LLDP (L2) options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-L2", action="store_true", dest="L2", default=False, help=argparse.SUPPRESS
    )
    run_options.add_argument(
        "-L2-add-lag",
        action="store_true",
        dest="L2_add_lag",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-L2-group-links",
        action="store_true",
        dest="L2_group_links",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-L2-add-connected",
        action="store_true",
        dest="L2_add_connected",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-L2-combine-peers",
        action="store_true",
        dest="L2_combine_peers",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-L2-platforms",
        action="store",
        dest="L2_platforms",
        default="_all_",
        type=str,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # IP drawer options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-IP", action="store_true", dest="IP", default=False, help=argparse.SUPPRESS
    )
    run_options.add_argument(
        "-IP-group-links",
        action="store_true",
        dest="IP_group_links",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-IP-lbl-intf",
        action="store_true",
        dest="IP_lbl_intf",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-IP-lbl-vrf",
        action="store_true",
        dest="IP_lbl_vrf",
        default=False,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-IP-add-arp",
        action="store_true",
        dest="IP_add_arp",
        default=False,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # OSPF drawer options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-OSPF", action="store_true", dest="OSPF", default=False, help=argparse.SUPPRESS
    )
    run_options.add_argument(
        "-OSPF-add-con",
        action="store_true",
        dest="OSPF_ADD_CON",
        default=False,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # ISIS drawer options
    # -----------------------------------------------------------------------------
    run_options.add_argument(
        "-ISIS", action="store_true", dest="ISIS", default=False, help=argparse.SUPPRESS
    )
    run_options.add_argument(
        "-ISIS-add-con",
        action="store_true",
        dest="ISIS_ADD_CON",
        default=False,
        help=argparse.SUPPRESS,
    )
    # -----------------------------------------------------------------------------
    # Parse arguments
    # -----------------------------------------------------------------------------
    args = argparser.parse_args()

    # general arguments
    DATA = args.DATA  # string, OS path to data files to process
    OUT_FOLDER = args.OUT_FOLDER  # OS path to folder to save results into
    FILENAME = args.FILENAME  # output filename
    MODULE = args.MODULE
    IP_LOOKUP = args.IP_LOOKUP
    NO_DATA = args.NO_DATA
    LAYOUT = args.LAYOUT

    # V3D arguments
    RUN = args.RUN
    PORT = args.PORT

    # XLSX data plugin arguments
    XLSX_NODE_TABS = args.XLSX_NODE_TABS
    XLSX_LINK_TABS = args.XLSX_LINK_TABS

    # CDP and LLDP data plugin  arguments
    L2 = args.L2
    L2_add_lag = args.L2_add_lag
    L2_group_links = args.L2_group_links
    L2_add_connected = args.L2_add_connected
    L2_platforms = args.L2_platforms
    L2_combine_peers = args.L2_combine_peers

    # IP data plugin arguments
    IP = args.IP
    IP_group_links = args.IP_group_links
    IP_lbl_intf = args.IP_lbl_intf
    IP_lbl_vrf = args.IP_lbl_vrf
    IP_add_arp = args.IP_add_arp

    # OSPF data plugin arguments
    OSPF = args.OSPF
    OSPF_ADD_CON = args.OSPF_ADD_CON

    # ISIS data plugin arguments
    ISIS = args.ISIS
    ISIS_ADD_CON = args.ISIS_ADD_CON

    # Instantiate diagram
    ext = "txt"
    if MODULE == "yed":
        drawing = yed_diagram()
        ext = "graphml"
    elif MODULE == "drawio":
        drawing = drawio_diagram()
        ext = "drawio"
    elif MODULE == "v3d":
        drawing = v3d_diagramm()

    # create output filename and folder
    if not FILENAME:
        FILENAME = "output_{}.{}".format(ctime, ext)
    elif not FILENAME.endswith(ext):
        FILENAME = "{}.{}".format(FILENAME, ext)

    if not os.path.exists(OUT_FOLDER):
        os.mkdir(OUT_FOLDER)

    # check if need to use XLSX adapter
    if DATA.endswith(".xlsx"):
        xlsx_data(
            drawing,
            DATA,
            link_tabs=[i.strip() for i in XLSX_LINK_TABS.split(",")]
            if XLSX_LINK_TABS
            else [],
            node_tabs=[i.strip() for i in XLSX_NODE_TABS.split(",")]
            if XLSX_NODE_TABS
            else [],
        )

    # add CDP and LLDP to diagram
    if L2:
        config = {
            "add_interfaces_data": True,
            "group_links": L2_group_links,
            "add_lag": L2_add_lag,
            "add_all_connected": L2_add_connected,
            "platforms": [i.strip() for i in L2_platforms.split(",")],
            "combine_peers": L2_combine_peers,
        }
        drawer = cli_l2_data(drawing, **config)
        drawer.work(DATA)

    # add IP and Subnets nodes and links to diagram
    if IP:
        config = {
            "group_links": IP_group_links,
            "label_interface": IP_lbl_intf,
            "label_vrf": IP_lbl_vrf,
            "add_arp": IP_add_arp,
        }
        drawer = cli_ip_data(drawing, **config)
        drawer.work(DATA)

    # add OSPF LSDB links/nodes to diagram
    if OSPF:
        drawer = cli_ospf_data(
            drawing,
            ip_lookup_data=IP_LOOKUP,
            add_connected=OSPF_ADD_CON,
            add_data=NO_DATA,
        )
        drawer.work(DATA)

    # add ISIS LSDB links/nodes to diagram
    if ISIS:
        drawer = cli_isis_data(
            drawing,
            ip_lookup_data=IP_LOOKUP,
            add_connected=ISIS_ADD_CON,
            add_data=NO_DATA,
        )
        drawer.work(DATA)

    # layout diagram
    if LAYOUT:
        drawing.layout(algo=LAYOUT)

    # save diagram
    if RUN and MODULE == "v3d":
        # run V3D built in topology browser
        drawing.run(port=PORT)
    else:
        # save results in file
        drawing.dump_file(filename=FILENAME, folder=OUT_FOLDER)


if __name__ == "__main__":
    cli_tool()
