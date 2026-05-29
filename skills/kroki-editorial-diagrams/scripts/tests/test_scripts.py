"""Basic regression tests for Kroki Editorial Diagrams scripts."""
import base64
import pathlib
import zlib

import pytest

import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from render_kroki_diagram import SUPPORTED_ENGINES, build_kroki_url
from build_diagram_index import build_index_html, build_diagram_index, META_FILENAME
from build_interactive_kroki_html import annotate_svg, build_interactive_html_file


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
