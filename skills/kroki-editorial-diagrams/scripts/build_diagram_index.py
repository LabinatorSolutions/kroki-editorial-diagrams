#!/usr/bin/env python3
import argparse
import html
import json
import pathlib


META_FILENAME = ".diagram-meta.json"


def prettify_name(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


_SOURCE_SUFFIX_MAP: dict[str, str] = {
    ".puml": "plantuml",
    ".mmd": "mermaid",
    ".dot": "graphviz",
    ".erd": "erd",
    ".d2": "d2",
    ".bpmn": "bpmn",
}


def infer_engine_from_source(artifact_dir: pathlib.Path) -> str:
    for source in artifact_dir.glob("source.*"):
        engine = _SOURCE_SUFFIX_MAP.get(source.suffix.lower())
        if engine:
            return engine
    return "diagram"


def load_artifact_entry(artifact_dir: pathlib.Path) -> dict[str, str] | None:
    rendered_svg = artifact_dir / "rendered.svg"
    if not rendered_svg.exists():
        return None

    meta_path = artifact_dir / META_FILENAME
    meta: dict[str, str] = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    title = meta.get("title") or prettify_name(artifact_dir.name)
    engine = meta.get("engine") or infer_engine_from_source(artifact_dir)
    tier = meta.get("interactive_tier") or ("full" if (artifact_dir / "interactive.html").exists() else "static")
    summary = meta.get("summary") or f"Rendered with {engine}."

    return {
        "folder": artifact_dir.name,
        "title": title,
        "engine": engine,
        "tier": tier,
        "summary": summary,
        "interactive_href": f"./{artifact_dir.name}/interactive.html",
        "interactive_exists": str((artifact_dir / 'interactive.html').exists()).lower(),
        "svg_href": f"./{artifact_dir.name}/rendered.svg",
    }


def build_index_html(entries: list[dict[str, str]], title: str) -> str:
    # Editorial coloring based on design tokens
    _engine_colors: dict[str, tuple[str, str]] = {
        "plantuml":   ("235, 108, 54",  "#eb6c36"),
        "c4plantuml": ("46, 90, 168",   "#2e5aa8"),
        "d2":         ("79, 93, 117",   "#4f5d75"),
        "graphviz":   ("79, 93, 117",   "#4f5d75"),
        "mermaid":    ("122, 131, 153", "#7a8399"),
        "erd":        ("191, 192, 192", "#bfc0c0"),
        "bpmn":       ("100, 120, 140", "#64788c"),
    }
    _default_color = ("235, 108, 54", "#eb6c36")

    cards = []
    for entry in entries:
        title_html   = html.escape(entry["title"])
        summary_html = html.escape(entry["summary"])
        engine_html  = html.escape(entry["engine"])
        tier         = entry["tier"]

        tool_rgb, tool_hex = _engine_colors.get(entry["engine"], _default_color)

        interactive_href = html.escape(entry["interactive_href"]) if entry["interactive_exists"] == "true" else ""
        svg_href         = html.escape(entry["svg_href"])
        primary_href     = interactive_href or svg_href

        if tier == "full":
            badge = '<span class="pill badge-full">Interactive</span>'
        elif tier == "best-effort":
            badge = '<span class="pill badge-best">Interactive (limited)</span>'
        else:
            badge = '<span class="pill badge-best">Static SVG</span>'

        svg_link = f'<a class="link-muted" href="{svg_href}" target="_blank" rel="noopener noreferrer">SVG</a>'

        cards.append(f"""      <article class="card" style="--tool-rgb:{tool_rgb};border-left-color:{tool_hex};">
        <a class="card-link" href="{primary_href}" target="_blank" rel="noopener noreferrer" aria-label="Open {title_html}"></a>
        <div class="card-preview">
          <img src="{svg_href}" alt="{title_html} diagram preview" loading="lazy">
        </div>
        <div class="card-content">
          <div class="card-header">
            <h2 class="card-title">{title_html}</h2>
            <span class="pill pill-tool"><span class="pill-dot"></span>{engine_html}</span>
          </div>
          <p class="card-body">{summary_html}</p>
          <div class="card-grid-meta">
            {badge}
            <span class="spacer"></span>
            {svg_link}
          </div>
          <div class="card-list-meta">
            {badge}
            {svg_link}
          </div>
        </div>
      </article>""")

    cards_html = "\n".join(cards)
    page_title = html.escape(title)
    n_entries  = len(entries)
    plural_s   = "s" if n_entries != 1 else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --paper: #f5f5f5;
      --paper-2: #ececec;
      --ink: #2d3142;
      --muted: #4f5d75;
      --soft: #7a8399;
      --rule: rgba(45, 49, 66, 0.12);
      --accent: #eb6c36;
      --accent-tint: rgba(235, 108, 54, 0.08);
      --link: #2e5aa8;
    }}

    body {{
      font-family: 'Geist', 'Inter', system-ui, sans-serif;
      background: var(--paper);
      color: var(--ink);
      min-height: 100vh;
      overflow-x: hidden;
    }}

    a {{ color: inherit; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* ── Background ──────────────────────────────────────────── */
    .bg-layer {{ position: fixed; inset: 0; z-index: 0; pointer-events: none; }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(235, 108, 54, 0.06), transparent),
        linear-gradient(180deg, var(--paper-2) 0%, var(--paper) 100%);
    }}
    .bg-dots {{
      position: absolute; inset: 0;
      background-image: radial-gradient(rgba(45,49,66,0.035) 1px, transparent 1px);
      background-size: 24px 24px;
      mask-image: radial-gradient(ellipse 100% 60% at 50% 0%, black 10%, transparent 80%);
      -webkit-mask-image: radial-gradient(ellipse 100% 60% at 50% 0%, black 10%, transparent 80%);
    }}

    /* ── Nav ─────────────────────────────────────────────────── */
    nav {{
      position: sticky; top: 0; z-index: 50;
      border-bottom: 1px solid var(--rule);
      background: rgba(245, 245, 245, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }}
    .nav-inner {{
      max-width: 1280px; margin: 0 auto; padding: 0 24px;
      height: 60px; display: flex; align-items: center; gap: 12px;
    }}
    .nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
    .nav-icon {{
      width: 32px; height: 32px; border-radius: 6px;
      background: linear-gradient(135deg, var(--accent), var(--link));
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 0 16px rgba(235, 108, 54, 0.15); flex-shrink: 0;
    }}
    .nav-icon svg {{ width: 18px; height: 18px; fill: none; stroke: white; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .nav-wordmark {{ font-family: 'Instrument Serif', serif; font-size: 1.4rem; color: var(--ink); }}
    .nav-wordmark span {{ color: var(--muted); font-family: 'Geist', sans-serif; font-size: 0.9rem; margin-left: 4px; }}

    /* ── Main ────────────────────────────────────────────────── */
    main {{ position: relative; z-index: 10; max-width: 1280px; margin: 0 auto; padding: 64px 24px 96px; }}

    /* ── Hero ────────────────────────────────────────────────── */
    .hero {{ max-width: 680px; margin-bottom: 72px; animation: fade-up 0.6s ease both; }}
    .hero h1 {{
      font-family: 'Instrument Serif', serif;
      font-size: clamp(2.8rem, 6vw, 4rem);
      font-weight: 400; letter-spacing: -0.02em; line-height: 1.08;
      color: var(--ink);
      margin-bottom: 16px;
    }}
    .hero p {{ font-size: 1.05rem; font-weight: 300; color: var(--muted); line-height: 1.65; max-width: 560px; }}

    /* ── Toolbar ─────────────────────────────────────────────── */
    .toolbar {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 16px; margin-bottom: 24px; padding: 10px 16px;
      background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--rule); border-radius: 10px;
      box-shadow: inset 0 1px 1px rgba(255,255,255,0.4);
      animation: fade-up 0.6s 0.1s ease both;
    }}
    .toolbar-count {{ font-family: 'Geist Mono', monospace; font-size: 0.8rem; color: var(--muted); }}

    /* ── View toggle ─────────────────────────────────────────── */
    .view-toggle {{
      position: relative; display: inline-flex;
      background: var(--paper-2); border: 1px solid var(--rule);
      border-radius: 8px; padding: 4px;
    }}
    .toggle-indicator {{
      position: absolute; inset: 4px; width: calc(50% - 4px);
      background: #ffffff; border-radius: 6px;
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      pointer-events: none;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }}
    .toggle-btn {{
      position: relative; z-index: 1;
      display: flex; align-items: center; gap: 6px;
      padding: 6px 14px; border: none; background: transparent;
      border-radius: 6px; font-family: 'Geist', sans-serif; font-size: 0.82rem;
      font-weight: 500; cursor: pointer; transition: color 0.2s ease;
      color: var(--muted); white-space: nowrap;
    }}
    .toggle-btn.active {{ color: var(--ink); }}
    .toggle-btn svg {{
      width: 14px; height: 14px; stroke: currentColor; fill: none;
      stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0;
    }}

    /* ── Gallery grid ────────────────────────────────────────── */
    .gallery {{ animation: fade-up 0.6s 0.2s ease both; }}
    .gallery.view-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }}
    .gallery.view-grid .card {{ flex-direction: column; border-left: 1px solid var(--rule) !important; }}
    .gallery.view-grid .card-preview {{ width: 100%; height: 210px; border-bottom: 1px solid var(--rule); border-radius: 0; flex-shrink: unset; margin: 0; }}
    .gallery.view-grid .card-list-meta {{ display: none; }}

    /* ── Gallery list ────────────────────────────────────────── */
    .gallery.view-list {{ display: flex; flex-direction: column; gap: 10px; }}
    .gallery.view-list .card {{ flex-direction: row; align-items: center; min-height: 80px; padding: 10px 16px 10px 10px; border-left-width: 4px !important; }}
    .gallery.view-list .card-preview {{ width: 96px; height: 60px; border-radius: 6px; border: 1px solid var(--rule); flex-shrink: 0; margin-right: 16px; }}
    .gallery.view-list .card-preview img {{ object-fit: contain; padding: 6px; }}
    .gallery.view-list .card-body {{ display: none; }}
    .gallery.view-list .card-grid-meta {{ display: none; }}
    .gallery.view-list .card-list-meta {{ display: flex; align-items: center; gap: 12px; margin-left: auto; flex-shrink: 0; }}

    /* ── Card base ───────────────────────────────────────────── */
    .card {{
      display: flex;
      background: #ffffff;
      border: 1px solid var(--rule); border-radius: 12px;
      overflow: hidden; cursor: pointer; position: relative;
      transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
      box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }}
    .card-link {{ position: absolute; inset: 0; z-index: 0; border-radius: inherit; }}
    .link-muted {{ position: relative; z-index: 1; }}

    .gallery.view-grid .card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 16px 32px -10px rgba(var(--tool-rgb), 0.12), 0 0 0 1px rgba(var(--tool-rgb), 0.25);
    }}
    .gallery.view-list .card:hover {{ transform: translateX(4px); background: rgba(0,0,0,0.01); }}
    .card:hover .card-preview img {{ transform: scale(1.03); opacity: 1; }}

    /* ── Card preview ────────────────────────────────────────── */
    .card-preview {{
      position: relative; overflow: hidden;
      background: #fafafa;
      display: flex; align-items: center; justify-content: center;
    }}
    .card-preview img {{
      display: block; width: 100%; height: 100%;
      object-fit: contain; padding: 12px;
      transition: transform 0.45s ease, opacity 0.45s ease;
      opacity: 0.9;
    }}
    .card-preview::after {{
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(to top, rgba(245,245,245,0.4) 0%, transparent 50%);
      pointer-events: none;
    }}

    /* ── Card content ────────────────────────────────────────── */
    .card-content {{ display: flex; flex-direction: column; padding: 18px; flex: 1; min-width: 0; }}
    .card-header {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; margin-bottom: 10px; }}
    .card-title {{ font-size: 1rem; font-weight: 600; color: var(--ink); line-height: 1.3; flex: 1; min-width: 0; transition: color 0.2s ease; }}
    .card:hover .card-title {{ color: rgb(var(--tool-rgb)); }}
    .card-body {{ font-size: 0.83rem; color: var(--muted); line-height: 1.5; margin-bottom: 14px; flex: 1; }}

    /* ── Pills & badges ──────────────────────────────────────── */
    .pill {{
      display: inline-flex; align-items: center; gap: 5px;
      padding: 3px 8px; border-radius: 4px;
      font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 500;
      white-space: nowrap; flex-shrink: 0;
    }}
    .pill-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
    .pill-tool {{ background: rgba(var(--tool-rgb), 0.08); border: 1px solid rgba(var(--tool-rgb), 0.2); color: rgb(var(--tool-rgb)); }}
    .pill-tool .pill-dot {{ background: rgb(var(--tool-rgb)); }}
    .badge-full {{ background: rgba(46, 90, 168, 0.08); border: 1px solid rgba(46, 90, 168, 0.2); color: var(--link); }}
    .badge-best {{ background: transparent; border: 1px dashed var(--rule); color: var(--muted); }}

    /* ── Card footer ─────────────────────────────────────────── */
    .card-grid-meta {{
      display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
      padding-top: 12px; border-top: 1px solid var(--rule); margin-top: auto;
    }}
    .card-grid-meta .spacer {{ flex: 1; }}
    .card-list-meta {{ display: none; }}

    /* ── Action links ────────────────────────────────────────── */
    .link-muted {{
      font-family: 'Geist Mono', monospace; font-size: 0.75rem;
      color: var(--soft); transition: color 0.2s ease;
    }}
    .link-muted:hover {{ color: var(--ink); text-decoration: none; }}

    /* ── Animations ──────────────────────────────────────────── */
    @keyframes fade-up {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    /* ── Responsive ──────────────────────────────────────────── */
    @media (prefers-reduced-motion: reduce) {{
      .card,
      .card-preview img,
      .toggle-indicator,
      .toggle-btn {{
        transition: none;
      }}
      .hero {{
        animation: none; opacity: 1; transform: none;
      }}
      .toolbar {{
        animation: none; opacity: 1; transform: none;
      }}
      .gallery {{
        animation: none; opacity: 1; transform: none;
      }}
    }}

    @media (max-width: 600px) {{
      main {{ padding: 40px 14px 64px; }}
      .hero {{ margin-bottom: 48px; }}
      .toolbar {{ flex-direction: column; align-items: stretch; gap: 10px; }}
      .view-toggle {{ align-self: flex-end; }}
      .gallery.view-grid {{ grid-template-columns: 1fr; }}
      .gallery.view-list .card-preview {{ display: none; }}
    }}

    @media print {{
      nav,
      .bg-layer,
      .toolbar,
      .view-toggle {{ display: none; }}
      body {{ background: #ffffff; }}
      main {{ padding: 20px; }}
      .card {{
        box-shadow: none; break-inside: avoid;
        border: 1px solid #ccc;
      }}
      .card:hover {{ transform: none; box-shadow: none; }}
      .card-preview {{ background: #ffffff; }}
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --paper: #2d3142;
        --paper-2: #393e53;
        --ink: #f5f5f5;
        --muted: #bfc0c0;
        --soft: #8e98ac;
        --rule: rgba(245, 245, 245, 0.12);
        --accent: #f08a59;
        --accent-tint: rgba(240, 138, 89, 0.10);
        --link: #6a95d8;
      }}
      body {{ background: var(--paper); }}
      .card {{ background: #393e53; }}
      .card-preview {{ background: #2d3142; }}
      nav {{ background: rgba(45, 49, 66, 0.85); }}
      .toolbar {{ background: rgba(57, 62, 83, 0.8); }}
      .view-toggle {{ background: #2d3142; }}
      .toggle-indicator {{ background: #393e53; }}
    }}
  </style>
</head>
<body>
  <div class="bg-layer" aria-hidden="true">
    <div class="bg-gradient"></div>
    <div class="bg-dots"></div>
  </div>
  <nav>
    <div class="nav-inner">
      <a class="nav-logo" href=".">
        <div class="nav-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/><line x1="7" y1="11.3" x2="17" y2="6.7"/><line x1="7" y1="12.7" x2="17" y2="17.3"/></svg>
        </div>
        <span class="nav-wordmark">Kroki <span>Editorial Diagrams</span></span>
      </a>
    </div>
  </nav>
  <main>
    <header class="hero">
      <h1>{page_title}</h1>
      <p>An interactive, premium-designed gallery of system architectures and request flows, rendered via Kroki.</p>
    </header>
    <div class="toolbar">
      <span class="toolbar-count">{n_entries} diagram{plural_s}</span>
      <div class="view-toggle" id="view-toggle" role="group" aria-label="View mode">
        <div class="toggle-indicator" id="toggle-indicator"></div>
        <button class="toggle-btn" id="btn-grid" type="button" data-view="grid">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Grid
        </button>
        <button class="toggle-btn" id="btn-list" type="button" data-view="list">
          <svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="3.5" cy="6" r="1"/><circle cx="3.5" cy="12" r="1"/><circle cx="3.5" cy="18" r="1"/></svg>
          List
        </button>
      </div>
    </div>
    <div class="gallery view-grid" id="gallery">
{cards_html}
    </div>
  </main>
  <script>
    (function () {{
      const storageKey = "kroki-editorial-diagrams-index-view";
      const gallery    = document.getElementById("gallery");
      const indicator  = document.getElementById("toggle-indicator");
      const btnGrid    = document.getElementById("btn-grid");
      const btnList    = document.getElementById("btn-list");

      function applyView(view) {{
        const isGrid = view === "grid";
        gallery.classList.toggle("view-grid", isGrid);
        gallery.classList.toggle("view-list", !isGrid);
        indicator.style.transform = isGrid ? "translateX(0)" : "translateX(100%)";
        btnGrid.classList.toggle("active", isGrid);
        btnList.classList.toggle("active", !isGrid);
        try {{ localStorage.setItem(storageKey, view); }} catch (_) {{}}
      }}

      let initial = "grid";
      try {{
        const saved = localStorage.getItem(storageKey);
        if (saved === "grid" || saved === "list") initial = saved;
      }} catch (_) {{}}

      applyView(initial);
      btnGrid.addEventListener("click", () => applyView("grid"));
      btnList.addEventListener("click", () => applyView("list"));
    }})();
  </script>
</body>
</html>
"""


def build_diagram_index(root: pathlib.Path, title: str | None = None) -> pathlib.Path:
    entries = []
    for child in sorted(root.iterdir()):
        if child.is_dir():
            entry = load_artifact_entry(child)
            if entry:
                entries.append(entry)

    output_path = root / "index.html"
    page_title = title or "Editorial Diagrams Catalog"
    output_path.write_text(build_index_html(entries, page_title), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a premium index.html catalog for a directory of diagram artifacts.")
    parser.add_argument("--root", required=True, help="Directory containing one artifact folder per diagram.")
    parser.add_argument("--title", help="Optional page title.")
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    output_path = build_diagram_index(root=root, title=args.title)
    print(f"Index HTML: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
