# Diagram Selection Guide

When deciding how to visually represent information, follow these technical principles to select the best type of diagram.

---

## 1. Selection Rules of Thumb

1. **Prefer auto-layout engines**: Do not calculate manual coordinate points (`x`, `y`). Let engines like `d2` and `plantuml` calculate positioning so diagrams remain readable under code updates.
2. **Avoid crowded diagrams**: Keep elements within a strict complexity budget (≤9 nodes, ≤12 connections).
3. **Vary widths for summary layout**: When rendering supplementary context text, use 2-3 column grids with varying card widths rather than identical grids.
4. **Use serif titles and sans-serif node text**: Enforces structural design boundaries.
5. **Always place annotation labels on arrows**: Never use disconnected text nodes to describe arrow routes.
6. **Check companion server availability for self-hosted Kroki**: Mermaid, BPMN, WaveDrom, Vega/Vega-Lite, Excalidraw, and Diagrams.net require separate companion Docker containers. If you are generating diagrams for a self-hosted environment that only runs the gateway container, choose an engine that is built-in (D2, PlantUML, Graphviz, Structurizr, ERD, Nomnoml, Ditaa, etc.).
7. **Match styling capability to output purpose**: Engines with `None` styling (BPMN, Excalidraw, ASCII art) produce fixed visuals — use them only when the notation itself (not the aesthetic) is the deliverable.

---

## 2. Structurizr vs C4-PlantUML

Both engines produce C4 model diagrams. Choose based on environment:

* **Prefer `structurizr`** when running self-hosted Kroki in SECURE mode (default) — no remote `!include` needed, stdlib is built-in.
* **Prefer `c4plantuml`** when you need tight PlantUML ecosystem integration, PlantUML-specific `skinparam` customisation, or the full PlantUML UML feature set alongside C4.
* Both engines produce `Full` interactivity tier output.

---

## 3. Vega-Lite vs Mermaid for Data-Driven Diagrams

* **Use `vegalite`** when the diagram is driven by actual data values (JSON arrays, aggregations, statistical transforms). Vega-Lite's `config` block supports the full editorial color palette.
* **Use `mermaid`** for hand-coded timelines, Gantt charts, or Git graphs where the structure is authored directly rather than derived from data.
* **Companion server note**: Both require companion containers in self-hosted Kroki. On public `kroki.io` both work transparently.

---

## 4. ASCII Art Engine Selection (Ditaa / SvgBob / GoAT)

All three produce SVG from ASCII art source. Differences:

* **`ditaa`**: Widest adoption; recognises box-drawing characters and arrow connectors in a natural ASCII style. Good for block diagrams.
* **`svgbob`**: Produces cleaner, crisper SVG with smoother curves. Better for technical illustrations.
* **`goat`**: Optimised for embedding directly inside Go source files or Markdown documents; minimal setup.

None of these engines support custom styling. If aesthetics matter, prefer `graphviz` or `d2`.

---

## 5. When to Use Specialist Engines

* **`wavedrom`**: Use exclusively for digital timing/clock diagrams. Do not use as a general-purpose flowchart engine.
* **`bytefield`**: Use for documenting binary protocol wire formats (TCP headers, Ethernet frames, custom packet layouts).
* **`symbolator`**: Use for hardware HDL component documentation. Not for software architecture.
* **`wireviz`**: Use for physical wiring harness and connector pinout documentation.
* **`excalidraw`**: Use for rough early-stage wireframes and whiteboard sketches. Replace with a styled engine (D2, PlantUML) before including in production documentation.
