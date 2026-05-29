# Kroki Safe Subset Reference

To prevent rendering errors, standardise on the tested Kroki engine versions and format properties defined here.

---

## 1. Engine & Output Formats

| Engine       | SVG Output | PNG Output | PDF Output | Best Theme Option       |
|--------------|------------|------------|------------|-------------------------|
| `plantuml`   | **Yes**    | **Yes**    | **Yes**    | Skinparam block         |
| `c4plantuml` | **Yes**    | **Yes**    | **Yes**    | UpdateElementStyle      |
| `d2`         | **Yes**    | No         | No         | Classes block           |
| `mermaid`    | **Yes**    | **Yes**    | **Yes**    | %%{init:...}%% header   |
| `graphviz`   | **Yes**    | **Yes**    | **Yes**    | Graph [ bgcolor="..." ] |
| `erd`        | **Yes**    | **Yes**    | No         | Raw DSL styling         |
| `bpmn`       | **Yes**    | **Yes**    | No         | None (fixed renderer)   |
