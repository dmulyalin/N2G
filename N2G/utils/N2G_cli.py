"""
This tool allows to use N2G module capabilities from command line interface.

To produce diagram, N2G will need some source data to work with, for drawer
modules source data usually comes in the form of directories structure with 
text files containing show commands output for various devices.

After source data provided, CLI tool need to know what it needs to do, hence 
next comes the options of various drawers, such as L2 - layer 2 drawer.

And finally, results need to be saved somewhere on the hard drive using filename
and folder options.

*Sample Usage*::

    n2g -d ./path/to/data/ -L2 -L2-group-links -fn diagram_1.graphml -f ./Output/
    
*Supported options*::

    Parsing order is: CDP/LLDP (L2) => ...
    
    -d,   --data         OS path to data folder with files or file
    -of,  --out-folder   Folder where to save result, default ./Output/
    -fn,  --filename     Results filename, by default filename based on current time
    -m,   --module       Module to use - yed or drawio
							     
	XLSX data adapter            
	-nt,     --node_tabs           Comma separate list of tabs with nodes data
	-lt,     --link_tabs           Comma separate list of tabs with links data
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
"""
import argparse
import time
import os

#if run as a script, inject N2G folder in system path
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')

from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import layer_2_drawer
from N2G import ip_drawer

__version__ = "0.2.0"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

cli_help = """
Parsing order is: CDP/LLDP (L2) => ...

-d,   --data         OS path to data folder with files or file
-of,  --out-folder   Folder where to save result, default ./Output/
-fn,  --filename     Results filename, by default filename based on current time
-m,   --module       Module to use - yed or drawio
						     
XLSX data adapter. -d should point to ".xlsx" spreadsheet file.      
-nt,     --node_tabs           Comma separate list of tabs with nodes data
-lt,     --link_tabs           Comma separate list of tabs with links data
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
"""

def cli_tool():
    # form argparser menu:
    description_text = """Version: {}{}""".format(__version__, cli_help)

    argparser = argparse.ArgumentParser(
        description="N2G CLI, version {}".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_options = argparser.add_argument_group(description=description_text)
    #-----------------------------------------------------------------------------
    # General options
    #-----------------------------------------------------------------------------
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
    #-----------------------------------------------------------------------------
    # CDP and LLDP (L2) options
    #-----------------------------------------------------------------------------
    run_options.add_argument(
        "-L2",
        action="store_true",
        dest="L2",
        default=False,
        help=argparse.SUPPRESS,
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
    #-----------------------------------------------------------------------------
    # IP drawer options
    #-----------------------------------------------------------------------------
    run_options.add_argument(
        "-IP",
        action="store_true",
        dest="IP",
        default=False,
        help=argparse.SUPPRESS,
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
    #-----------------------------------------------------------------------------
    # Parse arguments
    #-----------------------------------------------------------------------------
    args = argparser.parse_args()

    # general arguments
    DATA = args.DATA  # string, OS path to data files to process
    OUT_FOLDER = args.OUT_FOLDER  # OS path to folder to save results into
    FILENAME = args.FILENAME  # output filename
    MODULE = args.MODULE

    # CDP and LLDP drawer arguments
    L2 = args.L2
    L2_add_lag = args.L2_add_lag
    L2_group_links = args.L2_group_links
    L2_add_connected = args.L2_add_connected
    L2_platforms = args.L2_platforms
    L2_combine_peers = args.L2_combine_peers
    
    # IP drawer arguments
    IP = args.IP
    IP_group_links = args.IP_group_links
    IP_lbl_intf = args.IP_lbl_intf
    IP_lbl_vrf = args.IP_lbl_vrf
    IP_add_arp = args.IP_add_arp

    ext = "graphml" if MODULE == "yed" else "drawio"
    if not FILENAME:
        FILENAME = 'output_{}.{}'.format(ctime, ext)
    elif not FILENAME.endswith(ext):
        FILENAME = "{}.{}".format(FILENAME, ext)

    if not os.path.exists(OUT_FOLDER):
        os.mkdir(OUT_FOLDER)

    if MODULE == "yed":
        drawing = create_yed_diagram()
    if MODULE == "drawio":
        drawing = create_drawio_diagram()
            
    # add CDP and LLDP to diagram
    if L2:
        config = {
            "add_interfaces_data": True,
            "group_links": L2_group_links,
            "add_lag": L2_add_lag,
            "add_all_connected": L2_add_connected,
            "platforms": [i.strip() for i in L2_platforms.split(",")],
            "combine_peers": L2_combine_peers
        }
        drawer = layer_2_drawer(drawing, config)
        drawer.work(DATA)
        
    # add IP and Subnets nodes and links to diagram
    if IP:
        config = {
            "group_links": IP_group_links,
            "label_interface": IP_lbl_intf,
            "label_vrf": IP_lbl_vrf,
            "add_arp": IP_add_arp
        }
        drawer = ip_drawer(drawing, config)
        drawer.work(DATA)
    
    # save results in file    
    drawing.dump_file(filename=FILENAME, folder=OUT_FOLDER)

if __name__ == "__main__":
    cli_tool()
