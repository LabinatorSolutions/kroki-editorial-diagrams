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

# Render a diagram to SVG (default format) with interactive HTML overlay
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine d2 \
  --input docs/examples/architecture-d2/source.d2 \
  --output docs/examples/architecture-d2/rendered.svg \
  --interactive-output docs/examples/architecture-d2/interactive.html

# Render to PNG or PDF (--interactive-output unavailable for non-SVG)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine mermaid --format png --input path/to/source.mmd --output out.png

# Use a self-hosted Kroki instance
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine plantuml --input src.puml --output out.svg \
  --kroki-endpoint https://kroki.example.com

# Print shareable Kroki URL without rendering (offline / debug)
python3 skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py \
  --engine mermaid --input path/to/source.mmd --print-url-only
```

## Architecture

This repo is a Claude Code / Antigravity IDE (Gemini CLI) **skill** — an LLM instruction set backed by Python tooling that generates premium interactive diagram outputs.

### Entry point

`skills/kroki-editorial-diagrams/SKILL.md` is the LLM instruction set. It defines the 8-step workflow, engine selection logic, mandatory design rules (Narrow & Tall layout, 60-30-10 color system), and execution commands. The skill is installed as a symlink in `~/.claude/skills/` and `~/.gemini/config/skills/`.

### Python scripts (three cooperating modules)

**`render_kroki_diagram.py`** — the CLI. It reads the source file, POSTs to the Kroki API via `curl` (always `Content-Type: text/plain; charset=utf-8` to handle `%` characters safely), writes the rendered output, then calls the other two modules. Index auto-build fires only when the output filename is exactly `rendered.svg`; use `--skip-index` to suppress it.

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

`docs/examples/` contains four working diagrams: `architecture-d2`, `erd-schema`, `flowchart-mermaid`, `sequence-plantuml`. Each folder holds a source file, `rendered.svg`, `interactive.html`, and `_diagram_meta.json`.

## Key invariants

- `--interactive-output` only works with `--format svg` (the default).
- Index rebuild triggers only when the output file is named exactly `rendered.svg`. Naming it anything else (e.g. `diagram.svg`) silently skips indexing.
- The Kroki `%` character trap: do not strip `%` from source; the POST with `text/plain; charset=utf-8` already handles it.
- Mermaid node labels: use `<br/>` for line breaks, not `\n` — literal newlines corrupt SVG output.
