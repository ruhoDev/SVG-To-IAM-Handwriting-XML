import os.path

from svg.path import parse_path
from xml.dom.minidom import parse
import numpy as np
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

default_x = 400
default_y = 200


def get_first_pos(str):
    path = parse_path(str)
    point = path[0].point(0)
    return point.real


# root = ET.Element("root")
# doc = ET.SubElement(root, "doc")
#
# ET.SubElement(doc, "field1", name="blah").text = "some value1"
# ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
#
# tree = ET.ElementTree(root)
# tree.write("filename.xml")

def bezier_to_points(svg_input, stroke_dir, xml_output, num_points):
    # Parse the SVG XML file
    dom = parse(svg_input)
    path_strings = [path.getAttribute('d') for path in dom.getElementsByTagName('path')]
    path_strings.sort(key=get_first_pos)
    dom.unlink()

    xmlroot = ET.Element("WhiteboardCaptureSession")
    WhiteboardDescription = ET.SubElement(xmlroot, "WhiteboardDescription")
    ET.SubElement(WhiteboardDescription, "SensorLocation", corner="top_left")

    # Parse each path, convert Bézier curves to points, and create new path strings
    max_x = 0
    max_y = 0
    min_x = 100000
    min_y = 100000
    new_path_strings = []
    for path_string in path_strings:
        path = parse_path(path_string)
        # str_point = path[0].point(0)
        # str_path = "M" + str(str_point.real) + " " + str(str_point.imag) + " "
        points = []
        # new_path_strings.append(str_path)
        # for curve in path:
        for i in range(0, len(path)):
            curve = path[i]
            for t in np.linspace(0, 1, 10):
                point = curve.point(t)
                points.append(point)
                max_x = max(max_x, point.real)
                max_y = max(max_y, point.imag)
                min_x = min(min_x, point.real)
                min_y = min(min_y, point.imag)

        # new_path_strings.append(' '.join(f"L {point.real},{max_y - point.imag}" for point in points))
    default_y = default_x * max_y / max_x
    ET.SubElement(WhiteboardDescription, "DiagonallyOppositeCoords", x=str(default_x), y=str(default_y))
    ET.SubElement(WhiteboardDescription, "VerticallyOppositeCoords", x=str(min_x * default_x / max_x), y=str(default_y))
    ET.SubElement(WhiteboardDescription, "HorizontallyOppositeCoords", x=str(default_x), y=str(min_y * default_y / max_y))
    stroke_set = ET.SubElement(xmlroot, "StrokeSet")
    points = []
    index = 0
    for path_string in path_strings:
        stroke = ET.SubElement(stroke_set, "Stroke", colour="black")
        path = parse_path(path_string)
        str_point = path[0].point(0)
        str_x = str(default_x * str_point.real / max_x)
        str_y = str(default_y * (max_y - str_point.imag) / max_y)
        # ET.SubElement(stroke, "Point", x=str(str_x), y=str(str_y))
        str_path = "M" + str_x + " " + str_y + " "
        new_path_strings.append(str_path)
        # for curve in path:
        for i in range(1, len(path)):
            curve = path[i]
            for t in np.linspace(0, 1, num_points):
                point = curve.point(t)
                points.append(point)
                ET.SubElement(stroke, "Point", x=str(default_x * point.real / max_x), y=str(default_y * (max_y - point.imag) / max_y))

        new_path_strings.append(' '.join(
            f"L {default_x * point.real / max_x},{default_y * (max_y - point.imag) / max_y}" for point in points))

        # Create a new SVG XML file with the point-based paths
        svg_output = stroke_dir + str(index) + '.svg'
        with open(svg_output, 'w') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
            f.write(f' viewBox="0,0,{default_x},{default_y}" width="100%">\n')
            f.write('<path d="')
            for new_path_string in new_path_strings:
                f.write(new_path_string)
            f.write('"/>')
            f.write('</svg>\n')
        index += 1

    # Create an ElementTree object
    tree = ET.ElementTree(xmlroot)
    ET.indent(tree, space="\t", level=0)

    # Write the tree to an XML file
    tree.write(xml_output, encoding="utf-8")


svg_dir = "svg_files/tm"
out_dir = "svg_files/new"
xml_dir = "svg_files/xml"
stroke_history_dir = "svg_files/stroke_history/"
svg_files = [f for f in listdir(svg_dir) if isfile(join(svg_dir, f))]

for svg_file in svg_files:
    name, suffix = os.path.splitext(svg_file)
    input_path = join(svg_dir, svg_file)
    # output_path = join(out_dir, svg_file)
    xml_path = join(xml_dir, name + '.xml')
    stroke_dir = stroke_history_dir + name + "/"
    if not os.path.exists(stroke_dir):
        os.makedirs(stroke_dir)
    bezier_to_points(input_path, stroke_dir, xml_path, 10)
# test_input = "svg_files/1.svg"
# test_output = "svg_files/2.svg"
# xml_path = "svg_files/3.xml"
# bezier_to_points(test_input, stroke_history_dir, xml_path, 60)
