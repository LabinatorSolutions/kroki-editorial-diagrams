# Contributing

## Setup

```bash
git clone https://github.com/LabinatorSolutions/kroki-editorial-diagrams.git
cd kroki-editorial-diagrams

# Install Python dependency
pacman -S python-defusedxml   # Arch / Manjaro
# or: pip install defusedxml

# Run tests to confirm baseline
python -m pytest skills/kroki-editorial-diagrams/scripts/tests/ -v
```

## What Lives Where

| Path | Purpose |
| ---- | ------- |
| `skills/kroki-editorial-diagrams/SKILL.md` | LLM instruction set — workflow, engine table, design rules, execution commands |
| `skills/kroki-editorial-diagrams/references/` | Reference docs loaded by the agent at runtime |
| `skills/kroki-editorial-diagrams/scripts/render_kroki_diagram.py` | Kroki API caller, URL builder, metadata writer |
| `skills/kroki-editorial-diagrams/scripts/build_interactive_kroki_html.py` | SVG annotator + interactive HTML wrapper |
| `skills/kroki-editorial-diagrams/scripts/build_diagram_index.py` | Gallery index generator |
| `skills/kroki-editorial-diagrams/scripts/tests/` | pytest suite |

## Adding a New Engine

1. Add the engine slug to `SUPPORTED_ENGINES` in `render_kroki_diagram.py`.
2. Add an annotator function in `build_interactive_kroki_html.py` (or route to an existing one if the SVG structure matches).
3. Add an `_engine_colors` entry in both `build_interactive_kroki_html.py` and `build_diagram_index.py`.
4. Document in: `engine-matrix.md`, `kroki-safe-subset.md`, `use-case-taxonomy.md`, `interactive-support.md`, and the engine table in `SKILL.md`.
5. Add a test in `tests/test_scripts.py`.
6. Add a style template in `engine-style-templates.md`.

## Changing Design Tokens

Edit `references/style-guide.md` first, then propagate to:
- Both HTML template generators (`build_interactive_kroki_html.py`, `build_diagram_index.py`) — both light and dark mode CSS blocks.
- Engine style templates in `references/engine-style-templates.md`.

## Pull Requests

Use the PR template checklist. Every PR must pass the test suite. Update `CHANGELOG.md`.
