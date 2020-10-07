[![Downloads](https://pepy.tech/badge/n2g)](https://pepy.tech/project/n2g)
[![Documentation Status](https://readthedocs.org/projects/n2g/badge/?version=latest)](https://n2g.readthedocs.io/en/latest/?badge=latest)

# Need To Graph

N2G is a library to generate diagrams in [yWorks](https://www.yworks.com/) graphml or [Diagrams](https://www.diagrams.net/) drawio formats.

<details><summary>Demo</summary>
<img src="example.gif">  
</details>

## Why?

To save your time on producing consistently looking, editable diagrams of arbitrary size and complexity in a programmatic way helping to satisfy your "Need To Graph" desire.

## How?

Not a secret that many applications use XML structured text to save their diagrams content, then why not to do the opposite - produce XML structured text that applications can open and understand and work with. N2G does exactly that, it takes structured data - csv, dictionary, list or api calls and gives back XML text that can be opened and edited by application of choice.

## What?

All formats supported so far have very similar API capable of:

* adding nodes and links with various attributes such as shape, labels, urls, data, styles
* bulk graph creation using from_x methods supporting lists, dictionaries or csv data
* existing nodes and links attributes manipulation and update
* loading existing XML diagram files for processing and modification
* deletion of nodes and links from diagrams
* comparing two diagrams to highlight the difference between them
* layout your diagram with algorithms available in [igraph](https://igraph.org/2020/02/14/igraph-0.8.0-python.html) library
* returning results in text format or saving directly into the file

Reference [documentation](https://n2g.readthedocs.io/en/0.1.2/index.html) for more information.

## What it's not?

N2G is not a magic bullet that will produce perfect diagrams for you, it can help to simplify the process of adding elements to your diagrams. However, (manual) efforts required to put all the elements in positions where they will satisfy your inner sense of perfection, as a result, keep in mind that (normally) the more elements you have on your diagram, the more efforts required to make it looks good.

Quite unlikely it would ever be a tool with support of all capabilities available in subject applications, however, feature requests are welcomed.

## Example

```python
from N2G import yed_diagram

diagram = yed_diagram()
sample_list_graph = [
    {'source': {'id': 'SW1', 'top_label': 'CORE', 'bottom_label': '1,1,1,1'}, 'src_label': 'Gig0/0', 'target': 'R1', 'trgt_label': 'Gig0/1'},
    {'source': {'id': 'R2', 'top_label': 'DC-PE'}, 'src_label': 'Gig0/0', 'target': 'SW1', 'trgt_label': 'Gig0/2'},
    {'source': {'id':'R3', 'bottom_label': '1.1.1.3'}, 'src_label': 'Gig0/0', 'target': 'SW1', 'trgt_label': 'Gig0/3'},
    {'source': 'SW1', 'src_label': 'Gig0/4', 'target': 'R4', 'trgt_label': 'Gig0/1'},
    {'source': 'SW1', 'src_label': 'Gig0/5', 'target': 'R5', 'trgt_label': 'Gig0/7'},
    {'source': 'SW1', 'src_label': 'Gig0/6', 'target': 'R6', 'trgt_label': 'Gig0/11'}
]
diagram.from_list(sample_list_graph)
diagram.dump_file(filename="Sample_graph.graphml", folder="./")
```

# Disclaimer

Author of this module not affiliated with any of the application Vendors mentioned so far. The choice of formats to support was primarily driven by the fact of how much functionality available in particular application for free. Moreover, this module does not use any aforementioned (diagramming) applications in any programmatic way to produce its results, in other words, none of the aforementioned applications required to be installed on the system for this (N2G) module to work.

# Contributions
Feel free to submit an issue, to report a bug or ask a question, feature requests are welcomed or [buy](https://paypal.me/dmulyalin) Author a coffee