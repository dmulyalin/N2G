# Need To Graph

N2G is a library to generate diagrams in [yWorks](https://www.yworks.com/) graphml or [Diagrams](https://www.diagrams.net/) drawio formats.

## Why?

To save your time on producing consistently looking, editable diagrams of arbitrary size and complexity in a programmatic way.

## How?

Not a secret that many applications use XML structured text to save their diagrams content, then why not to do the opposite - produce XML structured text that applications can open and understand and work with. N2G does exactly that, it takes structured data - csv, dictionary, list or api calls and gives back XML text that can be opened and edited by application of choice.

## What?

All formats supported so far have very similar api capable of:

* adding nodes and links with various attributes such as shape, labels, urls, data, styles
* bulk graph creation using from_x methods supporting lists, dictionaries or csv data
* existing nodes and links attributes manipulation and update
* loading existing XML diagram files for processing and modification
* deletion of nodes and links from diagrams
* comparing two diagrams to highlight the difference between them
* layout your diagram with algorithms available in (igraph)[https://igraph.org/2020/02/14/igraph-0.8.0-python.html] library
* returning results in text format or saving directly into the file

Reference [documentation](https://n2g.readthedocs.io) for more information.

## What it's not?

N2G is not a magic bullet that will produce perfect diagrams for you, it can help to simplify the process of adding elements to your diagrams. However, (manual) efforts required to put all the elements in positions where they will satisfy your inner sense of perfection, as a result, keep in mind that (normally) the more elements you have on your diagram, the more efforts required to make it looks good.

Quite unlikely it would ever be a tool that will support 100% of capabilities available in subject applications, however, feature requests are welcomed.

## Example

```python
from N2G import yed_diagram

diagram = yed_diagram()

graph_data = [
    {
        'source': 'a', 
        'src_label': 'Gig0/0\nUP', 
        'label': 'DF', 
        'target': 'b', 
        'trgt_label': 'Gig0/1', 
        'description': 'vlans_trunked: 1,2,3\nstate: up'
    },
    {
        'source': 
            {
                'id':'b', 
                'bottom_label': 'node_b'
            }, 
        'src_label': 'Gig0/0', 
        'label': 'Copper', 
        'target': 'e', 
        'trgt_label': 'Gig0/2'}
]
diagram.from_list(graph_data)
diagram.layout(algo="kk")
diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")  
```

# Disclaimer

Author of this module not affiliated with any of the application Vendors mentioned so far. The choice of formats to support was primarily driven by the fact of how much functionality available in particular application for free. Moreover, this module does not use any aforementioned (diagramming) applications in any programmatic way to produce its results, in other words, none of the aforementioned applications required to be installed on the system for this (N2G) module to work.