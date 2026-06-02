# Kroki Editorial Diagrams

A premium, unified diagramming skill for **Claude Code** and **Antigravity IDE** (Gemini CLI).

It pairs **multi-engine diagrammatic DSLs** (PlantUML, C4, D2, Mermaid, Graphviz, ERD, BPMN) with **editorial design guidelines**, producing **interactive SVG viewers**, **dark-mode gallery indexes**, and **shareable Kroki URLs** — all from a single Python-backed skill.

Maintained by [Labinator.com](https://labinator.com).

---

## Key Features

1. **Editorial Theme Out-of-the-Box** — Warm paper `#f5f5f5`, ink `#2d3142`, slate `#4f5d75`, rust-accent `#eb6c36`. Geist Sans/Mono + Instrument Serif typography. Dark-mode support via `prefers-color-scheme`.
2. **Engine Independence** — Auto-selects D2, PlantUML, C4, Mermaid, Graphviz, ERD, or BPMN based on semantic use case. All engines are wired end-to-end.
3. **Interactive SVG Viewer** — Click-to-highlight node focus, animated edge flow, dimmed inactive elements, pan/zoom with keyboard shortcuts. Full interactivity on D2, PlantUML, C4-PlantUML, and Graphviz; best-effort on Mermaid and ERD; limited on BPMN.
4. **Automated Gallery Index** — Generates a `index.html` card-deck from all diagrams in a folder, with grid/list toggle and per-engine color coding.
5. **Narrow & Tall Layout Standard** — Max ~800px width, vertical flows enforced across all engines to prevent horizontal scrolling.
6. **Robust Error Handling** — `curl -f` detects HTTP 4xx/5xx from Kroki. 30-second timeout. Shareable Kroki URL printed on failure for manual debugging.
7. **Secure SVG Parsing** — Uses `defusedxml` to prevent XXE injection when wrapping SVG files in the interactive viewer.
8. **Test Suite** — 19 pytest tests covering engine registration, URL encoding, pluralization, SVG annotation, edge label parsing, sequence/Mermaid annotation, engine inference from source files, and HTML generation.

---

## Supported Engines

| Engine       | Best For                                  | SVG | PNG | PDF |
| ------------ | ----------------------------------------- | --- | --- | --- |
| `plantuml`   | Sequences, class diagrams, state machines | Yes | Yes | Yes |
| `c4plantuml` | C4 container/context architecture         | Yes | Yes | Yes |
| `d2`         | Modern system architecture, cloud layouts | Yes | —   | —   |
| `mermaid`    | Flowcharts, timelines, Git graphs         | Yes | Yes | Yes |
| `graphviz`   | Complex DAGs, dependency graphs           | Yes | Yes | Yes |
| `erd`        | Database entity-relationship diagrams     | Yes | Yes | —   |
| `bpmn`       | Business process / workflow compliance    | Yes | Yes | —   |

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
        │       └── test_scripts.py        # pytest suite (10 tests)
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
