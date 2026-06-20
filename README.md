# Kroki Editorial Diagrams

A premium, unified diagramming skill for **Claude Code** and **Antigravity IDE** (Gemini CLI).

It pairs **multi-engine diagrammatic DSLs** (PlantUML, C4, D2, Mermaid, Graphviz, ERD, BPMN) with **editorial design guidelines**, producing **interactive SVG viewers**, **dark-mode gallery indexes**, and **shareable Kroki URLs** — all from a single Python-backed skill.

Maintained by [Labinator.com](https://labinator.com).

---

## Key Features

1. **Editorial Theme Out-of-the-Box** — Warm paper `#f5f5f5`, ink `#2d3142`, slate `#4f5d75`, rust-accent `#eb6c36`. Geist Sans/Mono + Instrument Serif typography. Dark-mode support via `prefers-color-scheme`.
2. **Engine Independence** — Auto-selects D2, PlantUML, C4, Structurizr, Mermaid, Graphviz, ERD, BPMN, WaveDrom, Vega-Lite, Nomnoml, Ditaa, SvgBob, Excalidraw, and more based on semantic use case. All engines are wired end-to-end.
3. **Diagram Options** — Pass engine-specific Kroki options via `--diagram-option key=value` (e.g. D2 theme, layout, sketch mode; PlantUML theme).
4. **Interactive SVG Viewer** — Click-to-highlight node focus, animated edge flow, dimmed inactive elements, pan/zoom with keyboard shortcuts. Full interactivity on D2, PlantUML, C4-PlantUML, Graphviz, and Structurizr; best-effort on Mermaid and ERD; limited/pan-zoom on all others.
5. **Automated Gallery Index** — Generates a `index.html` card-deck from all diagrams in a folder, with grid/list toggle and per-engine color coding.
6. **Narrow & Tall Layout Standard** — Max ~800px width, vertical flows enforced across all engines to prevent horizontal scrolling.
7. **Robust Error Handling** — Detects HTTP 4xx/5xx from Kroki via `urllib.error.HTTPError`. Configurable timeout (`--timeout`). Shareable Kroki URL printed on failure for manual debugging.
8. **Secure SVG Parsing** — Uses `defusedxml` to prevent XXE injection when wrapping SVG files in the interactive viewer.
9. **Test Suite** — 36 pytest tests covering engine registration, URL encoding, pluralization, SVG annotation, edge label parsing, sequence/Mermaid/ERD/BPMN annotation, engine inference from source files, diagram options curl headers, background rect removal, and HTML generation.

---

## Supported Engines

### Core Editorial Engines (full styling + interactive support)

| Engine | Best For | SVG | PNG | PDF | JPG | Companion Server |
| --- | --- | --- | --- | --- | --- | --- |
| `plantuml` | Sequences, class diagrams, state machines | Yes | Yes | Yes | — | — |
| `c4plantuml` | C4 container/context architecture | Yes | Yes | Yes | — | — |
| `structurizr` | C4 via native DSL (no stdlib include) | Yes | Yes | — | — | — |
| `d2` | Modern system architecture, cloud layouts | Yes | Yes | — | — | — |
| `mermaid` | Flowcharts, timelines, Git graphs | Yes | Yes | Yes | — | Yes |
| `graphviz` | Complex DAGs, dependency graphs | Yes | Yes | Yes | — | — |
| `erd` | Database entity-relationship diagrams | Yes | Yes | — | — | — |
| `bpmn` | Business process / workflow compliance | Yes | Yes | — | — | Yes |

### Extended Engines

| Engine | Best For | SVG | PNG | Companion Server |
| --- | --- | --- | --- | --- |
| `nomnoml` | Lightweight UML sketches, concept maps | Yes | — | — |
| `wavedrom` | Digital timing / waveform diagrams | Yes | Yes | Yes |
| `vegalite` | Data-driven charts (concise grammar) | Yes | Yes | Yes |
| `vega` | Complex data visualizations | Yes | Yes | Yes |
| `ditaa` | ASCII art → clean SVG | Yes | Yes | — |
| `svgbob` | Rich ASCII art → crisp SVG | Yes | — | — |
| `goat` | ASCII art for inline Markdown | Yes | — | — |
| `excalidraw` | Hand-drawn wireframes and sketches | Yes | Yes | Yes |
| `pikchr` | Minimalist line-art diagrams | Yes | — | — |
| `bytefield` | Binary/byte protocol packet fields | Yes | — | — |
| `wireviz` | Wiring harnesses, cable connectors | Yes | Yes | — |
| `blockdiag` / `actdiag` / `seqdiag` / `nwdiag` | Quick block, activity, network diagrams | Yes | Yes | — |

> **Companion server**: On the public `kroki.io` instance, companion-server engines work transparently. For self-hosted Kroki, run the matching Docker image alongside the gateway (`yuzutech/kroki-mermaid`, `yuzutech/kroki-bpmn`, etc.).
>
> [!WARNING]
> **Data Privacy Warning**: By default, rendering requests are transmitted to the public gateway `https://kroki.io`. Because diagram source text may contain sensitive architecture details, schema information, or proprietary IP, you should deploy a self-hosted Kroki server and set `--kroki-endpoint` when diagramming private, confidential, or sensitive systems.

---

## Folder Structure

```text
kroki-editorial-diagrams/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── package.json
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/
│   └── examples/                          # Sample rendered diagrams
│       ├── architecture-d2/               # D2 system architecture example
│       ├── erd-schema/                    # ERD database schema example
│       ├── flowchart-mermaid/             # Mermaid flowchart example
│       └── sequence-plantuml/             # PlantUML sequence diagram example
└── skills/
    └── kroki-editorial-diagrams/
        ├── SKILL.md                       # Main LLM instruction set
        ├── scripts/
        │   ├── render_kroki_diagram.py    # Kroki API caller, SVG/PNG renderer
        │   ├── build_interactive_kroki_html.py  # Interactive HTML wrapper
        │   ├── build_diagram_index.py     # Gallery index generator
        │   ├── requirements.txt           # Python dependencies (defusedxml)
        │   └── tests/
        │       └── test_scripts.py        # pytest suite (36 tests)
        └── references/
            ├── style-guide.md
            ├── engine-matrix.md
            ├── engine-style-templates.md
            ├── use-case-taxonomy.md
            ├── diagram-selection.md
            ├── interactive-support.md
            ├── kroki-safe-subset.md
            ├── layout-control.md
            └── output-placement.md
```

---

## How to Install

### 1. Clone to a stable location

```bash
mkdir -p ~/.repos
git clone https://github.com/LabinatorSolutions/kroki-editorial-diagrams.git ~/.repos/kroki-editorial-diagrams
```

### 2. Install the Python dependency

```bash
# Arch / Manjaro
pacman -S python-defusedxml

# Other distros / macOS
pip install defusedxml
```

### 3. Symlink — Claude Code

```bash
mkdir -p ~/.claude/skills
ln -sf ~/.repos/kroki-editorial-diagrams/skills/kroki-editorial-diagrams \
       ~/.claude/skills/kroki-editorial-diagrams
```

### 4. Symlink — Antigravity IDE (Gemini CLI)

```bash
mkdir -p ~/.gemini/config/skills
ln -sf ~/.repos/kroki-editorial-diagrams/skills/kroki-editorial-diagrams \
       ~/.gemini/config/skills/kroki-editorial-diagrams
```

### 5. Wire into your auto-update script *(optional but recommended)*

If you use a `claude-update-all.sh` script (or similar), add a git-pull block for this repo so it stays current automatically.

Add after your plugin updates, before any bunx section:

```bash
# Community skills (git-tracked repos)
log "--- community skill updates ---"
git -C "$HOME/.repos/kroki-editorial-diagrams" pull --ff-only 2>&1 | tee -a "$LOG" \
  || log "WARN: kroki-editorial-diagrams update failed"
```

Because both IDEs resolve the skill through symlinks pointing into `~/.repos/kroki-editorial-diagrams/`, a `git pull` there is instantly visible to both IDEs — no restart or re-symlink needed.

---

## How It Auto-Updates

```text
git pull (in ~/.repos/kroki-editorial-diagrams)
    │
    └─► skills/kroki-editorial-diagrams/ updated
            │
            ├─► ~/.claude/skills/kroki-editorial-diagrams  (symlink → live)
            └─► ~/.gemini/config/skills/kroki-editorial-diagrams  (symlink → live)
```

Both IDEs pick up changes on the next conversation — no reinstall, no restart.

---

## Running the Tests

```bash
cd ~/.repos/kroki-editorial-diagrams/skills/kroki-editorial-diagrams/scripts
python -m pytest tests/ -v
```

---

## Usage

The skill is invoked automatically in Claude Code and Antigravity IDE whenever you ask for a diagram. Example prompts:

- *"Draw the authentication flow for this service"*
- *"Create a C4 container diagram for our microservices"*
- *"Generate an ERD for the users and orders tables"*
- *"Map the CI/CD pipeline as a flowchart"*

The skill reads the codebase context, selects the right engine, drafts the DSL, renders via Kroki, and returns an `interactive.html`, `rendered.svg`, and shareable URL.

---

## License & Credits

Author: **LabinatorSolutions** — [Labinator.com](https://labinator.com) · [GitHub](https://github.com/LabinatorSolutions)

Licensed under the GNU General Public License v3.0 (GPLv3). See [LICENSE](LICENSE) for details.
