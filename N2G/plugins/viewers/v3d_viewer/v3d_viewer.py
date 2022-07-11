"""
V3D Diagrams Viewer
*******************

V3D (Vasturiano 3D) Diagrams Viewer allows to start simple Flask WEB UI application
to visualize network data in 3D using
`force-3d-graph <https://github.com/vasturiano/3d-force-graph>`_ library.

This viewer needs to have Flask installed::

    pip install flask

Flask installed as part of ``full`` extras as well.

First, produce JSON file using N2G V3D diagram module using preferred data
plugin, L2 in this case::

    N2G -d ./Data/ -m v3d -L2 -fn sample_v3d_viewer_file

Next, run V3D viewer application using N2G CLI tool::

    N2G --v3d-viewer --diagram-file Output/sample_v3d_viewer_file.txt

Access WEB UI application via URL ``http://127.0.0.1:9000`` using your browser. It
should look similar to this:

.. image:: ../_images/v3d_viewer/v3d_viewer_1.png

By default Flask server starts and listens on all operating system interfaces, but
specific IP address and port number can be specified as required using ``--ip`` and
``--port`` N2G CLI arguments.

Where ``sample_v3d_viewer_file.txt`` file content should contain JSON data
conforming to force-3d-graph input
`JSON syntax format <https://github.com/vasturiano/3d-force-graph#input-json-syntax>`_
for example::

    {
        "nodes": [
            {
                "id": "id1",
                "name": "name1",
            },
            {
                "id": "id2",
                "name": "name2",
            }
        ],
        "links": [
            {
                "source": "id1",
                "target": "id2"
            }
        ]
    }
"""
import os
import json
import logging

try:
    from flask import Flask, render_template, Markup

    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

log = logging.getLogger(__name__)

app_dir = os.path.abspath(os.path.dirname(__file__))

if HAS_FLASK:
    app = Flask(
        __name__, static_folder=app_dir, static_url_path="", template_folder=app_dir
    )
    # based on https://stackoverflow.com/a/19269087/12300761 answer
    app.jinja_env.filters["json"] = lambda v: Markup(json.dumps(v))

    @app.route("/")
    def home():
        return render_template("v3d_viewer.html", json_data=diagram_content)


def run_v3d_viewer(
    ip: str = "0.0.0.0",
    port: int = 9000,
    debug: bool = True,
    diagram_file: str = None,
    diagram_data: str = None,
    **kwargs,
) -> None:
    """
    Function to start Flask server to run V3D viewer application.

    :param ip: IP address to run server on
    :param port: port number to run server on
    :param debug: whether server should run in debug mode
    :param diagram_file: OS path to JSON file with diagram content
    :param diagram_data: JSON string with diagram content
    :param kwargs: any additional argument to pass to Flask ``app.run`` call
    """
    global diagram_content
    if diagram_file:
        log.debug(
            f"Starting server on 'http://{ip}:{port}', diagram file: '{diagram_file}'"
        )
        with open(diagram_file, mode="r", encoding="utf-8") as f:
            diagram_content = f.read()
    elif diagram_data:
        log.debug(f"Starting server on 'http://{ip}:{port}' using diagram data")
        diagram_content = diagram_data
    else:
        log.error("No diagram file or diagram data provided, stopping...")
        return
    app.run(host=ip, port=port, debug=debug, **kwargs)
