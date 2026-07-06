# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- `.gitignore` no longer strips the committed showcase artifacts under
  `docs/examples/` (`rendered.svg`, `interactive.html`, `.diagram-meta.json`,
  `index.html`), so the gallery renders on a fresh clone.

### Changed

- Version is now single-source: `package.json` is canonical and the three CLIs
  read it through `scripts/_version.py` (resolves the skill symlink). Bumping
  the version means editing `package.json` only — no more four hardcoded copies.
- Documentation corrected: the `.diagram-meta.json` schema in `CLAUDE.md` now
  reflects the keys the render script actually writes, and stale "curl"
  references were updated to "HTTP" (the pipeline uses `urllib`, not curl).

## [1.1.0] - 2026-06-22

### Added

- CI workflow (`.github/workflows/test.yml`) running the pytest suite on push
  and pull request.
- Expanded Kroki engine coverage: Structurizr, Ditaa, Nomnoml, SvgBob, Pikchr,
  Goat, Bytefield, WaveDrom, WireViz, Vega/Vega-Lite, Excalidraw, Diagrams.net,
  and the *diag family, alongside the core editorial engines.
- `--diagram-option key=value` (repeatable) to pass engine-specific Kroki
  options as `Kroki-Diagram-Options-*` headers.
- `--format jpg` and configurable `--timeout` for slow self-hosted instances.
- Comprehensive unit tests for the SVG annotators; limited-tier interactive
  diagrams now emit a stderr warning.
- Engine inference from `source.*` extension when `.diagram-meta.json` is absent.

### Changed

- SVG processing split into private modules `_svg_utils.py` (namespace/util
  helpers) and `_svg_annotators.py` (per-engine annotation) for testability.
- Gallery index build now fires only when the output file is exactly
  `rendered.svg`; recursive viewBox lookup improves background-rect detection.

### Fixed

- Robust error handling for missing input files and corrupted metadata.
- Kroki endpoint URLs sanitized (trailing slash stripped); hidden directories
  excluded from index generation.
- Guarded `svg.getBBox` calls in the interactive viewer to survive hidden
  elements; click events suppressed during drag.

## [1.0.0] - 2026-05-29

### Added

- Initial Kroki editorial diagram skill: PlantUML, C4-PlantUML, D2, Mermaid,
  Graphviz, ERD, and BPMN support.
- Interactive SVG viewer with click-to-highlight node focus, animated
  directional edge flows, and pan/zoom.
- Dark-mode gallery index generator.
- Editorial design system (Narrow & Tall layout, 60-30-10 color) and reference
  documentation set.
- XXE-safe SVG parsing via `defusedxml`; data-privacy warning for the public
  `kroki.io` gateway.

[Unreleased]: https://github.com/LabinatorSolutions/kroki-editorial-diagrams/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/LabinatorSolutions/kroki-editorial-diagrams/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/LabinatorSolutions/kroki-editorial-diagrams/releases/tag/v1.0.0
