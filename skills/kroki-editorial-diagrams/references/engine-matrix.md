# Engine Matrix Reference

Understand the core trade-offs of the rendering engines bundled in this skill.

---

## 1. Engine Trade-offs

### Core Editorial Engines (full styling + interactive support)

| Engine | Ideal Scenario | Drawback | Styling | Companion Server |
| --- | --- | --- | --- | --- |
| **D2** | Container architectures, cloud layouts, nested boundaries. | Newer DSL syntax; limited specialized UML features. | **High** — clean natural styling; supports `theme`, `layout`, `sketch` options. | No |
| **PlantUML** | Complex sequence flows, API messaging, UML-specific OOP/class/state layouts. | Slightly dated defaults if styled poorly. | **High** — fully configurable via `<style>` blocks and `skinparam`. | No |
| **C4-PlantUML** | C4 model container/context/component/code diagrams. | Remote `!include` fails on self-hosted SECURE mode; use `!include <C4Container>` instead. | **High** — `UpdateElementStyle` / `UpdateRelStyle`. | No |
| **Structurizr** | C4 architecture via native Structurizr DSL; strong alternative to C4-PlantUML. | Less widely known DSL. | **High** — `styles {}` block in workspace. | No |
| **Mermaid** | Quick flowcharts, timelines, Git branch graphs, pie charts. | Older Kroki-bundled versions have fragile YAML frontmatter parsing. | **Medium** — `%%{init:...}%%` theme variables. | Yes |
| **Graphviz** | Highly complex directed acyclic graphs, module imports, dependency graphs, network topologies. | Fragile auto-routing; easily looks cluttered without careful node grouping. | **Medium** — `graph`, `node`, `edge` attribute blocks. | No |
| **ERD** | Database entity tables, relational schema mapping. | Weak layout control; text-only styling configurations. | **Low** — raw DSL attribute styling only. | No |
| **BPMN** | Business process notation with swimlanes, events, gateways; compliance and handoff docs. | Fixed renderer; no custom styling API through Kroki. | **None** | Yes |

### Extended Engines (built-in to Kroki gateway)

| Engine | Ideal Scenario | Drawback | Styling | Companion Server |
| --- | --- | --- | --- | --- |
| **Nomnoml** | Lightweight UML sketches, concept maps, quick class/component diagrams. | Limited interactivity (pan/zoom only); fewer layout options than PlantUML. | **Medium** — `#` directive headers control stroke, fill, font. | No |
| **Ditaa** | ASCII art → clean SVG; diagrams embedded in README or code comments. | Fixed color output; no styling API. | **None** | No |
| **SvgBob** | Rich ASCII art → crisp SVG; cleaner output than Ditaa. | Fixed color output; no styling API. | **None** | No |
| **GoAT** | Go ASCII Text diagrams; ideal for network flows embedded inline in Markdown. | Fixed color output; no styling API. | **None** | No |
| **Pikchr** | Minimalist line-art diagrams in PIC dialect; compact syntax. | Niche; little community tooling. | **Low** — inline style attributes. | No |
| **Bytefield** | Binary/byte protocol field diagrams (packet headers, register layouts). | Specialist use only. | **Low** | No |
| **WireViz** | Wiring harnesses, cable connector pinout documentation. | YAML input; specialist use. | **Low** | No |
| **BlockDiag family** (`actdiag`, `blockdiag`, `seqdiag`, `nwdiag`, `packetdiag`, `rackdiag`) | Quick activity, block, network, packet, or rack unit diagrams. | Limited styling; dated default visuals. | **Low** | No |
| **Symbolator** | HDL component interface symbols for hardware documentation. | Highly specialist; no general diagramming use. | **Low** | No |
| **UMLet** | UMLet XML-format diagrams (legacy UMLet tool output). | Requires UMLet XML source; no DSL. | **Low** | No |

### Companion-Server Engines (require separate Docker container in self-hosted Kroki)

| Engine | Ideal Scenario | Drawback | Styling | Companion Server |
| --- | --- | --- | --- | --- |
| **WaveDrom** | Digital timing diagrams, clock signals, bus waveforms, hardware protocol timing. | JSON DSL; fixed color scheme (no palette override). | **None** | Yes (`kroki-mermaid` bundle) |
| **Vega** | Complex data visualizations with full Vega grammar. | Heavy JSON spec; steep learning curve for non-data teams. | **High** — full `config` block supports editorial palette. | Yes |
| **Vega-Lite** | Data-driven bar/line/scatter/heat-map charts with concise JSON grammar. | Less expressive than full Vega for complex multi-layer specs. | **High** — `config` block supports editorial palette. | Yes |
| **Excalidraw** | Hand-drawn wireframes, rough architecture sketches, whiteboard-style diagrams. | Hand-drawn aesthetic is fixed; no styling API. | **None** | Yes |
| **Diagrams.net** | Import and render diagrams.net (draw.io) XML files. | Experimental in Kroki; output quality varies. | **None** | Yes |
