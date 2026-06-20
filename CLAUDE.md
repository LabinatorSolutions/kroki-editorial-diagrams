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

### Python scripts (three cooperating modules)

**`render_kroki_diagram.py`** — the CLI. It reads the source file, POSTs to the Kroki API via `curl` (always `Content-Type: text/plain; charset=utf-8` to handle `%` characters safely), writes the rendered output, then calls the other two modules. Supports `--diagram-option key=value` (repeatable) to pass engine-specific Kroki options as `Kroki-Diagram-Options-*` headers, `--format jpg` (in addition to svg/png/pdf), and `--timeout` for slow self-hosted instances. Index auto-build fires only when the output filename is exactly `rendered.svg`; use `--skip-index` to suppress it.

**`build_interactive_kroki_html.py`** — wraps a rendered SVG in an HTML page with click-to-highlight node focus, animated directional edge flows, and pan/zoom. Annotates the raw SVG with `data-node-id`, `data-edge-source`, `data-edge-target` attributes. Uses `defusedxml` for XXE-safe SVG parsing. Interactive tier varies by engine: `full` (PlantUML, C4-PlantUML, Graphviz, D2), `best-effort` (Mermaid, ERD), `limited` (BPMN).

**`build_diagram_index.py`** — scans a root folder for subfolders containing `rendered.svg` + `.diagram-meta.json`, then generates a dark-mode gallery `index.html`. Metadata is written by the render script after each successful render.

### Reference docs

`skills/kroki-editorial-diagrams/references/` holds eight markdown files loaded by the skill during diagram generation:

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
- `build_interactive_kroki_html.py` engine dispatch: Graphviz/D2/ERD/Structurizr use `annotate_graphviz_like()`; Mermaid uses `annotate_mermaid()`; PlantUML sequence uses `annotate_sequence()`; other PlantUML/C4 uses `annotate_plantuml_description()`. All other engines fall through to `limited` tier (no node/edge annotation).
- Interactive viewer keyboard shortcuts (non-obvious): `Space`+drag = pan; `+`/`-` = zoom; `0` = fit; `1` = 100%; arrow keys = pan by 60px.
- `build_diagram_index.py` infers engine from `source.*` file extension via `_SOURCE_SUFFIX_MAP` when `.diagram-meta.json` is absent (e.g., `.dsl` and `.structurizr` both map to `structurizr`).
