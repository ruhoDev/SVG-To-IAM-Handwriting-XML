"""
Utilities for manipulating/querying aspects of SVGs relevant to this
application (not a generic SVG library). All methods expect SVGs parsed as XML
using Python's ElementTree library.
"""

import re

from copy import deepcopy


# Relevant XML namespace URIs used by SVGs
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
INKSCAPE_NAMESPACE = "http://www.inkscape.org/namespaces/inkscape"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"

namespaces = {
    "svg": SVG_NAMESPACE,
    "inkscape": INKSCAPE_NAMESPACE,
    "xlink": XLINK_NAMESPACE,
}

# Unit conversion ratios
MM_PER_CM = 10.0
MM_PER_QUARTER_MM = 0.25
MM_PER_INCH = 25.4
MM_PER_PICA = MM_PER_INCH / 6.0
MM_PER_POINT = MM_PER_INCH / 72.0


def css_dimension_to_mm(dimension, pixels_per_mm=96.0 / MM_PER_INCH):
    """
    Convert a CSS dimension string (e.g. '3cm') into a number of mm. Fails for
    non-absolute units of size.
    """
    match = re.match(r"^\s*[+]?\s*([0-9.]+)\s*(cm|mm|Q|in|pc|pt|px|)\s*$", dimension)
    if not match:
        raise ValueError(
            "{} is not a positive, absolute unit of size".format(repr(dimension))
        )

    number, unit = match.groups()
    number = float(number)

    if unit == "mm":
        pass
    elif unit == "cm":
        number *= MM_PER_CM
    elif unit == "Q":
        number *= MM_PER_QUARTER_MM
    elif unit == "in":
        number *= MM_PER_INCH
    elif unit == "pc":
        number *= MM_PER_PICA
    elif unit == "pt":
        number *= MM_PER_POINT
    elif unit == "px" or unit == "":
        number /= pixels_per_mm
    else:
        assert False, "Supposedly-supported unit not implemented!"

    return number


def get_svg_page_size(root, dpi: float = None, use_illustrator_heuristic: bool = True):
    """
    Given an ElementTree-parsed SVG file, return a (width_mm, height_mm) pair
    giving the page dimensions in mm.

    If the DPI argument is None (the default), the number of Dots (pixels) Per
    Inch (DPI) of the SVG is assumed to be the (standard-defined) 96 DPI
    unless:

    * The file was produced by an old version of Inkscape known to erroneously
      use 90 DPI instead.
    * The file was detected as being generated by Adobe Illustrator which
      erroneously uses 72 DPI. Illustrator SVG detection is based on a
      heuristic (since Illustrator-generated SVGs don't formally identify
      themselves). This heuristic can be disabled by setting
      use_illustrator_heuristic to False if you find other documents are being
      misidentified.

    Alternatively the dpi argument may be set directly and the specified DPI
    will be assumed regardless.
    """

    assert root.tag == "svg" or root.tag == "{{{}}}svg".format(SVG_NAMESPACE)

    if dpi is None:
        # As per the CSS spec
        dpi = 96

        # Certain older Inkscape versions used the wrong DPI
        inkscape_version = root.attrib.get("{{{}}}version".format(INKSCAPE_NAMESPACE))
        if inkscape_version:
            version_number = inkscape_version.partition(" ")[0]
            version_number_tuple = tuple(map(int, version_number.split(".")))
            if version_number_tuple < (0, 92, 0):
                dpi = 90

        # Unfortunately the comments left by Illustrator in its SVGs are not
        # accessible via Python's ElementTree library. (This includes more
        # recent versions which support comments since the comment lies outside
        # the document root and is therefore not exposed by ET).
        #
        # Instead we observe the Illustrator (at least in some modes...) sets
        # the (deprecated) enable-background attribute to "new <x> <y> <w> <h>"
        # where "<x> <y> <w> <h>" is the view box of the document.
        if use_illustrator_heuristic:
            enable_background = root.attrib.get("enable-background")
            view_box = root.attrib.get("viewBox", "")
            if enable_background == "new " + view_box:
                dpi = 72

    pixels_per_mm = dpi / MM_PER_INCH

    try:
        width = root.attrib["width"]
        height = root.attrib["height"]
    except KeyError:
        raise ValueError("'width' and 'height' must be specified for <svg> tag.")

    width_mm = css_dimension_to_mm(width, pixels_per_mm)
    height_mm = css_dimension_to_mm(height, pixels_per_mm)

    return (width_mm, height_mm)


def lines_polylines_and_polygons_to_paths(root):
    """
    Given an SVG, convert all <line>, <polyline> and <polygon> elements to
    equivalent <path> elements. This is intended purely as a workaround for
    PySide bug PYSIDE-891 which prevents processing of SVGs containing those
    element types. (See :py:mod:`svgoutline.outline_painter`.)

    If no substitutions are made, returns the original object unchanged,
    otherwise returns an edited copy.
    """
    if (
        root.find(f".//{{{SVG_NAMESPACE}}}line") is None
        and root.find(f".//{{{SVG_NAMESPACE}}}polyline") is None
        and root.find(f".//{{{SVG_NAMESPACE}}}polygon") is None
    ):
        # No substitutions required
        return root

    root = deepcopy(root)

    for line in root.findall(f".//{{{SVG_NAMESPACE}}}line"):
        line.tag = f"{{{SVG_NAMESPACE}}}path"
        x1 = line.attrib.pop("x1")
        y1 = line.attrib.pop("y1")
        x2 = line.attrib.pop("x2")
        y2 = line.attrib.pop("y2")
        line.set("d", f"M{x1} {y1} L{x2} {y2}")

    for tag, closed in [("polyline", False), ("polygon", True)]:
        for poly in root.findall(f".//{{{SVG_NAMESPACE}}}{tag}"):
            poly.tag = f"{{{SVG_NAMESPACE}}}path"

            # NB: Since this function is a workaround which hopefully won't
            # stick around forever I'm deliberately taking a casual approach to
            # parsing here since this will work for any valid (or
            # defacto-valid, i.e. comma-separated) SVG.
            points = map(
                float, re.split(r"\s*(?:,|\s)\s*", poly.attrib.pop("points").strip())
            )
            d = "M" + "L".join(f"{x} {y}" for x, y in zip(points, points))
            if closed:
                d += "Z"
            poly.set("d", d)

    return root
