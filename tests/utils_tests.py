import sys
import xml.etree.ElementTree as ET
import xmltodict
import json

def normalize_xml(doc):
    """
    Function to normalize XML.
    
    For windows, prior to Py3.8 is good enough to compare strings just by passing
    them through ET one time, after 3.8 ET.canonicalize seems to give better results.
    
    For non windows OS, because all "should_be_xx" diagrams generated on windows,
    need to load xml to dictionary to json to string sorting all the keys, that
    is to make sure that we compare all the data in a uniform way, also string 
    allows us to get nice diff in return using pytest if tests fails.
    
    :param doc: (str) XML string
    """
    # use xml string comparison for windows
    if "win" in sys.platform.lower():
        # use canonicalize function starting with Python 3.8
        if sys.version_info.minor >= 8:
            return ET.canonicalize(doc)
        # convert to ET tree and back into string
        else:
            root = ET.fromstring(doc)
            return ET.tostring(root, encoding="unicode")
    # convert XML to dict, convert dict to json string sorting keys
    else:
        return json.dumps(
            xmltodict.parse(doc),
            sort_keys=True,
            indent=4,
        )
