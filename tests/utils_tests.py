import xmltodict
import json
import sys
import xml.etree.ElementTree as ET

def compare_xml(doc_a, doc_b):
    """
    Function to return True if both XML documents are identical, simply
    comparing string might be not enough, as XML generated on say Python 3.7
    produces not the same string as on Python 3.9
    
    :param doc_a: (str) XML string for first element
    :param doc_b: (str) XML string for second element
    """
    # load XML string to etree object
    root_a = ET.fromstring(doc_a)
    root_b = ET.fromstring(doc_b)
    # serialize back to string assuming that identical XML etree produce identical strings
    doc_a_norm = ET.tostring(root_a, encoding="unicode")
    doc_b_norm = ET.tostring(root_b, encoding="unicode")
    # run comparison
    return doc_a_norm == doc_b_norm
    
def normalize_xml(doc):
    """
    Function to normalize XML
    
    :param doc: (str) XML string
    """
    # use canonicalize function starting with Python 3.8
    if sys.version_info.minor >= 8:
        return ET.canonicalize(doc)
    # convert to ET tree and back into string
    else:
        root = ET.fromstring(doc)
        return ET.tostring(root, encoding="unicode")
    # return json.dumps(
    #     xmltodict.parse(doc, process_namespaces=True),
    #     sort_keys=True, indent=4
    # )