# Use-Case Taxonomy Reference

Identify your diagramming intent and map it to the recommended engine family.

---

## 1. Intent Mapping Directory

### System Structure & Containers

* **Intent**: Map microservices, databases, borders, APIs, and cloud services.
* **Ideal Family**: C4 Container / General Architecture.
* **Preferred Engine**: `structurizr` (native C4 DSL, no stdlib dependency), `d2`, or `c4plantuml`.
* **Note**: Prefer `structurizr` on self-hosted Kroki to avoid the remote `!include` problem. Use `d2` for container-style nested layouts; `c4plantuml` when PlantUML's UML precision is needed.

### Process & Logic Flow

* **Intent**: Map algorithmic pipelines, logical decision branches, user onboarding flows, or continuous integration steps.
* **Ideal Family**: Flowchart.
* **Preferred Engine**: `mermaid` (clean simple lines) or `plantuml` (custom shapes).

### Message Passing Over Time

* **Intent**: Show sequence of service calls, timing triggers, API round-trips, or client-server authentication handshakes.
* **Ideal Family**: Sequence Diagram.
* **Preferred Engine**: `plantuml` (deep timing and activation lifelines).

### Database Schemas

* **Intent**: Map relational keys, columns, foreign connections, and table attributes.
* **Ideal Family**: ERD.
* **Preferred Engine**: `erd` (clean structural output) or `plantuml` (database class shapes).

### Lifecycle Machine States

* **Intent**: Show logical transition states of an entity (e.g. Order created → Pending → Dispatched → Shipped).
* **Ideal Family**: State Diagram.
* **Preferred Engine**: `plantuml` or `mermaid`.

### OOP Hierarchy & Class Structure

* **Intent**: Represent object-oriented class hierarchies, inheritance chains, interfaces, and static relationships.
* **Ideal Family**: Class Diagram.
* **Preferred Engine**: `plantuml`.

### Gantt & Timeline

* **Intent**: Display schedules, milestones, parallel task tracks, or feature delivery timelines.
* **Ideal Family**: Gantt / Timeline.
* **Preferred Engine**: `mermaid`.

### Mind Map & Topic Breakdown

* **Intent**: Explore concept hierarchies, brainstorming branches, or document feature taxonomies.
* **Ideal Family**: Mind Map.
* **Preferred Engine**: `plantuml`.

### Business Process & Workflow Compliance

* **Intent**: Model formal business processes with swimlanes, BPMN events, gateways, and tasks for compliance or handoff documentation.
* **Ideal Family**: BPMN.
* **Preferred Engine**: `bpmn`.
* **Note**: BPMN output cannot be styled via this skill's design tokens. Use only when the audience requires standard BPMN notation; prefer `mermaid` flowcharts or `plantuml` activity diagrams for internal process documentation. Requires companion server on self-hosted Kroki.

### Network Topology & Infrastructure

* **Intent**: Map physical or logical network layouts, including nodes, subnets, firewalls, load balancers, and service connections.
* **Ideal Family**: General Architecture.
* **Preferred Engine**: `graphviz` or `d2`.
* **Note**: Use `graphviz` for highly connected directed graphs (DAGs) where auto-routing matters; prefer `d2` for cleaner container-style layouts with nested boundaries.

### Digital Timing & Waveform

* **Intent**: Show clock signals, bus waveforms, digital protocol timing (I²C, SPI, UART), setup/hold constraints, or hardware handshake sequences.
* **Ideal Family**: Timing Diagram.
* **Preferred Engine**: `wavedrom`.
* **Note**: WaveDrom uses a JSON DSL. No custom color palette is available through Kroki — focus on clear signal grouping and labelling. Requires companion server on self-hosted Kroki.

### Data Visualization & Charts

* **Intent**: Display data-driven bar charts, line plots, scatter plots, heat maps, or statistical summaries from structured data.
* **Ideal Family**: Data Visualization.
* **Preferred Engine**: `vegalite` (concise JSON grammar) or `vega` (full Vega grammar for complex specs).
* **Note**: Vega/Vega-Lite supports the editorial color palette via the `config` block. Use when the diagram is driven by actual data values rather than hand-coded topology. Requires companion server on self-hosted Kroki.

### ASCII Art & Plain-Text Diagrams

* **Intent**: Create diagrams that must be readable as plain text — embedded in README files, code comments, or terminals.
* **Ideal Family**: ASCII Art / Text Diagrams.
* **Preferred Engine**: `ditaa` (box-and-arrow ASCII → clean SVG), `svgbob` (richer ASCII shapes → crisp SVG), or `goat` (Go ASCII Text, optimised for inline Markdown).
* **Note**: No styling API is available for these engines. Output color is fixed. Prefer these only when source readability as text is the primary constraint.

### Sketch / Whiteboard Wireframe

* **Intent**: Produce rough hand-drawn wireframes, early-stage architecture sketches, or whiteboard-style diagrams for presentations or design reviews.
* **Ideal Family**: Sketch / Whiteboard.
* **Preferred Engine**: `excalidraw`.
* **Note**: Excalidraw output uses a fixed hand-drawn renderer — no editorial color tokens apply. Use for ideation and early design review, not for polished production documentation. Requires companion server on self-hosted Kroki.

### Lightweight UML / Concept Map

* **Intent**: Quickly sketch simple UML class structures, concept relationships, or component dependencies without the verbosity of full PlantUML.
* **Ideal Family**: Lightweight UML.
* **Preferred Engine**: `nomnoml`.
* **Note**: Nomnoml supports styling via `#` directive headers (stroke, fill, font). Interactivity is limited — pan/zoom only.

### Hardware / Protocol / Signal Diagrams

* **Intent**: Illustrate HDL component interfaces (ports, signals), binary protocol packet formats, or rack unit layouts for hardware documentation.
* **Ideal Family**: Hardware / Protocol.
* **Preferred Engine**: `symbolator` (HDL component symbols), `bytefield` (bit/byte protocol fields), `packetdiag` (packet diagrams), or `rackdiag` (server rack layouts).

### Wiring & Cable Harness

* **Intent**: Document physical wiring harnesses, connector pinouts, and cable routing for electronics or automotive harness design.
* **Ideal Family**: Wiring / Hardware.
* **Preferred Engine**: `wireviz`.
