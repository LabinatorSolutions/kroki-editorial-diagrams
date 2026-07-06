# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install Python dependency (only external dep)
pip install defusedxml           # Linux/macOS
pacman -S python-defusedxml      # Arch/Manjaro

# Run full test suite (run from scripts directory)
cd skills/kroki-editorial-diagrams/scripts && python -m pytest tests/ -v

# Run a single test
cd skills/kroki-editorial-diagrams/scripts && python -m pytest tests/test_scripts.py::test_build_kroki_url_roundtrip -v

# Render a diagram to SVG with interactive HTML overlay
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine d2 \
  --input docs/examples/architecture-d2/source.d2 \
  --output docs/examples/architecture-d2/rendered.svg \
  --interactive-output docs/examples/architecture-d2/interactive.html \
  --interactive-title "Architecture Overview" \
  --summary "Container layout for production microservices."

# Render to PNG, PDF, or JPG (--interactive-output unavailable for non-SVG)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine mermaid --format png --input path/to/source.mmd --output out.png

# Second-pass PNG after SVG (--skip-index avoids redundant gallery rebuild)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine d2 --format png --skip-index --input source.d2 --output rendered.png

# Pass diagram options (D2 theme, layout; PlantUML theme; etc.)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine d2 --input source.d2 --output rendered.svg \
  --diagram-option theme=earth-tones \
  --diagram-option layout=elk

# Use a self-hosted Kroki instance; increase timeout if server is slow
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine plantuml --input src.puml --output out.svg \
  --kroki-endpoint https://kroki.example.com \
  --timeout 60

# Print shareable Kroki URL without rendering (offline / debug)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine mermaid --input path/to/source.mmd --print-url-only

# Wrap an existing SVG directly (bypasses Kroki API)
python3 skills/kroki-editorial-diagrams/scripts/build_interactive_kroki_html.py \
  --engine d2 --input rendered.svg --output interactive.html --title "My Diagram"

# Rebuild the gallery index from an existing artifact directory
python3 skills/kroki-editorial-diagrams/scripts/build_diagram_index.py \
  --root docs/examples --title "My Diagram Gallery"
```

## Architecture

This repo is a Claude Code / Antigravity IDE (Gemini CLI) **skill** — an LLM instruction set backed by Python tooling that generates premium interactive diagram outputs.

### Entry point

`skills/kroki-editorial-diagrams/SKILL.md` is the LLM instruction set. It defines the 8-step workflow, engine selection logic, mandatory design rules (Narrow & Tall layout, 60-30-10 color system), and execution commands. The skill is installed as a symlink in `~/.claude/skills/` and `~/.gemini/config/skills/`.

### Dependencies

`scripts/requirements.txt` lists the single external dependency (`defusedxml`). Use `pip install -r skills/kroki-editorial-diagrams/scripts/requirements.txt` when setting up CI or a virtualenv.

### Python scripts

**`render_kroki_diagram.py`** — the CLI. It reads the source file, POSTs to the Kroki API via standard Python `urllib` (always `Content-Type: text/plain; charset=utf-8` to handle `%` characters safely), writes the rendered output, then calls the other two modules. Supports `--diagram-option key=value` (repeatable) to pass engine-specific Kroki options as `Kroki-Diagram-Options-*` headers, `--format jpg` (in addition to svg/png/pdf), and `--timeout` for slow self-hosted instances. Index auto-build fires only when the output filename is exactly `rendered.svg`; use `--skip-index` to suppress it.

**`build_interactive_kroki_html.py`** — wraps a rendered SVG in an HTML page with click-to-highlight node focus, animated directional edge flows, and pan/zoom. Annotates the raw SVG with `data-node-id`, `data-edge-source`, `data-edge-target` attributes. Uses `defusedxml` for XXE-safe SVG parsing. Interactive tier varies by engine: `full` (PlantUML, C4-PlantUML, Graphviz, D2*, Structurizr*); `best-effort` (Mermaid, ERD); `limited` (BPMN and ~20 others — stderr note printed). *D2 and Structurizr fall back to `best-effort` when no edges are detected.

**`build_diagram_index.py`** — scans a root folder for subfolders containing `rendered.svg` + `.diagram-meta.json`, then generates a dark-mode gallery `index.html`. Metadata is written by the render script after each successful render. The `.diagram-meta.json` schema (exactly the keys `render_kroki_diagram.py` writes):

```json
{ "title": "Architecture Overview", "engine": "d2", "format": "svg",
  "summary": "...", "interactive_tier": "full" }
```

`interactive_tier` is present only when `--interactive-output` was used. The gallery card fields (`folder`, `interactive_exists`, `interactive_href`, `svg_href`, `tier`) are **computed at index time** by `load_artifact_entry()` from the folder contents — they are not stored in the meta file.

**`_svg_utils.py`** — private module: SVG namespace constants (`SVG_NS`, `NS`), `clean_svg_text`, `append_class`, `soften_svg_background`. Imported by `_svg_annotators.py`.

**`_svg_annotators.py`** — private module: all annotation functions (`annotate_graphviz_like`, `annotate_mermaid`, `annotate_d2`, `annotate_sequence`, `annotate_plantuml_description`) and the `annotate_svg` dispatcher. Engines without a dedicated annotator fall through to `limited` tier; `build_interactive_html_file` prints a stderr warning in that case.

**`_version.py`** — private module: reads `__version__` from the repo-root `package.json` (single source of truth), resolving through the installed skill's symlink via `parents[3]`. Falls back to `0.0.0+unknown` if `package.json` is unreachable. Imported by all three CLIs for `--version`.

### Reference docs

`skills/kroki-editorial-diagrams/references/` holds nine markdown files loaded by the skill during diagram generation:

- `engine-matrix.md` — engine trade-offs and ideal scenarios
- `engine-style-templates.md` — copy-paste aesthetic scaffolds per engine (includes BPMN no-styling warning)
- `style-guide.md` — 60-30-10 color system, typography rules
- `layout-control.md` — Narrow & Tall enforcement per engine
- `use-case-taxonomy.md` — diagram pattern catalogue (OOP, Gantt, Mind Map, BPMN, etc.)
- `diagram-selection.md` — decision tree for engine selection
- `interactive-support.md` — interactivity tier table per engine (`full`/`best-effort`/`limited`)
- `kroki-safe-subset.md` — syntax features confirmed safe across Kroki's renderer versions
- `output-placement.md` — output file naming rules and index rebuild trigger

### Examples

`docs/examples/` contains four working diagrams: `architecture-d2`, `erd-schema`, `flowchart-mermaid`, `sequence-plantuml`. Each folder holds a source file, `rendered.svg`, `interactive.html`, and `.diagram-meta.json` (dotfile — `META_FILENAME` constant in `build_diagram_index.py`).

## Key invariants

- `--interactive-output` only works with `--format svg` (the default).
- Index rebuild triggers only when the output file is named exactly `rendered.svg`. Naming it anything else (e.g. `diagram.svg`) silently skips indexing.
- The Kroki `%` character trap: do not strip `%` from source; the POST with `text/plain; charset=utf-8` already handles it.
- Mermaid node labels: use `<br/>` for line breaks, not `\n` — literal newlines corrupt SVG output.
- Mermaid YAML frontmatter (`---\ntitle:...\n---`) chokes older Kroki parsers. Use `%%{init:...}%%` blocks instead.
- C4-PlantUML self-hosted: use `!include <C4Container>` (local stdlib), not the raw GitHub URL — the GitHub URL fails on Kroki's default SECURE mode.
- Companion-server engines (Mermaid, BPMN, WaveDrom, Vega/Vega-Lite, Excalidraw, Diagrams.net) require separate Docker containers on self-hosted Kroki. On public `kroki.io` they work transparently.
- **Data Privacy & Public Gateway**: By default, rendering requests are transmitted to the public gateway `https://kroki.io`. Because diagram source text may contain sensitive architecture details, schema structures, or proprietary IP, you should configure a self-hosted Kroki server and set `--kroki-endpoint` when diagramming private, confidential, or sensitive systems.
- `_svg_annotators.py` engine dispatch: Graphviz/ERD use `annotate_graphviz_like()`; D2 uses `annotate_d2()` (base64-decoded class heuristic); Structurizr uses `annotate_plantuml_description()`; Mermaid uses `annotate_mermaid()`; PlantUML sequence uses `annotate_sequence()`; other PlantUML/C4 use `annotate_plantuml_description()`. All other engines fall through to `limited` tier — `build_interactive_html_file` prints a stderr warning.
- Interactive viewer keyboard shortcuts (non-obvious): `Space`+drag = pan; `+`/`-` = zoom; `0` = fit; `1` = 100%; arrow keys = pan by 60px.
- `build_diagram_index.py` infers engine from `source.*` file extension via `_SOURCE_SUFFIX_MAP` when `.diagram-meta.json` is absent (e.g., `.dsl` and `.structurizr` both map to `structurizr`).
- Version bump: edit `package.json` only. `_version.py` reads it at import time; do not hardcode version strings in the CLIs.
