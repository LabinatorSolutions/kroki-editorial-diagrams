# Engine Matrix Reference

Understand the core trade-offs of the rendering engines bundled in this skill.

---

## 1. Engine Trade-offs

| Engine       | Ideal Scenario                                                         | Drawback                                                 | Styling Support                                                       |
|--------------|------------------------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------------------------|
| **D2**       | Container architectures, cloud layouts, nested boundaries.             | Newer DSL syntax, limited specialized UML features.      | **High** (very clean natural styling out of the box).                 |
| **PlantUML** | Complex sequence flows, timed API messaging, UML-specific OOP layouts. | Slightly dated default graphics if styled poorly.        | **High** (fully configurable via stylesheet blocks).                  |
| **Mermaid**  | Quick flowcharts, timelines, Git branches.                             | Older versions have fragile parsing of YAML tags.        | **Medium** (styled via base variables in init block).                 |
| **Graphviz** | Highly complex directed acyclic graphs (DAGs), module imports, network topologies. | Fragile auto-routing algorithms; easily looks cluttered. | **Medium** (configured in graph blocks).                              |
| **ERD**      | Database entity tables.                                                | Weaker layout styles; text-only configurations.          | **Low** (best suited for quick schematic outlines).                   |
| **BPMN**     | Business process / workflow notation (swimlanes, events, gateways).    | Niche DSL; no custom styling API exposed by Kroki.       | **None** (output is fixed; use for process compliance diagrams only). |
