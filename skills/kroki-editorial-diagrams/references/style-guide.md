# Style Guide

This style guide defines the colors, typography, spacing, and stroke tokens that make our diagrams look premium, clean, and professional. All engines must map their internal configurations to these semantic roles.

---

## 1. Aesthetic Design System

### Semantic Roles

We use an opinionated, minimalist warm-editorial color skin. Colors must be mapped by semantic role to avoid arbitrary color choices.

| Role          | Purpose                              | Hex Value (Light Mode)      | Hex Value (Dark Mode)       |
|---------------|--------------------------------------|-----------------------------|-----------------------------|
| `paper`       | Canvas/page background               | `#f5f5f5` (warm light-grey) | `#2d3142` (slate-black)     |
| `paper-2`     | Container backgrounds                | `#ececec`                   | `#393e53`                   |
| `ink`         | Primary headers, key frames          | `#2d3142` (slate-black)     | `#f5f5f5` (warm light-grey) |
| `muted`       | Connective arrows, minor text        | `#4f5d75` (slate-blue)      | `#bfc0c0` (silver)          |
| `soft`        | Sublabels, boundary outlines         | `#7a8399`                   | `#8e98ac`                   |
| `rule`        | Thin hairline structural dividers    | `rgba(45,49,66,0.12)`       | `rgba(245,245,245,0.12)`    |
| `accent`      | Focal point (MAX 1-2 per chart)      | `#eb6c36` (rust-tangerine)  | `#f08a59`                   |
| `accent-tint` | Background highlight fill            | `rgba(235,108,54,0.08)`     | `rgba(240,138,89,0.10)`     |
| `link`        | HTTP requests, external dependencies | `#2e5aa8` (link-blue)       | `#6a95d8`                   |

---

## 2. Typography

| Role          | Font Family                      | Size / Weight      | Usage                                       |
|---------------|----------------------------------|--------------------|---------------------------------------------|
| `title`       | Instrument Serif, Georgia, serif | 1.6rem / 400       | Page / Diagram H1 Title                     |
| `node-name`   | Geist, Helvetica, sans-serif     | 12px / 600         | Human-readable system names                 |
| `sublabel`    | Geist Mono, Monaco, monospace    | 9px / 400          | Technical specs (ports, protocols, schemas) |
| `arrow-label` | Geist Mono, Monaco, monospace    | 8px / 400, tracked | Connecting line annotation labels           |

---

## 3. Spacing, Stroke & Grid

All coordinates, gaps, and dimensions must align to a strict **4px grid** to preserve high visual symmetry.

* `stroke-thin`: `0.8px` (tag outlines)
* `stroke-default`: `1.0px` (standard system borders)
* `stroke-strong`: `1.2px` (focal elements)
* `radius-sm`: `4px` (type tags)
* `radius-md`: `6px` (main component boxes)
* `radius-lg`: `8px` (container zones)
* `grid`: `4px` (every coordinate, padding, and gap spacing must be divisible by 4)
