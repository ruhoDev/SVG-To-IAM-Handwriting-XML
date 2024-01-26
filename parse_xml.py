from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
from svg.path import parse_path
from xml.dom.minidom import parse
from os.path import isfile, join

check_dir1 = "svg_files/xml_check/1/"
check_dir2 = "svg_files/xml_check/2/"

xml1 = "svg_files/a01-000u-01.xml"
xml2 = "svg_files/3.xml"

dom1 = parse(xml1)
root1 = dom1.documentElement
region = root1.getElementsByTagName('WhiteboardDescription')[0]
# <DiagonallyOppositeCoords x="6512" y="1376"/>
DiagonallyOppositeCoords = region.getElementsByTagName('DiagonallyOppositeCoords')[0]
max_x_1 = float(DiagonallyOppositeCoords.getAttribute('x'))
max_y_1 = float(DiagonallyOppositeCoords.getAttribute('y'))
    # <VerticallyOppositeCoords x="966" y="1376"/>
VerticallyOppositeCoords = region.getElementsByTagName('VerticallyOppositeCoords')[0]
min_x_1 = float(VerticallyOppositeCoords.getAttribute('x'))
    # <HorizontallyOppositeCoords x="6512" y="787"/>
HorizontallyOppositeCoords = region.getElementsByTagName('HorizontallyOppositeCoords')[0]
min_y_1 = float(HorizontallyOppositeCoords.getAttribute('y'))

strokeset = root1.getElementsByTagName('StrokeSet')[0]
strokes = [stroke for stroke in strokeset.getElementsByTagName('Stroke')]
parse_strings = []
g_max_x = 0
g_min_x = 100000
g_max_y = 0
g_min_y = 100000
for i in range(len(strokes)):
    stroke = strokes[i]
    points = stroke.getElementsByTagName('Point')
    p_x = points[0].getAttribute("x")
    p_y = points[0].getAttribute("y")
    str_path = "M" + p_x + " " + p_y + " "
    parse_strings.append(str_path)
    g_max_x = max(g_max_x, float(p_x))
    g_min_x = min(g_min_x, float(p_x))
    g_max_y = max(g_max_y, float(p_y))
    g_min_y = min(g_min_y, float(p_y))
    print("Points: " + str(len(points)) + "\n")
    for j in range(1, len(points)):
        point = points[j]
        p_x = point.getAttribute("x")
        p_y = point.getAttribute("y")
        str_path = "L " + p_x + " " + p_y + " "
        parse_strings.append(str_path)
        g_max_x = max(g_max_x, float(p_x))
        g_min_x = min(g_min_x, float(p_x))
        g_max_y = max(g_max_y, float(p_y))
        g_min_y = min(g_min_y, float(p_y))

    file_path = join(check_dir1 + str(i) + ".svg")
    with open(file_path, 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f' viewBox="0,0,{max_x_1},{max_y_1}" width="100%">\n')
        f.write('<path d="')
        for new_path_string in parse_strings:
            f.write(new_path_string)
        f.write('"/>')
        f.write('</svg>\n')


dom1 = parse(xml2)
root1 = dom1.documentElement
region = root1.getElementsByTagName('WhiteboardDescription')[0]
# <DiagonallyOppositeCoords x="6512" y="1376"/>
DiagonallyOppositeCoords = region.getElementsByTagName('DiagonallyOppositeCoords')[0]
max_x_1 = float(DiagonallyOppositeCoords.getAttribute('x'))
max_y_1 = float(DiagonallyOppositeCoords.getAttribute('y'))
    # <VerticallyOppositeCoords x="966" y="1376"/>
VerticallyOppositeCoords = region.getElementsByTagName('VerticallyOppositeCoords')[0]
min_x_1 = float(VerticallyOppositeCoords.getAttribute('x'))
    # <HorizontallyOppositeCoords x="6512" y="787"/>
HorizontallyOppositeCoords = region.getElementsByTagName('HorizontallyOppositeCoords')[0]
min_y_1 = float(HorizontallyOppositeCoords.getAttribute('y'))

strokeset = root1.getElementsByTagName('StrokeSet')[0]
strokes = [stroke for stroke in strokeset.getElementsByTagName('Stroke')]
parse_strings = []
g_max_x = 0
g_min_x = 100000
g_max_y = 0
g_min_y = 100000
for i in range(len(strokes)):
    stroke = strokes[i]
    points = stroke.getElementsByTagName('Point')
    p_x = points[0].getAttribute("x")
    p_y = points[0].getAttribute("y")
    str_path = "M" + p_x + " " + p_y + " "
    parse_strings.append(str_path)
    g_max_x = max(g_max_x, float(p_x))
    g_min_x = min(g_min_x, float(p_x))
    g_max_y = max(g_max_y, float(p_y))
    g_min_y = min(g_min_y, float(p_y))
    print("Points: " + str(len(points)) + "\n")
    for j in range(1, len(points)):
        point = points[j]
        p_x = point.getAttribute("x")
        p_y = point.getAttribute("y")
        str_path = "L " + p_x + " " + p_y + " "
        parse_strings.append(str_path)
        g_max_x = max(g_max_x, float(p_x))
        g_min_x = min(g_min_x, float(p_x))
        g_max_y = max(g_max_y, float(p_y))
        g_min_y = min(g_min_y, float(p_y))

    file_path = join(check_dir2 + str(i) + ".svg")
    with open(file_path, 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f' viewBox="0,0,{max_x_1},{max_y_1}" width="100%">\n')
        f.write('<path d="')
        for new_path_string in parse_strings:
            f.write(new_path_string)
        f.write('"/>')
        f.write('</svg>\n')

print("")


