import sys
sys.path.insert(0,'..')
# after updated sys path, can do N2G import from parent dir

from N2G import drawio_diagram
from N2G import xlsx_data
from utils_tests import normalize_xml

def test_xlsx_data_base():
    drawio_drawing = drawio_diagram()
    xlsx_data(drawio_drawing, "./Data/xlsx_data_base.xlsx")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_xlsx_data_base.drawio", folder="./Output/")
    # run test
    with open ("./Output/test_xlsx_data_base.drawio") as produced:
        with open("./Output/should_be_test_xlsx_data_base.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())
            
# test_xlsx_data_base()

def test_xlsx_data_tanslate_headers():
    drawio_drawing = drawio_diagram()
    xlsx_data(drawio_drawing, "./Data/xlsx_data_tanslate_headers.xlsx")
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_xlsx_data_tanslate_headers.drawio", folder="./Output/")
    # run test
    with open ("./Output/test_xlsx_data_tanslate_headers.drawio") as produced:
        with open("./Output/should_be_test_xlsx_data_tanslate_headers.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())    
            
# test_xlsx_data_tanslate_headers()

def test_xlsx_data_tanslate_headers_several_tabs():
    drawio_drawing = drawio_diagram()
    xlsx_data(
        drawio_drawing, 
        "./Data/xlsx_data_tanslate_headers_several_tabs.xlsx", 
        link_tabs=["L1", "L3"]
    )
    drawio_drawing.layout(algo="kk")
    drawio_drawing.dump_file(filename="test_xlsx_data_tanslate_headers_several_tabs.drawio", folder="./Output/")
    # run test
    with open ("./Output/test_xlsx_data_tanslate_headers_several_tabs.drawio") as produced:
        with open("./Output/should_be_test_xlsx_data_tanslate_headers_several_tabs.drawio") as should_be:
            assert normalize_xml(produced.read()) == normalize_xml(should_be.read())   
			
# test_xlsx_data_tanslate_headers_several_tabs()