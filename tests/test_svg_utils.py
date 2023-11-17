import pytest

from xml.etree import ElementTree

from svgoutline.svg_utils import (
    css_dimension_to_mm,
    get_svg_page_size,
)


class TestCssDimensionToMm(object):

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_mm_and_formatting(self, ppmm):
        # Integer and float support
        assert css_dimension_to_mm("123mm", ppmm) == 123
        assert css_dimension_to_mm("1.23mm", ppmm) == 1.23

        # With optional plus
        assert css_dimension_to_mm("+1mm", ppmm) == 1

        # With whitespace
        assert css_dimension_to_mm(" 1 mm ", ppmm) == 1
        assert css_dimension_to_mm(" + 1 mm ", ppmm) == 1

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_cm(self, ppmm):
        assert css_dimension_to_mm("1.2cm", ppmm) == 12.0

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_Q(self, ppmm):
        assert css_dimension_to_mm("1Q", ppmm) == 0.25
        assert css_dimension_to_mm("4Q", ppmm) == 1.0

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_inches(self, ppmm):
        assert css_dimension_to_mm("1in", ppmm) == 25.4
        assert css_dimension_to_mm("2in", ppmm) == 50.8

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_pica(self, ppmm):
        assert css_dimension_to_mm("6pc", ppmm) == \
            css_dimension_to_mm("1in", ppmm)

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_point(self, ppmm):
        assert css_dimension_to_mm("72pt", ppmm) == \
            css_dimension_to_mm("1in", ppmm)

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_pixels(self, ppmm):
        assert css_dimension_to_mm("1px", ppmm) == 1.0 / ppmm
        assert css_dimension_to_mm("1", ppmm) == 1.0 / ppmm

        assert css_dimension_to_mm("2px", ppmm) == 2.0 / ppmm
        assert css_dimension_to_mm("2", ppmm) == 2.0 / ppmm

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_unsupported_units(self, ppmm):
        # No font-relative sizes
        with pytest.raises(ValueError):
            css_dimension_to_mm("1em", ppmm)

        # No viewport-relative sizes
        with pytest.raises(ValueError):
            css_dimension_to_mm("1vw", ppmm)
        with pytest.raises(ValueError):
            css_dimension_to_mm("1%", ppmm)

    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_negative(self, ppmm):
        with pytest.raises(ValueError):
            css_dimension_to_mm("-1mm", ppmm)

    @pytest.mark.parametrize("value", [
        # No number
        "",
        "mm",
        # Invalid/malformed number
        "1.2.3",  # >1 decimal
        "1,2mm",  # Comma
        "1 2mm",  # Space
        # Other content in string
        "foo 10 mm",
        "10 bar mm",
        "10 mm baz",
        # Multiple units
        "1 px mm",
        # Wrong case
        "1MM",
    ])
    @pytest.mark.parametrize("ppmm", [96.0/25.4, 90.0/25.4])
    def test_malformed(self, value, ppmm):
        with pytest.raises(ValueError):
            css_dimension_to_mm(value, ppmm)


class TestGetSvgPageSize(object):

    def test_minimal_svg(self):
        # Pixels at 96 dpi
        svg = ElementTree.fromstring('<svg width="96" height="192" />')
        assert get_svg_page_size(svg) == (25.4, 50.8)

    def test_modern_inkscape_svg_pixels(self):
        # An A4 empty SVG generated by Inkscape 0.92
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!-- Created with Inkscape (http://www.inkscape.org/) -->

            <svg
               xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:cc="http://creativecommons.org/ns#"
               xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
               xmlns:svg="http://www.w3.org/2000/svg"
               xmlns="http://www.w3.org/2000/svg"
               xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
               xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
               width="96"
               height="192"
               viewBox="0 0 25.4 50.800001"
               version="1.1"
               id="svg11896"
               inkscape:version="0.92.2 2405546, 2018-03-11"
               sodipodi:docname="pixels.svg">
              <defs
                 id="defs11890" />
              <sodipodi:namedview
                 id="base"
                 pagecolor="#ffffff"
                 bordercolor="#666666"
                 borderopacity="1.0"
                 inkscape:pageopacity="0.0"
                 inkscape:pageshadow="2"
                 inkscape:zoom="2.36"
                 inkscape:cx="50"
                 inkscape:cy="100"
                 inkscape:document-units="mm"
                 inkscape:current-layer="layer1"
                 showgrid="false"
                 units="px"
                 inkscape:window-width="956"
                 inkscape:window-height="1044"
                 inkscape:window-x="0"
                 inkscape:window-y="16"
                 inkscape:window-maximized="0" />
              <metadata
                 id="metadata11893">
                <rdf:RDF>
                  <cc:Work
                     rdf:about="">
                    <dc:format>image/svg+xml</dc:format>
                    <dc:type
                       rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                    <dc:title></dc:title>
                  </cc:Work>
                </rdf:RDF>
              </metadata>
              <g
                 inkscape:label="Layer 1"
                 inkscape:groupmode="layer"
                 id="layer1"
                 transform="translate(0,-246.19999)" />
            </svg>
        """)
        # 1x2inches at 96 DPI
        assert get_svg_page_size(svg) == (25.4, 50.8)

    def test_modern_inkscape_svg_mm(self):
        # An A4 empty SVG generated by Inkscape 0.92
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!-- Created with Inkscape (http://www.inkscape.org/) -->

            <svg
               xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:cc="http://creativecommons.org/ns#"
               xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
               xmlns:svg="http://www.w3.org/2000/svg"
               xmlns="http://www.w3.org/2000/svg"
               xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
               xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
               width="210mm"
               height="297mm"
               viewBox="0 0 210 297"
               version="1.1"
               id="svg8"
               inkscape:version="0.92.2 2405546, 2018-03-11"
               sodipodi:docname="a4.svg">
              <defs
                 id="defs2" />
              <sodipodi:namedview
                 id="base"
                 pagecolor="#ffffff"
                 bordercolor="#666666"
                 borderopacity="1.0"
                 inkscape:pageopacity="0.0"
                 inkscape:pageshadow="2"
                 inkscape:zoom="1.1078846"
                 inkscape:cx="120.48603"
                 inkscape:cy="552.48047"
                 inkscape:document-units="mm"
                 inkscape:current-layer="layer1"
                 showgrid="false"
                 inkscape:window-width="956"
                 inkscape:window-height="1044"
                 inkscape:window-x="0"
                 inkscape:window-y="16"
                 inkscape:window-maximized="0" />
              <metadata
                 id="metadata5">
                <rdf:RDF>
                  <cc:Work
                     rdf:about="">
                    <dc:format>image/svg+xml</dc:format>
                    <dc:type
                       rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                    <dc:title></dc:title>
                  </cc:Work>
                </rdf:RDF>
              </metadata>
              <g
                 inkscape:label="Layer 1"
                 inkscape:groupmode="layer"
                 id="layer1" />
            </svg>
        """)
        assert get_svg_page_size(svg) == (210.0, 297.0)

    def test_legacy_inkscape_svg(self):
        # An A4 empty SVG generated by Inkscape 0.46 (with width/height in 90
        # DPI pixels)
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!-- Created with Inkscape (http://www.inkscape.org/) -->
            <svg
               xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:cc="http://creativecommons.org/ns#"
               xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
               xmlns:svg="http://www.w3.org/2000/svg"
               xmlns="http://www.w3.org/2000/svg"
               xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
               xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
               width="744.09448819"
               height="1052.3622047"
               id="svg2"
               sodipodi:version="0.32"
               inkscape:version="0.46"
               sodipodi:docname="legacy.svg"
               inkscape:output_extension="org.inkscape.output.svg.inkscape">
              <defs
                 id="defs4">
                <inkscape:perspective
                   sodipodi:type="inkscape:persp3d"
                   inkscape:vp_x="0 : 526.18109 : 1"
                   inkscape:vp_y="0 : 1000 : 0"
                   inkscape:vp_z="744.09448 : 526.18109 : 1"
                   inkscape:persp3d-origin="372.04724 : 350.78739 : 1"
                   id="perspective10" />
              </defs>
              <sodipodi:namedview
                 id="base"
                 pagecolor="#ffffff"
                 bordercolor="#666666"
                 borderopacity="1.0"
                 gridtolerance="10000"
                 guidetolerance="10"
                 objecttolerance="10"
                 inkscape:pageopacity="0.0"
                 inkscape:pageshadow="2"
                 inkscape:zoom="2"
                 inkscape:cx="285.58936"
                 inkscape:cy="628.96054"
                 inkscape:document-units="px"
                 inkscape:current-layer="layer1"
                 showgrid="false"
                 showguides="true"
                 inkscape:guide-bbox="true" />
              <metadata
                 id="metadata7">
                <rdf:RDF>
                  <cc:Work
                     rdf:about="">
                    <dc:format>image/svg+xml</dc:format>
                    <dc:type
                       rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                  </cc:Work>
                </rdf:RDF>
              </metadata>
              <g
                 inkscape:label="Layer 1"
                 inkscape:groupmode="layer"
                 id="layer1"></g>
            </svg>
        """)
        assert get_svg_page_size(svg) == pytest.approx((210, 297))
    
    def test_illustrator_svg(self):
        # An A3 SVG generated by Adobe Illustrator (with width/height in 72 DPI
        # pixels)
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="iso-8859-1"?>
            <!-- Generator: Adobe Illustrator 27.8.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
            <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                width="841.89px" height="1190.551px" viewBox="0 0 841.89 1190.551" enable-background="new 0 0 841.89 1190.551"
                xml:space="preserve">
            <rect x="80" y="117" fill="#FFFFFF" stroke="#000000" stroke-miterlimit="10" width="216" height="271"/>

            </svg>
        """)
        assert get_svg_page_size(svg) == pytest.approx((297, 420))
    
    def test_illustrator_heuristic_disabled(self):
        # An A3 SVG generated by Adobe Illustrator (with width/height in 72 DPI
        # pixels)
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="iso-8859-1"?>
            <!-- Generator: Adobe Illustrator 27.8.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
            <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                width="841.89px" height="1190.551px" viewBox="0 0 841.89 1190.551" enable-background="new 0 0 841.89 1190.551"
                xml:space="preserve">
            <rect x="80" y="117" fill="#FFFFFF" stroke="#000000" stroke-miterlimit="10" width="216" height="271"/>

            </svg>
        """)
        assert get_svg_page_size(
            svg,
            use_illustrator_heuristic=False,
        ) == pytest.approx((297 / (96 / 72), 420 / (96 / 72)))
    
    def test_dpi_override(self):
        # An A3 SVG generated by Adobe Illustrator (with width/height in 72 DPI
        # pixels)
        svg = ElementTree.fromstring("""<?xml version="1.0" encoding="iso-8859-1"?>
            <!-- Generator: Adobe Illustrator 27.8.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
            <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                width="841.89px" height="1190.551px" viewBox="0 0 841.89 1190.551" enable-background="new 0 0 841.89 1190.551"
                xml:space="preserve">
            <rect x="80" y="117" fill="#FFFFFF" stroke="#000000" stroke-miterlimit="10" width="216" height="271"/>

            </svg>
        """)
        assert get_svg_page_size(svg, dpi=72/2) == pytest.approx((297 * 2, 420 * 2))
