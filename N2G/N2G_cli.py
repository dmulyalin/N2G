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
    
    -d,  --data          OS path to folder with data files subfolders
    -f,  --folder        Output folder location, default ./Output/
    -fn, --filename      Output filename, default file name based on current time
    -m,  --module        Module to use - yed or drawio
    
    CDP and LLDP drawer options:
    -L2                 Parse CDP and LLDP data
    -L2-add-lag         Add LAG/M-LAG information and delete member links
    -L2-group-links     Group links between nodes
    -L2-add-connected   Add all connected nodes
    -L2-combine-peers   Combine CDP/LLDP peers behind same interface
    -L2-platforms       Comma separated list of platforms to parse
"""
import argparse
import time
import os

if __name__ == "__main__":
    from N2G_DrawIO import drawio_diagram as create_drawio_diagram
    from N2G_yEd import yed_diagram as create_yed_diagram
    from N2G_L2_Drawer import layer_2_drawer
    from N2G_IP_Drawer import ip_drawer
else:
    from N2G.N2G_DrawIO import drawio_diagram as create_drawio_diagram
    from N2G.N2G_yEd import yed_diagram as create_yed_diagram
    from N2G.N2G_L2_Drawer import layer_2_drawer
    from N2G.N2G_IP_Drawer import ip_drawer

__version__ = "0.2.0"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

cli_help = """
Parsing order is: CDP/LLDP (L2) => ...

-d,  --data          OS path to folder with data files subfolders
-f,  --folder        Output folder location, default ./Output/
-fn, --filename      Output filename, default file name based on current time
-m,  --module        Module to use - yed or drawio

CDP and LLDP drawer options:
-L2                 Parse CDP and LLDP data
-L2-add-lag         Add LAG/M-LAG information and delete member links
-L2-group-links     Group links between nodes
-L2-add-connected   Add all connected nodes
-L2-combine-peers   Combine CDP/LLDP peers behind same interface
-L2-platforms       Comma separated list of platforms to parse

IP network drawer:
-IP                 Parse IP subnets
-IP-group-links     Group links between nodes
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
    args = argparser.parse_args()

    # general arguments
    DATA = args.DATA  # string, OS path to data files to process
    FOLDER = args.FOLDER  # OS path to folder to save results into
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

    ext = "graphml" if MODULE == "yed" else "drawio"
    if not FILENAME:
        FILENAME = 'output_{}.{}'.format(ctime, ext)
    elif not FILENAME.endswith(ext):
        FILENAME = "{}.{}".format(FILENAME, ext)

    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

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
            "group_links": IP_group_links
        }
        drawer = ip_drawer(drawing, config)
        drawer.work(DATA)
        
    drawing.dump_file(filename=FILENAME, folder=FOLDER)

if __name__ == "__main__":
    cli_tool()
