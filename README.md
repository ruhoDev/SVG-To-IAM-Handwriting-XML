SVG To IAM Handwriting XML
==========================

My script extracts all strokes from SVG using svg.path, then convert 
Bezier curve lines to all points on the curve.
Then my script convert SVG to XML format what used in IAM Handwriting.


Usage
-----

Python 
    $ Install Python 3.6


Limitations
-----------

* **Only [SVG Tiny 1.2](https://www.w3.org/TR/SVGTiny12/) is supported** due to the
  use of [Qt SVG](http://doc.qt.io/qt-5/qtsvg-index.html) internally. The
  following significant features are missing which you might otherwise expect:
  * Clipping masks are not supported and will be ignored.
  * Many text features beyond simple single-line text strings are not
    supported, for example text on path, line wrapping or style changes mid
    text element.
* **Depends on [Qt for Python (a.k.a.
  PySide6)](https://wiki.qt.io/Qt_for_Python).**  This is a relatively
  non-trivial dependency but is easy to install from
  [PyPI](https://pypi.org/project/PySide6/) on most platforms. Unfortunately it
  makes svgoutline subject to the same bugs (e.g.
  [QTBUG-72997](https://bugreports.qt.io/browse/QTBUG-72997) which at the time
  of writing causes text outlines and dash patterns to render too small).
* **Oblivious to fills and overlaps.** Consequently, if two shapes overlap,
  their full outlines will be included in the output regardless of what parts
  of their outlines are actually visible. For plotting purposes this should not
  be a significant problem as input SVGs are unlikely to contain filled
  elements.
* **Output does not distinguish between closed paths and paths whose start and
  end coordinates are the same.** This distinction is not important for most
  plotting applications.


Tests
-----

The tests are written using [py.test](https://docs.pytest.org/en/latest/) and
test dependencies can be installed and the tests executed with:

    $ pip install -r requirements-test.txt

There are two versions for testing: gen_outline.py, parse_xml.py. You can choose
any format according to your prepared svg files.
Then you can convert SVG files by following commands.

    $ python gen_outline.py
    or 
    $ python parse_xml.py