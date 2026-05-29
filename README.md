# Kroki Editorial Diagrams

A premium, unified diagramming skill designed for **Claude Code** (and similar agentic workflows).

It combines **auto-layout multi-engine diagrammatic DSLs** (PlantUML, C4, D2, Mermaid, Graphviz, ERD) with the **aesthetic styling guidelines** of high-end editorial design, featuring **interactive SVG wrappers** and **automated gallery indexing**.

## Key Features

1. **Editorial Theme Out-of-the-Box**: Uses a gorgeous warm-editorial color system (paper background `#f5f5f5`, ink `#2d3142`, slate muted `#4f5d75`, rust-accent `#eb6c36`) with Geist Sans/Mono typography.
2. **Brand-Matching Onboarding**: Includes guidelines to scan any target website, extract its colors/typography, and compile a brand-matching custom stylesheet.
3. **Engine Independence**: Automatically chooses the ideal engine (D2, PlantUML, Mermaid, Graphviz, ERD) based on your semantic use case (flows, state-machines, system architecture, database schemas).
4. **Auto-Layout with Layout Discipline**: Standardizes on a strict **Narrow & Tall** standard (max ~800px width, vertical flows) to ensure charts fit perfectly on standard viewports without horizontal scrolling.
5. **Interactive Exploration**: Builds an `interactive.html` wrapper adding click-to-highlight node focus, edge flow animations, and dimmed out inactive elements.
6. **Automated Directory Cataloging**: Generates a unified `index.html` gallery card deck listing all diagrams generated inside the folder.
7. **Robust Error Handling**: Integrates a complete gotcha checklist for Kroki API URL-decoding traps, Mermaid version discrepancies, and Vega-Lite SVG layer issues.

## Folder Structure

```text
kroki-editorial-diagrams/
├── README.md
├── LICENSE
├── package.json
└── skills/
    └── kroki-editorial-diagrams/
        ├── SKILL.md                 # Main LLM instruction set
        ├── scripts/                 # Core Python runner and wrappers
        │   ├── render_kroki_diagram.py
        │   ├── build_interactive_kroki_html.py
        │   └── build_diagram_index.py
        └── references/              # Detailed style rules and taxonomy
            ├── style-guide.md
            ├── engine-style-templates.md
            ├── use-case-taxonomy.md
            ├── diagram-selection.md
            ├── engine-matrix.md
            ├── interactive-support.md
            ├── kroki-safe-subset.md
            ├── layout-control.md
            └── output-placement.md
```

## How to Install

### 1. Clone the Repository

Clone the repository to a local directory of your choice:

```bash
git clone https://github.com/LabinatorSolutions/kroki-editorial-diagrams.git
cd kroki-editorial-diagrams
```

### 2. Install to Google Antigravity IDE

To install this skill in **Google Antigravity IDE**, create a symlink from this repository's skill folder directly to your Antigravity IDE configuration directory:

```bash
# Create the config skills directory if it doesn't exist
mkdir -p ~/.gemini/config/skills

# Symlink the skill folder
ln -s "$(pwd)/skills/kroki-editorial-diagrams" ~/.gemini/config/skills/kroki-editorial-diagrams
```

### 3. Install to Claude Code

To install in **Claude Code**, symlink the skill folder to the Claude configuration directory:

```bash
# Create the claude skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Symlink the skill folder
ln -s "$(pwd)/skills/kroki-editorial-diagrams" ~/.claude/skills/kroki-editorial-diagrams
```

---

## How to Update

Since you install via **symbolic links** pointing to your local git clone, updating the skill is trivial and automatic:

1. Navigate back to your cloned repository folder:

    ```bash
    cd /path/to/cloned/kroki-editorial-diagrams
    ```

2. Pull the latest upstream updates:

    ```bash
    git pull origin main
    ```

Your IDE (Antigravity or Claude Code) will instantly pick up the updated skill instructions, templates, and Python render scripts without needing re-installation or IDE restarts.

---

## License & Credits

Author: **LabinatorSolutions** (GitHub: [LabinatorSolutions](https://github.com/LabinatorSolutions))

Licensed under the GNU General Public License v3.0 (GPLv3). See [LICENSE](LICENSE) for details.
