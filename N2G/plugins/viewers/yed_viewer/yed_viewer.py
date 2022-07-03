"""
yEd SVG Viewer
**************

yED SVG Viewer allows to start simple Flask WEB UI application to visualize network
data using `D3.js <https://d3js.org/>`_ library.

This viewer needs to have Flask installed::

    pip install flask

Flask installed as part of ``full`` extras as well.

To run using N2G CLI tool::

    N2G --yed-svg-viewer --diagrams-dir /Diagrams/

Access WEB UI application via URL ``http://127.0.0.1:9000`` using your browser.

By default Flask server starts and listens on all operating system interfaces, but
specific IP address and port number can be specified as required using ``--ip`` and
``--port`` N2G CLI arguments.

OS path to directory with diagram files can be specified using ``--diagrams-dir``
N2G CLI tool argument or using ``N2G_DIAGRAMS_DIR`` environment variable. If no
``--diagrams-dir`` argument provided, N2G attempts to retrieve diagrams directory
path using ``N2G_DIAGRAMS_DIR`` environment variable.

Diagrams directory should contain SVG files produced by yED Graph Editor application
using ``File -> Export -> Save as type: SVG format`` feature.
"""
import os
import json
import logging

try:
    from flask import Flask, render_template

    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

log = logging.getLogger(__name__)

app_dir = os.path.abspath(os.path.dirname(__file__))

if HAS_FLASK:
    app = Flask(
        __name__, static_folder=app_dir, static_url_path="", template_folder=app_dir
    )

    @app.route("/")
    def home():
        return render_template("yed_viewer.html", select2_menu_data=scan_graphs())

    @app.route("/diagrams/<diagram_name>")
    def get_diagram(diagram_name):
        with open(os.path.join(diagrams_directory, diagram_name)) as f:
            return f.read()


def scan_graphs() -> str:
    """
    Helper function to scan folder with diagrams. Return
    json string of list of diagram dictionaries.
    """
    select2_menu_data = [
        {"id": i, "text": i.split(".")[0]}
        for i in os.listdir(diagrams_directory)
        if i.endswith("svg")
    ]
    return json.dumps(select2_menu_data)


def run_yed_viewer(
    ip: str = "0.0.0.0",
    port: int = 9000,
    debug: bool = True,
    diagrams_dir: str = None,
    **kwargs,
) -> None:
    """
    Function to start Flask server to run yED viewer application.

    :param ip: IP address to run server on
    :param port: port number to run server on
    :param debug: whether server should run in debug mode
    :param diagrams_dir: OS path to directory with diagrams, by default diagrams directory
        sourced using ``N2G_DIAGRAMS_DIR`` environment variable
    :param kwargs: any additional argument to pass to Flask app.run call
    """
    global diagrams_directory
    diagrams_directory = diagrams_dir or os.getenv("N2G_DIAGRAMS_DIR", "diagrams")
    log.debug(
        f"Starting server on 'http://{ip}:{port}', diagrams directory: '{diagrams_directory}'"
    )
    app.run(host=ip, port=port, debug=debug, **kwargs)


if __name__ == "__main__":
    run_yed_viewer()
