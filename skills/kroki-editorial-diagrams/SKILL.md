---
name: kroki-editorial-diagrams
description: Create premium, responsive, interactive diagrams (flowcharts, sequence, architecture, data models, timing, data visualization) with an elegant editorial design aesthetic. Chooses the optimal layout engine (PlantUML, C4, D2, Mermaid, Graphviz, Structurizr, WaveDrom, Vega-Lite, ERD, BPMN, and more) and exports to PNG/SVG, adding interactive edge flows and visual galleries.
allowed-tools: Read, Write, Grep, Glob, Bash(cat *), Bash(mkdir *), Bash(ls *), Bash(python3 *)
---

# Kroki Editorial Diagrams Skill

You are an elite, modern technical designer. Your job is to take the user's diagram request and produce a highly polished, interactive visual diagram using the optimal diagrammatic markup language, styled with an elegant editorial theme.

---

## 1. Core Workflow

1. **Analyze Context**: Read the relevant codebase files, technical logs, or user prompt to understand the system or process to be diagrammed.
2. **Determine Diagram Family**: Match the user's intent to the correct diagram type using `references/use-case-taxonomy.md`.
3. **Choose Engine & Styling**: Select the best rendering engine using `references/engine-matrix.md` (D2, PlantUML, C4, Mermaid, Graphviz, ERD, Structurizr, WaveDrom, Vega-Lite, or others) and load its aesthetic scaffold from `references/engine-style-templates.md`.
4. **Layout Planning**: Enforce the non-negotiable **Narrow & Tall** vertical layout standard (maximum target width ~800px) from `references/layout-control.md` to prevent horizontal scrolling on standard viewports.
5. **Draft Diagram Source**: Generate the clean diagram code, applying the core visual guidelines from `references/style-guide.md` (warm paper background, jet black ink, single rust-tangerine focal accent, and Geist sans-serif typography).
6. **Run Kroki Exporter**: Execute `python3 scripts/render_kroki_diagram.py` to POST to the Kroki API and generate the `.svg` asset (default). PNG is generated with a second call using `--format png --skip-index`; see execution commands below.
7. **Generate Interactivity & Gallery Index**: Optionally pass `--interactive-output <path>.html` to generate a click-to-highlight interactive overlay with animated directional edge flows. This is opt-in — omitting the flag skips HTML generation. The gallery `index.html` auto-rebuilds only when the output file is named exactly `rendered.svg`; any other name silently skips indexing.
8. **Output Summary**: Return the clickable file links, a brief analysis of design decisions made, and the diagram source in a fenced code block. To obtain a shareable Kroki URL, run a second call with `--print-url-only` (no network call, no render).

---

## 2. Diagram Family & Engine Selection

| If you want to show… | Choose Family | Default Engine | Notes |
| --- | --- | --- | --- |
| **System boundaries, container architecture** | C4 Container | `structurizr` / `c4plantuml` / `d2` | `structurizr` needs no stdlib include |
| **Microservices, pipelines, system layouts** | General Architecture | `d2` / `plantuml` | |
| **Formal business processes with swimlanes** | BPMN | `bpmn` | No styling; companion server |
| **Logic branches, processes, decision steps** | Flowchart | `mermaid` / `plantuml` | |
| **Step-by-step API interactions, protocol messaging** | Sequence | `plantuml` | |
| **OOP hierarchies, static structures** | Class Diagram | `plantuml` | |
| **State transitions, lifecycle machines** | State Machine | `plantuml` / `mermaid` | |
| **Entity fields, primary keys, DB schema mapping** | ERD | `erd` / `plantuml` | |
| **Schedules, Gantt, parallel dependencies** | Gantt / Timeline | `mermaid` | |
| **Network topology, infrastructure, subnets** | Network Topology | `graphviz` / `d2` | |
| **Topic breakdowns, brainstorming nodes** | Mind Map | `plantuml` | |
| **Digital timing, clock signals, bus waveforms** | Timing Diagram | `wavedrom` | Companion server |
| **Data charts, bar/line/scatter plots** | Data Visualization | `vegalite` / `vega` | Companion server |
| **ASCII art, plaintext, README-embedded diagrams** | ASCII Art | `ditaa` / `svgbob` / `goat` | No styling API |
| **Hand-drawn wireframes, rough architecture sketches** | Sketch / Whiteboard | `excalidraw` | No styling; companion server |
| **Lightweight UML, concept maps, quick class sketches** | Lightweight UML | `nomnoml` | |
| **Hardware signals, HDL components, protocol packet formats** | Hardware / Protocol | `symbolator` / `bytefield` / `packetdiag` | Specialist use |
| **Wiring harnesses, cable connector diagrams** | Wiring / Hardware | `wireviz` | |

---

## 3. Mandatory Design Rules (Aesthetic Quality Gate)

### Layout Prioritization — "Narrow & Tall" (MANDATORY)

Diagrams MUST fit on a standard monitor without horizontal scrolling.

* **Vertical-first flow**: Set `rankdir=TB` (Graphviz/D2), `direction TD` (Mermaid), or vertical PlantUML layout.
* Stack parallel branches or layers vertically (e.g., client on top → proxy → gateways → microservices → database on bottom).
* Avoid horizontal sprawl. If a diagram has >8 nodes or many connections, split it into two diagrams (high-level overview + deep dive detail) instead of cramming them into a single wide graphic.
* **Max width: ~800px**. Keep the layout narrow and clean.

### Typographic Contrast

* **Titles / Headers**: Elegant serif font (e.g., *Instrument Serif*).
* **Names / Labels**: Professional geometric sans-serif (e.g., *Geist Sans*) — NOT monospace.
* **Ports / Codes / URLs / Fields**: Pure technical monospace (e.g., *Geist Mono*).
* **Asides / Callouts**: Romantic *italic serif*.
* *Never use JetBrains Mono as a blanket typography style.*

### Minimalist Color System

Apply the **60-30-10 principle**:

1. **60% Neutral Ground**: A warm, off-white/cream paper background (`#f5f5f5`) or clean slate-grey dark mode background (`#2d3142`). No pure white grids unless requested.
2. **30% Structure**: Strong jet black ink strokes (`#2d3142`) for main boxes and slate blue (`#4f5d75`) for passive arrows and secondary labels.
3. **10% Focal Contrast**: Place a single rust-tangerine accent color (`#eb6c36`) on **at most 1–2 elements** in the entire diagram. Accent signifies focus (e.g. the specific API call being audited, or the core data store failing). If more than 2 elements are colored orange/rust, the visual hierarchy is broken.

### Opaque Arrow Masking

Always define a solid masking background (`#f5f5f5` in light mode or `#2d3142` in dark mode) behind all line annotations and arrow labels. Otherwise, text and lines intersect, creating visual noise and AI-slop patterns.

---

## 4. Execution Commands

Render via Python wrapper:

```bash
# Render D2 architecture to SVG (default)
python3 scripts/render_kroki_diagram.py \
  --engine d2 \
  --input docs/diagrams/system-arch/source.d2 \
  --output docs/diagrams/system-arch/rendered.svg \
  --interactive-output docs/diagrams/system-arch/interactive.html \
  --interactive-title "System Architecture Overview" \
  --summary "Container layout for production microservices."

# Render PlantUML sequence to SVG
python3 scripts/render_kroki_diagram.py \
  --engine plantuml \
  --input docs/diagrams/auth-flow/source.puml \
  --output docs/diagrams/auth-flow/rendered.svg \
  --interactive-output docs/diagrams/auth-flow/interactive.html \
  --summary "Auditing user JWT sign-on sequence and DB validation."

# Pass diagram options (D2 theme + layout; PlantUML theme; etc.)
python3 scripts/render_kroki_diagram.py \
  --engine d2 \
  --input docs/diagrams/system-arch/source.d2 \
  --output docs/diagrams/system-arch/rendered.svg \
  --diagram-option theme=earth-tones \
  --diagram-option layout=elk

# Render with a self-hosted Kroki instance; increase timeout for slow servers
python3 scripts/render_kroki_diagram.py \
  --engine plantuml \
  --input docs/diagrams/auth-flow/source.puml \
  --output docs/diagrams/auth-flow/rendered.svg \
  --kroki-endpoint https://kroki.internal.example.com \
  --timeout 60
```

Second-pass PNG/JPG after SVG (use `--skip-index` to avoid redundant gallery rebuild):

```bash
# PNG after SVG — skip the index rebuild since SVG pass already ran it
python3 scripts/render_kroki_diagram.py \
  --engine d2 --format png --skip-index \
  --input docs/diagrams/system-arch/source.d2 \
  --output docs/diagrams/system-arch/rendered.png
# JPG is also supported: --format jpg
```

Shareable URL only (no network call, no render):

```bash
# Print GET URL only (offline / debug)
python3 scripts/render_kroki_diagram.py \
  --engine mermaid \
  --input docs/diagrams/flow/source.mmd \
  --print-url-only
```

> **Output naming invariant**: `--output` MUST end with `rendered.svg` for the gallery index to auto-rebuild. Any other filename silently skips indexing. Use `--skip-index` when rendering non-SVG formats to suppress the (already-run) index rebuild.

---

## 5. Kroki Debugging & Gotcha Guide

* **Self-hosted Kroki**: Use `--kroki-endpoint` to point at an internal instance (e.g., `https://kroki.internal.example.com`). Default is `https://kroki.io`. Use `--timeout 60` if the server is slow.
* **Data Privacy Warning**: By default, rendering requests are transmitted to the public gateway `https://kroki.io`. Because diagram source text may contain sensitive architecture details, schema structures, or proprietary IP, you should deploy a self-hosted Kroki server and set `--kroki-endpoint` when diagramming private, confidential, or sensitive systems.
* **Companion server engines** (Mermaid, BPMN, WaveDrom, Vega/Vega-Lite, Excalidraw, Diagrams.net): On public `kroki.io` these work transparently. On a self-hosted Kroki gateway, they require separate Docker companion containers (`yuzutech/kroki-mermaid`, `yuzutech/kroki-bpmn`, etc.) running alongside the gateway, with `KROKI_*_HOST` env vars configured. Sending a companion engine request to a gateway-only instance returns a 404 or 503 — not a diagram error.
* **Diagram options** (`--diagram-option key=value`): Pass engine-specific rendering options. Examples — D2: `theme=earth-tones`, `layout=elk`, `sketch=`; PlantUML: `theme=minty`, `no-metadata=`. Options are sent as `Kroki-Diagram-Options-*` HTTP headers. Full option catalogue in `references/kroki-safe-subset.md`.
* **C4 stdlib include on self-hosted**: Use `!include <C4Container>` (local stdlib), not the raw GitHub URL. The GitHub URL fails on self-hosted Kroki running in default `SECURE` mode. See `references/engine-style-templates.md` Section 3.
* **Percent Character Trap (`%`)**: If Kroki returns a `400 Bad Request`, it's often because a `%` character (e.g., `"load: 40%"`) was posted without a specified Content-Type. The server tries to URL-decode `%` and fails.
  * *Resolution*: The Python runner handles this by posting with `Content-Type: text/plain; charset=utf-8`. Do not strip or alter percent symbols.
* **Mermaid YAML Discrepancy**: Older Mermaid parsers in Kroki can choke on newer frontmatter configs like `---\ntitle:...\n---`.
  * *Resolution*: Use the `%%{init:...}%%` block instead of YAML frontmatter.
* **Mermaid Line Breaks**: Use `<br/>` for HTML-safe breaks within node labels (e.g., `Node["First Line<br/>Second Line"]`). Literal `\n` corrupts SVG XML output.
