import sys
import xml.etree.ElementTree as ET
   
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
