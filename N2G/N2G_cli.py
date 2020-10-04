import argparse
from N2G_DrawIO import drawio_diagram as create_drawio_diagram
from N2G_yEd import yed_diagram as create_yed_diagram
from N2G_CDP_LLDP_Drawer import cdp_lldp_drawer

__version__ = "0.1.0"

# form argparser menu:
description_text = """-d,  --data            OS path to folder with data files subfolders
-of, --out-folder      Output folder location, default ./Output/
-on, --out-name        Output filename
-m,  --module          Module to use - yed or drawio
-cdp-lldp              Parse CDP and LLDP data
-cdp-lldp-add-lag      Add LAG information and delete member links
-cdp-lldp-group-links  Group links between nodes"""

argparser = argparse.ArgumentParser(
    description="N2G CLI, version {}".format(__version__),
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
run_options = argparser.add_argument_group(description=description_text)
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
    dest="FOLDER",
    default="./Output/",
    type=str,
    help=argparse.SUPPRESS,
)
run_options.add_argument(
    "-on",
    "--out-name",
    action="store",
    dest="FILENAME",
    default="FILENAME",
    type=str,
    help=argparse.SUPPRESS,
)

# extract argparser arguments:
args = argparser.parse_args()
DATA = args.DATA  # string, OS path to data files to process
FOLDER = args.FOLDER  # OS path to folder to save results into
FILENAME = args.FILENAME  # output filename

config = {"add_all_connected": True, "add_lag": True}
drawing = create_yed_diagram()
drawer = cdp_lldp_drawer(drawing, config)
drawer.work(DATA)
drawer.drawing.dump_file(filename=FILENAME, folder=FOLDER)