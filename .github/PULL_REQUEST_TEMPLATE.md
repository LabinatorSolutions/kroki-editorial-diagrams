## Summary

Describe what this PR changes and why.

## Checklist

- [ ] Tests pass: `python -m pytest skills/kroki-editorial-diagrams/scripts/tests/ -v`
- [ ] If a new engine was added: entry in `engine-matrix.md`, `kroki-safe-subset.md`, `use-case-taxonomy.md`, `interactive-support.md`, and `SKILL.md` engine table
- [ ] If a design token changed: `style-guide.md` updated and both HTML templates (`build_interactive_kroki_html.py`, `build_diagram_index.py`) reflect the change
- [ ] `CHANGELOG.md` updated under `[Unreleased]` or a new version section
- [ ] No generated artifacts committed (`.svg`, `.png`, `.pdf`, `rendered/`, `index.html`, `interactive.html`)
