# Output Placement Reference

Maintain clean repository structures by saving diagrams in standard paths.

---

## 1. Directory Layout

Diagram assets must be stored in isolated component folders. Never scatter raw `.svg` files randomly in the repository root.

### Standard Storage Hierarchy
1.  **With `docs/` folder**: If a `docs/` folder exists, save to `docs/diagrams/<slug>/`.
2.  **No `docs/` folder**: Save to `diagrams/<slug>/` in the repository root.

Each individual diagram gets its own folder:
```text
diagrams/<slug>/
├── source.<ext>        # Original source DSL file (.puml, .mmd, .d2, .dot)
├── rendered.svg        # Renders directly in markdown files
├── rendered.png        # Best fallback for standard previews
└── interactive.html    # Full interactive HTML canvas
```

The parent path (`diagrams/` or `docs/diagrams/`) will also automatically contain a unified `index.html` page to list and search all generated diagrams.

---

## 2. File Naming Conventions (Slug rules)
Convert diagram names to standard kebab-case filenames:
*   Convert all characters to lowercase.
*   Replace spaces or underscores with hyphens.
*   Remove special punctuation.
*   Keep filenames under **30 characters**.
*   *Example*: "AWS user login flow" → `aws-login-flow`
