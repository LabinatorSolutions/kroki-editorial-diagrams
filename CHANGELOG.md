# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-05-29

### Fixed

- **Critical**: `d2` engine was missing from `SUPPORTED_ENGINES` — any call using `--engine d2` was rejected by argparse despite D2 being the top recommended engine throughout the documentation.
- **Critical**: Pluralization bug in gallery index — `{{"s" if n_entries != 1 else ""}}` was never evaluated as a Python expression inside the f-string; the raw Python literal was rendered as HTML text. Fixed by extracting `plural_s` variable before the f-string.
- **Critical**: No HTTP error detection for non-SVG formats — `curl` exits 0 on HTTP 4xx/5xx; Kroki error responses were silently written as garbage bytes to PNG/PDF output files. Added `curl -f` flag.
- **Critical**: `allowed-tools` in `SKILL.md` was missing `Write` — agents following the workflow couldn't create diagram source files before rendering.
- **Security**: SVG parsing in `build_interactive_kroki_html.py` used Python's stdlib `xml.etree.ElementTree.fromstring`, which is vulnerable to XXE injection. Switched to `defusedxml.ElementTree.fromstring`. Added `defusedxml>=0.7.1` to `scripts/requirements.txt`.
- **D2 interactivity**: `interactive-support.md` claimed D2 had "Full" interactivity tier but no D2 annotator existed in the code. Implemented `annotate_d2()` (D2 SVG uses the same `class="node"` / `class="edge"` conventions as Graphviz).
- Dead `selectedNodeId = nodeId` assignment before `resetState()` in interactive viewer JS removed.
- Exception handling in `build_interactive_kroki_html.py` CLI broadened to catch `ValueError`, `KeyError`, `UnicodeDecodeError` in addition to `ET.ParseError`.

### Added

- **BPMN engine**: Added `bpmn` to all reference documentation (`engine-matrix.md`, `kroki-safe-subset.md`, `use-case-taxonomy.md`, `interactive-support.md`) and to the engine selection table in `SKILL.md`. Was in `SUPPORTED_ENGINES` code but completely undocumented.
- **Dark mode**: Added `@media (prefers-color-scheme: dark)` CSS blocks to both HTML templates (`build_interactive_kroki_html.py` and `build_diagram_index.py`) using the full dark palette from `style-guide.md`.
- **`d2` in `_engine_colors`**: Added slate-blue color entry for D2 in both HTML generators. Previously fell back to tangerine accent.
- **curl `--max-time 30`**: Prevents indefinite hangs on slow or unreachable Kroki instances.
- **pytest suite**: `scripts/tests/test_scripts.py` — 10 tests covering engine registration, Kroki URL roundtrip, pluralization (singular + plural), index file generation, SVG annotation (Graphviz, D2, unknown engine), and interactive HTML output.
- **`scripts/requirements.txt`** with `defusedxml>=0.7.1`.
- **GitHub repository files**: `CHANGELOG.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, `.github/PULL_REQUEST_TEMPLATE.md`.

### Changed

- `SKILL.md` step 6 clarified: default output is SVG only; PNG requires a separate `--format png --skip-index` call.
- `engine-style-templates.md` D2 template: fixed `*.style.font` → `*.style.font-color` (correct D2 syntax).
- `engine-style-templates.md` PlantUML: added version note — the `<style>` block requires PlantUML ≥ 1.2020.x (Kroki ≥ 0.19); skinparam fallback documented.
- `_engine_colors` tuples in `build_diagram_index.py` simplified from 3-element to 2-element (third element was unused `"Full"` label).
- `interactive-support.md` ERD tier updated from "Static/Limited" to "Best Effort" (Graphviz-style parsing is attempted).
- `.gitignore` updated: added `.pytest_cache/`.
- README fully rewritten to reflect current engine support, install pattern with auto-update integration, and test instructions.

---

## [1.0.0] — 2026-05-28

### Added

- Initial release.
- Skill definition (`SKILL.md`) with 8-step workflow, engine selection table, mandatory design rules, execution commands, and Kroki gotcha guide.
- Python scripts: `render_kroki_diagram.py`, `build_interactive_kroki_html.py`, `build_diagram_index.py`.
- Reference documentation: `style-guide.md`, `engine-matrix.md`, `engine-style-templates.md`, `use-case-taxonomy.md`, `diagram-selection.md`, `interactive-support.md`, `kroki-safe-subset.md`, `layout-control.md`, `output-placement.md`.
- Supported engines: `plantuml`, `c4plantuml`, `mermaid`, `graphviz`, `bpmn`, `erd`.
- Interactive viewer with pan, zoom, click-to-highlight, and animated edge flows.
- Gallery index generator with grid/list toggle and per-engine color coding.
