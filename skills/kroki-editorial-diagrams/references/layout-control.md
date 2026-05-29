# Layout Control Reference

How to ensure your diagrams stay clean, perfectly balanced, and highly readable under updates.

---

## 1. The "Narrow & Tall" Standard

Standard computer monitors and mobile displays fit taller layouts much better than very wide horizontal layouts. Wide diagrams force horizontal scrolling, causing the reader to lose spatial orientation.

### Vertical Flow Directives

Force engines to route from Top to Bottom:

* **Mermaid**: Use `flowchart TD` (Top-Down) or `flowchart TB`.
* **PlantUML / C4**: Use default vertical layout. Avoid `left to right direction` for complex architectures.
* **Graphviz (DOT)**: Ensure `rankdir=TB` is defined in the base graph block.
* **D2**: Define `direction: down` at the top of the file.

### Layer Placement

Structure your system layers logically from top-to-bottom:

1. **Actor / User / Client Tier** (Top layer)
2. **Edge / CDN / DNS proxy**
3. **API Gateway / Auth Gateway**
4. **Microservices / Application Controllers**
5. **Databases / In-Memory Caches / File Stores** (Bottom layer)

---

## 2. Spacing Grid (4px Non-negotiable)

When writing D2 or raw styles:

* Ensure every box width, padding, border-radius, and connection gap value is a multiple of **4** (e.g. padding: 8px, box height: 60px, gap: 32px).
* Avoid arbitrary pixel measurements. Symmetry is what makes diagrams feel premium.
