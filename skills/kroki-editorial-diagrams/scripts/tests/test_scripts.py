"""Basic regression tests for Kroki Editorial Diagrams scripts."""
import base64
import pathlib
import zlib
from unittest.mock import MagicMock, patch

import pytest

import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from render_kroki_diagram import SUPPORTED_ENGINES, build_kroki_url, render
from build_diagram_index import build_index_html, build_diagram_index, META_FILENAME, infer_engine_from_source
from build_interactive_kroki_html import annotate_svg, build_interactive_html_file, soften_svg_background
from defusedxml.ElementTree import fromstring as safe_fromstring


# ---------------------------------------------------------------------------
# render_kroki_diagram
# ---------------------------------------------------------------------------

def test_d2_in_supported_engines():
    assert "d2" in SUPPORTED_ENGINES


def test_all_expected_engines_present():
    expected = {"plantuml", "c4plantuml", "d2", "mermaid", "graphviz", "bpmn", "erd"}
    assert expected.issubset(set(SUPPORTED_ENGINES))


def test_build_kroki_url_roundtrip():
    source = "@startuml\nA -> B : hello\n@enduml"
    url = build_kroki_url("plantuml", "svg", source)
    assert url.startswith("https://kroki.io/plantuml/svg/")
    # Verify the payload decodes back to the original source
    encoded = url.split("/")[-1]
    # Restore base64 padding
    padded = encoded + "=" * (-len(encoded) % 4)
    compressed = base64.urlsafe_b64decode(padded)
    decompressed = zlib.decompress(compressed, wbits=-15)
    assert decompressed.decode("utf-8") == source


# ---------------------------------------------------------------------------
# build_diagram_index — pluralization
# ---------------------------------------------------------------------------

def _make_entry(name: str) -> dict:
    return {
        "folder": name,
        "title": name.replace("-", " ").title(),
        "engine": "plantuml",
        "tier": "full",
        "summary": "Test diagram.",
        "interactive_href": f"./{name}/interactive.html",
        "interactive_exists": "true",
        "svg_href": f"./{name}/rendered.svg",
    }


def test_pluralization_singular():
    html = build_index_html([_make_entry("auth-flow")], "Test")
    assert "1 diagram<" in html
    assert '{"s"' not in html


def test_pluralization_plural():
    entries = [_make_entry(f"diagram-{i}") for i in range(5)]
    html = build_index_html(entries, "Test")
    assert "5 diagrams<" in html
    assert '{"s"' not in html


def test_build_diagram_index_creates_file(tmp_path):
    artifact = tmp_path / "auth-flow"
    artifact.mkdir()
    (artifact / "rendered.svg").write_text("<svg></svg>")
    (artifact / META_FILENAME).write_text('{"title":"Auth Flow","engine":"plantuml","summary":"Test."}')
    index = build_diagram_index(root=tmp_path)
    assert index.exists()
    content = index.read_text()
    assert "Auth Flow" in content
    assert "1 diagram<" in content


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — annotate_svg
# ---------------------------------------------------------------------------

GRAPHVIZ_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <g id="node1" class="node"><title>A</title><ellipse/><text>A</text></g>
  <g id="node2" class="node"><title>B</title><ellipse/><text>B</text></g>
  <g id="edge1" class="edge"><title>A-&gt;B</title><path/></g>
</svg>"""


def test_annotate_graphviz_detects_nodes_and_edges():
    _, meta = annotate_svg("graphviz", GRAPHVIZ_SVG)
    assert meta["nodes"] == 2
    assert meta["edges"] == 1
    assert meta["tier"] in ("full", "best-effort")


def test_annotate_d2_uses_graphviz_conventions():
    _, meta = annotate_svg("d2", GRAPHVIZ_SVG)
    assert meta["nodes"] == 2
    assert meta["edges"] == 1


def test_annotate_unknown_engine_is_limited():
    _, meta = annotate_svg("bpmn", "<svg xmlns='http://www.w3.org/2000/svg'></svg>")
    assert meta["tier"] == "limited"
    assert meta["nodes"] == 0


def test_build_interactive_html_file_writes_output(tmp_path):
    out = tmp_path / "interactive.html"
    build_interactive_html_file(
        engine="graphviz",
        svg_text=GRAPHVIZ_SVG,
        output_path=out,
        title="Test Diagram",
    )
    assert out.exists()
    content = out.read_text()
    assert "Test Diagram" in content
    assert "interactive-node" in content


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — edge label parsing
# ---------------------------------------------------------------------------

GRAPHVIZ_SVG_EDGE = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <g id="node1" class="node"><title>A</title><ellipse/><text>A</text></g>
  <g id="node2" class="node"><title>B</title><ellipse/><text>B</text></g>
  <g id="edge1" class="edge"><title>A-&gt;B</title><path/></g>
</svg>"""


def test_annotate_graphviz_parses_edge_labels():
    annotated, meta = annotate_svg("graphviz", GRAPHVIZ_SVG_EDGE)
    assert meta["edges"] == 1
    assert meta["nodes"] == 2
    assert "data-edge-source" in annotated
    assert "data-edge-target" in annotated
    assert 'data-edge-source="A"' in annotated
    assert 'data-edge-target="B"' in annotated
    assert 'data-edge-kind="directed"' in annotated


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — plantuml sequence annotation
# ---------------------------------------------------------------------------

PLANTUML_SEQUENCE_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" data-diagram-type="SEQUENCE" viewBox="0 0 400 300">
  <g class="participant-head" data-entity-uid="client">
    <text>Client</text>
  </g>
  <g class="participant-lifeline" data-entity-uid="server">
    <text>Server</text>
  </g>
  <g class="message" data-entity-1="client" data-entity-2="server">
    <text>GET /api</text>
  </g>
</svg>"""


def test_annotate_sequence_detects_participants_and_messages():
    annotated, meta = annotate_svg("plantuml", PLANTUML_SEQUENCE_SVG)
    assert meta["nodes"] == 2
    assert meta["edges"] == 1
    assert meta["tier"] == "full"
    assert "data-node-id" in annotated
    assert "data-edge-source" in annotated


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — mermaid annotation
# ---------------------------------------------------------------------------

MERMAID_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <g id="flowchart-A-42" class="node">
    <text>A</text>
  </g>
  <g id="flowchart-B-43" class="node">
    <text>B</text>
  </g>
  <g id="L_A_B_0" class="flowchart-link" marker-end="url(#arrowhead)">
    <path/>
  </g>
</svg>"""


def test_annotate_mermaid_detects_nodes_and_edges():
    annotated, meta = annotate_svg("mermaid", MERMAID_SVG)
    assert meta["nodes"] == 2
    assert meta["edges"] == 1
    assert meta["tier"] == "best-effort"
    assert "data-node-id" in annotated
    assert "data-edge-source" in annotated
    assert "data-edge-kind" in annotated


# ---------------------------------------------------------------------------
# build_diagram_index — engine inference from source files
# ---------------------------------------------------------------------------

def test_infer_engine_detects_d2_source(tmp_path):
    (tmp_path / "source.d2").write_text("direction: down")
    assert infer_engine_from_source(tmp_path) == "d2"


def test_infer_engine_detects_plantuml_source(tmp_path):
    (tmp_path / "source.puml").write_text("@startuml")
    assert infer_engine_from_source(tmp_path) == "plantuml"


def test_infer_engine_detects_mermaid_source(tmp_path):
    (tmp_path / "source.mmd").write_text("flowchart TD")
    assert infer_engine_from_source(tmp_path) == "mermaid"


def test_infer_engine_detects_graphviz_source(tmp_path):
    (tmp_path / "source.dot").write_text("digraph {}")
    assert infer_engine_from_source(tmp_path) == "graphviz"


def test_infer_engine_detects_erd_source(tmp_path):
    (tmp_path / "source.erd").write_text("[table]")
    assert infer_engine_from_source(tmp_path) == "erd"


def test_infer_engine_defaults_when_no_source(tmp_path):
    assert infer_engine_from_source(tmp_path) == "diagram"


# ---------------------------------------------------------------------------
# render_kroki_diagram — new format + engine coverage
# ---------------------------------------------------------------------------

def test_jpg_format_builds_valid_url():
    url = build_kroki_url("mermaid", "jpg", "flowchart TD\n  A --> B")
    assert "/mermaid/jpg/" in url


def test_extended_engines_present():
    extended = {"structurizr", "ditaa", "nomnoml", "svgbob", "wavedrom", "vega", "vegalite", "excalidraw"}
    assert extended.issubset(set(SUPPORTED_ENGINES))


def test_diagram_option_curl_headers():
    mock_response = MagicMock()
    mock_response.read.return_value = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        render(
            "d2", "svg", "direction: down",
            diagram_options=[("theme", "earth-tones"), ("layout", "elk")],
        )
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Kroki-diagram-options-theme") == "earth-tones"
        assert req.get_header("Kroki-diagram-options-layout") == "elk"


def test_diagram_option_no_options_produces_no_extra_headers():
    mock_response = MagicMock()
    mock_response.read.return_value = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        render("graphviz", "svg", "digraph G {}")
        req = mock_urlopen.call_args[0][0]
        assert not any(key.startswith("Kroki-diagram-options") for key in req.headers)


def test_timeout_is_passed_to_curl():
    mock_response = MagicMock()
    mock_response.read.return_value = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        render("plantuml", "svg", "@startuml\n@enduml", timeout=90)
        assert mock_urlopen.call_args[1]["timeout"] == 90


# ---------------------------------------------------------------------------
# build_diagram_index — new engine inference extensions
# ---------------------------------------------------------------------------

def test_infer_engine_detects_c4puml_source(tmp_path):
    (tmp_path / "source.c4puml").write_text("!include <C4Container>")
    assert infer_engine_from_source(tmp_path) == "c4plantuml"


def test_infer_engine_detects_structurizr_source(tmp_path):
    (tmp_path / "source.structurizr").write_text("workspace {}")
    assert infer_engine_from_source(tmp_path) == "structurizr"


def test_infer_engine_detects_wavedrom_source(tmp_path):
    (tmp_path / "source.wsd").write_text('{"signal":[]}')
    assert infer_engine_from_source(tmp_path) == "wavedrom"


def test_infer_engine_detects_vega_source(tmp_path):
    (tmp_path / "source.vega").write_text('{"$schema":""}')
    assert infer_engine_from_source(tmp_path) == "vega"


def test_infer_engine_detects_svgbob_source(tmp_path):
    (tmp_path / "source.svgbob").write_text(".--.")
    assert infer_engine_from_source(tmp_path) == "svgbob"


def test_infer_engine_detects_plantuml_pu_extension(tmp_path):
    (tmp_path / "source.pu").write_text("@startuml")
    assert infer_engine_from_source(tmp_path) == "plantuml"


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — ERD and BPMN paths
# ---------------------------------------------------------------------------

ERD_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
  <g id="node1" class="node"><title>users</title><polygon/><text>users</text></g>
  <g id="node2" class="node"><title>posts</title><polygon/><text>posts</text></g>
  <g id="edge1" class="edge"><title>users-&gt;posts</title><path/></g>
</svg>"""

BPMN_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200">
  <g class="djs-group">
    <circle class="djs-element" cx="50" cy="100" r="18"/>
  </g>
</svg>"""


def test_annotate_erd_uses_graphviz_path():
    _, meta = annotate_svg("erd", ERD_SVG)
    assert meta["nodes"] == 2
    assert meta["edges"] == 1
    assert meta["tier"] == "best-effort"


def test_annotate_bpmn_is_limited():
    _, meta = annotate_svg("bpmn", BPMN_SVG)
    assert meta["tier"] == "limited"
    assert meta["nodes"] == 0
    assert meta["edges"] == 0


# ---------------------------------------------------------------------------
# build_interactive_kroki_html — soften_svg_background
# ---------------------------------------------------------------------------

def _make_svg_with_bg_rect(width: int = 200, height: int = 200) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff" style="stroke:none"/>'
        f'<g class="node"><title>A</title></g>'
        f"</svg>"
    )


def test_soften_svg_background_removes_background_rect():
    svg_text = _make_svg_with_bg_rect(200, 200)
    root = safe_fromstring(svg_text)
    rects_before = root.findall(".//{http://www.w3.org/2000/svg}rect")
    assert len(rects_before) == 1

    soften_svg_background(root)

    rects_after = root.findall(".//{http://www.w3.org/2000/svg}rect")
    assert len(rects_after) == 0


def test_soften_svg_background_preserves_non_background_rects():
    svg_text = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
        '<rect x="0" y="0" width="200" height="200" fill="#ffffff" style="stroke:none"/>'
        '<rect x="10" y="10" width="50" height="30" fill="#ececec"/>'
        "</svg>"
    )
    root = safe_fromstring(svg_text)
    soften_svg_background(root)
    rects_after = root.findall(".//{http://www.w3.org/2000/svg}rect")
    # Background rect removed; content rect kept
    assert len(rects_after) == 1
    assert rects_after[0].get("x") == "10"
