import argparse
import time
import os
from N2G_DrawIO import drawio_diagram as create_drawio_diagram
from N2G_yEd import yed_diagram as create_yed_diagram
from N2G_CDP_LLDP_Drawer import cdp_lldp_drawer

__version__ = "0.2.0"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

# form argparser menu:
description_text = """Parsing order is: CDP/LLDP (clp) => ...

-d,  --data          OS path to folder with data files subfolders
-f,  --folder        Output folder location, default ./Output/
-fn, --filename      Output filename, default file name based on current time
-m,  --module        Module to use - yed or drawio

CDP and LLDP drawer options:
-clp                 Parse CDP and LLDP data
-clp-add-lag         Add LAG/M-LAG information and delete member links
-clp-group-links     Group links between nodes
-clp-add-connected   Add all connected nodes
-clp-combine-peers   Combine CDP/LLDP peers behind same interface
-clp-platforms       Comma separated list of platforms to parse"""

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
    "-f",
    "--folder",
    action="store",
    dest="FOLDER",
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
# CDP and LLDP (CLP) options
#-----------------------------------------------------------------------------
run_options.add_argument(
    "-clp",
    action="store_true",
    dest="clp",
    default=False,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-clp-add-lag",
    action="store_true",
    dest="clp_add_lag",
    default=False,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-clp-group-links",
    action="store_true",
    dest="clp_group_links",
    default=False,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-clp-add-connected",
    action="store_true",
    dest="clp_add_connected",
    default=False,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-clp-combine-peers",
    action="store_true",
    dest="clp_combine_peers",
    default=False,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-clp-platforms",
    action="store",
    dest="clp_platforms",
    default="_all_",
    type=str,
    help=argparse.SUPPRESS,
)
args = argparser.parse_args()

# general arguments
DATA = args.DATA  # string, OS path to data files to process
FOLDER = args.FOLDER  # OS path to folder to save results into
FILENAME = args.FILENAME  # output filename
MODULE = args.MODULE

# CDP and LLDP drawer arguments
clp = args.clp
clp_add_lag = args.clp_add_lag
clp_group_links = args.clp_group_links
clp_add_connected = args.clp_add_connected
clp_platforms = args.clp_platforms
clp_combine_peers = args.clp_combine_peers

ext = "graphml" if MODULE == "yed" else "drawio"
if not FILENAME:
    FILENAME = 'output_{}.{}'.format(ctime, ext)
elif not FILENAME.endswith(ext):
    FILENAME = "{}.{}".format(FILENAME, ext)
    
if not os.path.exists(FOLDER):
    os.mkdir(FOLDER)
        
if clp:
    config = {
        "add_interfaces_data": True,
        "group_links": clp_group_links,
        "add_lag": clp_add_lag,
        "add_all_connected": clp_add_connected, 
        "platforms": [i.strip() for i in clp_platforms.split(",")],
        "combine_peers": clp_combine_peers
    }
    if MODULE == "yed":
        drawing = create_yed_diagram()
    elif MODULE == "drawio":
        drawing = create_drawio_diagram()
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(DATA)
    drawer.drawing.dump_file(filename=FILENAME, folder=FOLDER)