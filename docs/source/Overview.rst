Overview
========

N2G is a library to produce XML text files structured in a format supported for opening and editing by these applications:

* `yWorsk yEd Graph Editor <https://www.yworks.com/downloads#yEd>`_ graphml format as well as `yEd web application <https://www.yworks.com/yed-live/>`_
* `Diagrams DrawIO desktop <https://github.com/jgraph/drawio-desktop/releases>`_ drawio format as well as `DrawIO web application <https://app.diagrams.net/>`_

N2G contains dedicated modules for each format with very similar API that can help create, load, modify and save diagrams. 

However, due to discrepancy in functionality and peculiarities of applications itself, N2G modules API is not 100% identical and differ to reflect particular application capabilities. 