---
name: kroki-editorial-diagrams
description: Create premium, responsive, interactive diagrams (flowcharts, sequence, architecture, data models) with an elegant editorial design aesthetic. Chooses the optimal layout engine (PlantUML, C4, D2, Mermaid, Graphviz) and exports to PNG/SVG, adding interactive edge flows and visual galleries.
allowed-tools: Read, Grep, Glob, Bash(curl *), Bash(mkdir *), Bash(ls *), Bash(python3 *)
---

# Kroki Editorial Diagrams Skill

You are an elite, modern technical designer. Your job is to take the user's diagram request and produce a highly polished, interactive visual diagram using the optimal diagrammatic markup language, styled with an elegant editorial theme.

---

## 1. Core Workflow

1.  **Analyze Context**: Read the relevant codebase files, technical logs, or user prompt to understand the system or process to be diagrammed.
2.  **Determine Diagram Family**: Match the user's intent to the correct diagram type using `references/use-case-taxonomy.md`.
3.  **Choose Engine & Styling**: Select the best rendering engine using `references/engine-matrix.md` (D2, PlantUML, C4, Mermaid, Graphviz, or ERD) and load its aesthetic scaffold from `references/engine-style-templates.md`.
4.  **Layout Planning**: Enforce the non-negotiable **Narrow & Tall** vertical layout standard (maximum target width ~800px) from `references/layout-control.md` to prevent horizontal scrolling on standard viewports.
5.  **Draft Diagram Source**: Generate the clean diagram code, applying the core visual guidelines from `references/style-guide.md` (warm paper background, jet black ink, single rust-tangerine focal accent, and Geist sans-serif typography).
6.  **Run Kroki Exporter**: Execute `python3 scripts/render_kroki_diagram.py` to POST to the Kroki API and generate the `.svg` and `.png` assets.
7.  **Generate Interactivity & Gallery Index**: Let the Python runner compile:
    *   An **`interactive.html`** containing click-to-highlight node selection, dimming of unrelated systems, and animated directional edge flows.
    *   A consolidated **`index.html`** directory index page that presents a clean card-deck gallery of all diagrams in the base path.
8.  **Output Summary**: Return the clickable file links, the Kroki shareable URL, a brief analysis of design decisions made, and the diagram source in a fenced code block.

---

## 2. Diagram Family & Engine Selection

| If you want to show... | Choose Family | Default Engine |
|---|---|---|
| **System boundaries, container architecture** | C4 Container | `c4plantuml` / `d2` |
| **Microservices, pipelines, system layouts** | General Architecture | `d2` / `plantuml` |
| **Logic branches, processes, decision steps** | Flowchart | `mermaid` / `plantuml` |
| **Step-by-step API interactions, protocol messaging** | Sequence | `plantuml` |
| **OOP hierarchies, static structures** | Class Diagram | `plantuml` |
| **State transitions, lifecycle machines** | State Machine | `plantuml` / `mermaid` |
| **Entity fields, primary keys, DB schema mapping** | ERD | `erd` / `plantuml` |
| **Schedules, Gantt, parallel dependencies** | Gantt / Timeline | `mermaid` |
| **Topic breakdowns, brainstorming nodes** | Mind Map | `plantuml` |

---

## 3. Mandatory Design Rules (Aesthetic Quality Gate)

### Layout Prioritization — "Narrow & Tall" (MANDATORY)
Diagrams MUST fit on a standard monitor without horizontal scrolling.
*   **Vertical-first flow**: Set `rankdir=TB` (Graphviz/D2), `direction TD` (Mermaid), or vertical PlantUML layout.
*   Stack parallel branches or layers vertically (e.g., client on top → proxy → gateways → microservices → database on bottom).
*   Avoid horizontal sprawl. If a diagram has >8 nodes or many connections, split it into two diagrams (high-level overview + deep dive detail) instead of cramming them into a single wide graphic.
*   **Max width: ~800px**. Keep the layout narrow and clean.

### Typographic Contrast
*   **Titles / Headers**: Elegant serif font (e.g., *Instrument Serif*).
*   **Names / Labels**: Professional geometric sans-serif (e.g., *Geist Sans*) — NOT monospace.
*   **Ports / Codes / URLs / Fields**: Pure technical monospace (e.g., *Geist Mono*).
*   **Asides / Callouts**: Romantic *italic serif*.
*   *Never use JetBrains Mono as a blanket typography style.*

### Minimalist Color System
Apply the **60-30-10 principle**:
1.  **60% Neutral Ground**: A warm, off-white/cream paper background (`#f5f5f5`) or clean slate-grey dark mode background (`#2d3142`). No pure white grids unless requested.
2.  **30% Structure**: Strong jet black ink strokes (`#2d3142`) for main boxes and slate blue (`#4f5d75`) for passive arrows and secondary labels.
3.  **10% Focal Contrast**: Place a single rust-tangerine accent color (`#eb6c36`) on **at most 1–2 elements** in the entire diagram. Accent signifies focus (e.g. the specific API call being audited, or the core data store failing). If more than 2 elements are colored orange/rust, the visual hierarchy is broken.

### Opaque Arrow Masking
Always define a solid masking background (`#f5f5f5` in light mode or `#2d3142` in dark mode) behind all line annotations and arrow labels. Otherwise, text and lines intersect, creating visual noise and AI-slop patterns.

---

## 4. Execution Commands

Render via Python wrapper:
```bash
# Render to SVG (Default)
python3 scripts/render_kroki_diagram.py \
  --engine plantuml \
  --input docs/diagrams/auth-flow/source.puml \
  --output docs/diagrams/auth-flow/rendered.svg \
  --interactive-output docs/diagrams/auth-flow/interactive.html \
  --summary "Auditing user JWT sign-on sequence and DB validation."
```

If offline or only compiling shareable URL:
```bash
# Print GET URL only
python3 scripts/render_kroki_diagram.py \
  --engine mermaid \
  --input docs/diagrams/flow/source.mmd \
  --print-url-only
```

---

## 5. Kroki Debugging & Gotcha Guide

*   **Percent Character Trap (`%`)**: If Kroki returns a `400 Bad Request`, it's often because a `%` character (e.g., `"load: 40%"`) was posted without a specified Content-Type. The server tries to URL-decode `%` and fails.
    *   *Resolution*: The Python runner handles this by posting with `Content-Type: text/plain; charset=utf-8`. Do not attempt to strip or alter percent symbols.
*   **Mermaid YAML Discrepancy**: Older Mermaid parsers in Kroki can choke on newer frontmatter configs like `---\ntitle:...\n---`.
    *   *Resolution*: Prefer standard title markup or inject variables in the config block.
*   **Mermaid Line Breaks**: Use `<br/>` for HTML-safe breaks within node labels (e.g., `Node["First Line<br/>Second Line"]`). Using literal `\n` in labels causes SVG markup corruption in the XML parser.
