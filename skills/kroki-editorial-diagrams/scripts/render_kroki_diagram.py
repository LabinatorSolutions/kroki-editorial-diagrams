#!/usr/bin/env python3
import argparse
import base64
import json
import pathlib
import urllib.request
import urllib.error
import sys
import zlib

# Robust sibling import resolution
sys.path.append(str(pathlib.Path(__file__).parent.resolve()))
from build_diagram_index import META_FILENAME, build_diagram_index
from build_interactive_kroki_html import build_interactive_html_file

SUPPORTED_ENGINES = [
    # Core editorial engines (full styling + interactive support)
    "plantuml",
    "c4plantuml",
    "d2",
    "mermaid",
    "graphviz",
    "bpmn",
    "erd",
    # Extended engines (built-in to Kroki gateway)
    "structurizr",
    "ditaa",
    "nomnoml",
    "svgbob",
    "pikchr",
    "goat",
    "bytefield",
    "wavedrom",
    "wireviz",
    "actdiag",
    "blockdiag",
    "seqdiag",
    "nwdiag",
    "packetdiag",
    "rackdiag",
    "symbolator",
    "umlet",
    # Companion-server engines (require separate Docker container in self-hosted Kroki)
    "excalidraw",
    "diagramsnet",
    "vega",
    "vegalite",
]


def build_kroki_url(engine: str, fmt: str, source: str, endpoint: str = "https://kroki.io") -> str:
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(source.encode("utf-8")) + compressor.flush()
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii").rstrip("=")
    return f"{endpoint}/{engine}/{fmt}/{encoded}"


def render(
    engine: str,
    fmt: str,
    source: str,
    endpoint: str = "https://kroki.io",
    diagram_options: list[tuple[str, str]] | None = None,
    timeout: int = 30,
) -> bytes:
    url = f"{endpoint}/{engine}/{fmt}"
    headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    for key, value in (diagram_options or []):
        # Capitalise each word of the key to match Kroki header convention:
        # e.g. "no-metadata" → "Kroki-Diagram-Options-No-Metadata"
        header_key = "Kroki-Diagram-Options-" + "-".join(
            word.capitalize() for word in key.replace("_", "-").split("-")
        )
        headers[header_key] = value

    req = urllib.request.Request(
        url,
        data=source.encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace").strip()
        except Exception:
            err_body = ""
        raise RuntimeError(err_body or f"Kroki server returned HTTP status {e.code}")
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render diagrams through Kroki with premium formatting."
    )
    parser.add_argument(
        "--engine",
        required=True,
        choices=SUPPORTED_ENGINES,
        help="Kroki engine to use.",
    )
    parser.add_argument("--input", required=True, help="Path to diagram source file.")
    parser.add_argument(
        "--format",
        default="svg",
        choices=["svg", "png", "pdf", "jpg"],
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        help="Path to write the rendered output. Defaults next to input with matching extension.",
    )
    parser.add_argument(
        "--interactive-output",
        help="Optional HTML output path for an interactive SVG wrapper.",
    )
    parser.add_argument(
        "--interactive-title",
        help="Title used by the interactive HTML wrapper.",
    )
    parser.add_argument(
        "--summary",
        help="Optional short summary stored for generated index pages.",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Do not create or update the parent index.html.",
    )
    parser.add_argument(
        "--print-url-only",
        action="store_true",
        help="Only print the shareable Kroki GET URL and do not render via POST.",
    )
    parser.add_argument(
        "--kroki-endpoint",
        default="https://kroki.io",
        help="Custom Kroki server endpoint (for self-hosted instances).",
    )
    parser.add_argument(
        "--diagram-option",
        action="append",
        metavar="KEY=VALUE",
        dest="diagram_options",
        help=(
            "Pass a diagram option to Kroki (repeatable). "
            "Sent as a Kroki-Diagram-Options-* HTTP header. "
            "Example: --diagram-option theme=earth-tones"
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="curl --max-time value in seconds (default: 30). Increase for slow self-hosted instances.",
    )
    args = parser.parse_args()

    # Parse --diagram-option KEY=VALUE pairs
    diagram_options: list[tuple[str, str]] = []
    for opt in args.diagram_options or []:
        if "=" not in opt:
            print(f"Invalid --diagram-option '{opt}': expected KEY=VALUE format", file=sys.stderr)
            return 1
        key, _, value = opt.partition("=")
        diagram_options.append((key.strip(), value.strip()))

    input_path = pathlib.Path(args.input)
    source = input_path.read_text(encoding="utf-8")
    url = build_kroki_url(args.engine, args.format, source, endpoint=args.kroki_endpoint)

    if args.print_url_only:
        print(url)
        return 0

    output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(f".{args.format}")

    try:
        rendered = render(
            args.engine,
            args.format,
            source,
            endpoint=args.kroki_endpoint,
            diagram_options=diagram_options,
            timeout=args.timeout,
        )
    except RuntimeError as exc:
        print(f"Render failed: {exc}", file=sys.stderr)
        print(f"Kroki URL: {url}", file=sys.stderr)
        return 1

    # Scan up to 4096 bytes for the SVG tag to handle large XML preambles safely
    text_probe = rendered[:4096].decode("utf-8", errors="ignore")
    if "<svg" not in text_probe and args.format == "svg":
        print("Render failed: Kroki did not return SVG output", file=sys.stderr)
        print(text_probe.strip(), file=sys.stderr)
        print(f"Kroki URL: {url}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(rendered)
    print(f"Rendered: {output_path}")

    interactive_summary = None
    if args.interactive_output:
        if args.format != "svg":
            print("Interactive build failed: --interactive-output requires --format svg", file=sys.stderr)
            return 1
        interactive_path = pathlib.Path(args.interactive_output)
        title = args.interactive_title or input_path.stem.replace("-", " ").title()
        interactive_summary = build_interactive_html_file(
            engine=args.engine,
            svg_text=rendered.decode("utf-8"),
            output_path=interactive_path,
            title=title,
        )
        print(f"Interactive HTML: {interactive_path}")
        print(
            "Interactive summary:"
            f" tier={interactive_summary['tier']}"
            f" nodes={interactive_summary['nodes']}"
            f" edges={interactive_summary['edges']}"
        )

    artifact_dir = output_path.parent
    title = args.interactive_title or input_path.stem.replace("-", " ").title()
    meta = {
        "title": title,
        "engine": args.engine,
        "format": args.format,
        "summary": args.summary or f"Rendered with {args.engine}.",
    }
    if interactive_summary:
        meta["interactive_tier"] = interactive_summary["tier"]
    (artifact_dir / META_FILENAME).write_text(json.dumps(meta, indent=2), encoding="utf-8")

    if not args.skip_index and output_path.name == "rendered.svg":
        index_path = build_diagram_index(root=artifact_dir.parent)
        print(f"Index HTML: {index_path}")

    print(f"Kroki URL: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
