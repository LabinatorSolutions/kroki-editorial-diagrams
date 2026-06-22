#!/usr/bin/env python3
import argparse
import pathlib
import sys
from defusedxml.ElementTree import ParseError

from _svg_utils import soften_svg_background  # noqa: F401 — re-exported for callers
from _svg_annotators import annotate_svg  # noqa: F401 — re-exported for callers


def build_html_document(
    svg_markup: str, title: str, metadata: dict[str, str | int]
) -> str:
    engine = metadata["engine"]

    # Editorial colors matching the design system
    _engine_colors = {
        "plantuml":    ("235, 108, 54",  "#eb6c36"),
        "c4plantuml":  ("46, 90, 168",   "#2e5aa8"),
        "d2":          ("79, 93, 117",   "#4f5d75"),
        "graphviz":    ("79, 93, 117",   "#4f5d75"),
        "mermaid":     ("122, 131, 153", "#7a8399"),
        "erd":         ("191, 192, 192", "#bfc0c0"),
        "bpmn":        ("100, 120, 140", "#64788c"),
        "structurizr": ("46, 90, 168",   "#2e5aa8"),
        "nomnoml":     ("79, 93, 117",   "#4f5d75"),
        "wavedrom":    ("122, 131, 153", "#7a8399"),
        "vega":        ("46, 90, 168",   "#2e5aa8"),
        "vegalite":    ("46, 90, 168",   "#2e5aa8"),
        "ditaa":       ("191, 192, 192", "#bfc0c0"),
        "svgbob":      ("191, 192, 192", "#bfc0c0"),
        "goat":        ("191, 192, 192", "#bfc0c0"),
        "pikchr":      ("122, 131, 153", "#7a8399"),
        "excalidraw":  ("235, 108, 54",  "#eb6c36"),
        "wireviz":     ("79, 93, 117",   "#4f5d75"),
    }
    _tool_rgb, _tool_hex = _engine_colors.get(engine, ("235, 108, 54", "#eb6c36"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
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

      --dim-opacity: 0.28;
      --node-shadow: drop-shadow(0 0 10px rgba(235, 108, 54, 0.3));
      --focus-ring: rgba(235, 108, 54, 0.4);
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      font-family: 'Geist', 'Inter', system-ui, sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}

    .diagram-nav {{
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 100;
      height: 52px;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 0 18px;
      background: rgba(245, 245, 245, 0.85);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--rule);
    }}

    .back-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 6px;
      background: rgba(45, 49, 66, 0.05);
      border: 1px solid var(--rule);
      color: var(--muted);
      font-size: 0.8rem;
      font-weight: 500;
      text-decoration: none;
      transition: color 0.2s ease, background 0.2s ease;
      font-family: 'Geist Mono', monospace;
    }}

    .back-link:hover {{ color: var(--ink); background: rgba(45,49,66,0.08); text-decoration: none; }}

    .back-link svg {{
      width: 13px; height: 13px;
      stroke: currentColor; fill: none;
      stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
      flex-shrink: 0;
    }}

    .nav-title {{
      font-family: 'Instrument Serif', serif;
      font-size: 1.35rem;
      font-weight: 400;
      color: var(--ink);
      letter-spacing: -0.01em;
    }}

    .nav-sep {{ color: var(--soft); font-size: 0.75rem; }}

    .shell {{
      width: 100%;
      padding: 10px;
      padding-top: 62px;
    }}

    .stage {{
      position: relative;
      overflow: hidden;
      padding: 10px;
      min-height: calc(100vh - 72px);
      border-radius: 12px;
      border: 1px solid var(--rule);
      background: var(--paper-2);
      box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.4),
        0 8px 24px rgba(0, 0, 0, 0.05);
    }}

    .stage:focus-visible {{
      outline: 2px solid var(--focus-ring);
      outline-offset: 2px;
    }}

    .canvas-toolbar {{
      position: absolute;
      top: 18px;
      right: 18px;
      z-index: 5;
      display: flex;
      gap: 6px;
      align-items: center;
      padding: 6px;
      border-radius: 8px;
      background: rgba(245, 245, 245, 0.9);
      border: 1px solid var(--rule);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }}

    .canvas-toolbar button {{
      border: 1px solid var(--rule);
      background: #ffffff;
      color: var(--muted);
      border-radius: 4px;
      min-width: 34px;
      height: 30px;
      padding: 0 8px;
      font-family: 'Geist Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 120ms ease, background 120ms ease, color 120ms ease, border-color 120ms ease;
    }}

    .canvas-toolbar button:hover {{
      background: var(--accent-tint);
      border-color: var(--accent);
      color: var(--accent);
      transform: translateY(-1px);
    }}

    .canvas-toolbar button:active {{ transform: translateY(0); }}

    .canvas-toolbar button:focus-visible {{
      outline: 2px solid var(--focus-ring);
      outline-offset: 2px;
    }}

    .canvas-viewport {{
      position: relative;
      height: calc(100vh - 92px);
      min-height: 0;
      overflow: hidden;
      border-radius: 8px;
      background: var(--paper);
      cursor: default;
      touch-action: none;
      user-select: none;
    }}

    .canvas-viewport.is-pan-mode {{ cursor: grab; }}
    .canvas-viewport.is-dragging {{ cursor: grabbing; }}

    .canvas-content {{
      position: absolute;
      top: 0;
      left: 0;
      transform-origin: 0 0;
      will-change: transform;
      overflow: visible;
    }}

    .canvas-content svg {{
      display: block;
      width: max-content;
      max-width: none;
      height: auto;
      overflow: visible;
      background: transparent !important;
    }}

    .canvas-status {{
      position: absolute;
      left: 18px;
      bottom: 18px;
      z-index: 4;
      padding: 5px 12px;
      border-radius: 6px;
      background: rgba(245, 245, 245, 0.9);
      border: 1px solid var(--rule);
      color: var(--muted);
      font-family: 'Geist Mono', monospace;
      font-size: 0.78rem;
      font-weight: 500;
      letter-spacing: 0.04em;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
      backdrop-filter: blur(10px);
      pointer-events: none;
    }}

    .interactive-node {{
      cursor: pointer;
      transition: opacity 160ms ease, filter 160ms ease, transform 160ms ease;
      transform-origin: center center;
    }}

    .interactive-edge {{
      transition: opacity 160ms ease, filter 160ms ease;
    }}

    .interactive-node.is-dimmed,
    .interactive-edge.is-dimmed {{
      opacity: var(--dim-opacity);
    }}

    .interactive-node.is-active,
    .interactive-node.is-connected,
    .interactive-edge.is-connected {{
      opacity: 1;
    }}

    .interactive-node.is-active {{
      filter: var(--node-shadow);
    }}

    .interactive-node.is-active rect,
    .interactive-node.is-active ellipse,
    .interactive-node.is-active circle,
    .interactive-node.is-active polygon,
    .interactive-node.is-active path {{
      stroke-width: 2.2px !important;
      stroke: var(--accent) !important;
    }}

    .interactive-node.is-connected rect,
    .interactive-node.is-connected ellipse,
    .interactive-node.is-connected circle,
    .interactive-node.is-connected polygon,
    .interactive-node.is-connected path {{
      stroke-width: 1.7px !important;
      stroke: var(--link) !important;
    }}

    .interactive-edge.is-connected path,
    .interactive-edge.is-connected line,
    .interactive-edge.is-connected polyline {{
      stroke-width: 2.2px !important;
      stroke: var(--accent) !important;
      stroke-linecap: round;
      filter: drop-shadow(0 0 4px rgba(235, 108, 54, 0.2));
    }}

    .interactive-edge.is-connected polygon {{
      fill: var(--accent) !important;
      stroke: var(--accent) !important;
    }}

    .interactive-edge.is-connected text,
    .interactive-edge.is-connected tspan {{
      fill: var(--accent) !important;
      stroke: none !important;
      font-weight: 700 !important;
    }}

    .interactive-edge.edge-flow-forward path,
    .interactive-edge.edge-flow-forward line,
    .interactive-edge.edge-flow-forward polyline {{
      stroke-dasharray: 10 6;
      animation: flow-forward 850ms linear infinite;
    }}

    .interactive-edge.edge-flow-reverse path,
    .interactive-edge.edge-flow-reverse line,
    .interactive-edge.edge-flow-reverse polyline {{
      stroke-dasharray: 10 6;
      animation: flow-reverse 850ms linear infinite;
    }}

    .interactive-edge.edge-neutral path,
    .interactive-edge.edge-neutral line,
    .interactive-edge.edge-neutral polyline {{
      stroke-dasharray: 8 6;
      animation: flow-neutral 1150ms ease-in-out infinite;
    }}

    @keyframes flow-forward  {{ to {{ stroke-dashoffset: -16; }} }}
    @keyframes flow-reverse  {{ to {{ stroke-dashoffset:  16; }} }}

    @keyframes flow-neutral {{
      0%   {{ stroke-dashoffset: 0;  filter: brightness(1);   }}
      50%  {{ stroke-dashoffset: 8;  filter: brightness(1.2); }}
      100% {{ stroke-dashoffset: 16; filter: brightness(1);   }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .interactive-node,
      .interactive-edge {{
        transition: none;
      }}
      .interactive-edge.edge-flow-forward path,
      .interactive-edge.edge-flow-forward line,
      .interactive-edge.edge-flow-forward polyline,
      .interactive-edge.edge-flow-reverse path,
      .interactive-edge.edge-flow-reverse line,
      .interactive-edge.edge-flow-reverse polyline,
      .interactive-edge.edge-neutral path,
      .interactive-edge.edge-neutral line,
      .interactive-edge.edge-neutral polyline {{
        animation: none;
      }}
      .canvas-toolbar button {{
        transition: none;
      }}
    }}

    @media (max-width: 720px) {{
      .shell {{ padding: 6px; padding-top: 58px; }}
      .canvas-toolbar {{ top: 10px; right: 10px; gap: 4px; padding: 5px; }}
      .canvas-toolbar button {{ min-width: 30px; height: 28px; padding: 0 6px; }}
      .canvas-viewport {{ height: calc(100vh - 74px); }}
      .canvas-status {{ left: 10px; bottom: 10px; }}
    }}

    @media print {{
      .diagram-nav,
      .canvas-toolbar,
      .canvas-status {{ display: none; }}
      .shell {{ padding: 0; }}
      .stage {{
        border: none; border-radius: 0; padding: 0;
        box-shadow: none; background: #ffffff;
      }}
      .canvas-viewport {{
        height: auto; overflow: visible;
        background: #ffffff;
      }}
      .canvas-content {{
        position: static; transform: none !important;
      }}
      .canvas-content svg {{ max-width: 100%; height: auto; }}
      .interactive-node,
      .interactive-edge {{
        opacity: 1 !important; filter: none !important;
      }}
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
        --dim-opacity: 0.22;
        --node-shadow: drop-shadow(0 0 10px rgba(240, 138, 89, 0.3));
        --focus-ring: rgba(240, 138, 89, 0.4);
      }}
      .canvas-toolbar button {{ background: #393e53; }}
      .canvas-content svg {{ background: transparent !important; }}
    }}
  </style>
</head>
<body>
  <nav class="diagram-nav">
    <a class="back-link" href="../index.html">
      <svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
      Gallery
    </a>
    <span class="nav-sep">/</span>
    <span class="nav-title">{title}</span>
    <span style="margin-left:auto;padding:3px 9px;border-radius:6px;font-family:'Geist Mono',monospace;font-size:0.7rem;font-weight:600;background:{_tool_hex}15;border:1px solid {_tool_hex}30;color:{_tool_hex};">{engine}</span>
  </nav>
  <main class="shell">
    <section class="stage" id="diagram-stage" tabindex="0" aria-label="Interactive diagram canvas">
      <div class="canvas-toolbar" aria-label="Canvas controls">
        <button type="button" id="zoom-out" aria-label="Zoom out">-</button>
        <button type="button" id="zoom-in" aria-label="Zoom in">+</button>
        <button type="button" id="fit-view" aria-label="Fit to screen">Fit</button>
        <button type="button" id="actual-size" aria-label="Reset to one hundred percent">100%</button>
      </div>
      <div class="canvas-viewport" id="diagram-viewport">
        <div class="canvas-content" id="diagram-content">
          {svg_markup}
        </div>
      </div>
      <div class="canvas-status" id="diagram-status">Fit 100%</div>
    </section>
  </main>
  <script>
    const stage = document.getElementById("diagram-stage");
    const viewport = document.getElementById("diagram-viewport");
    const content = document.getElementById("diagram-content");
    const status = document.getElementById("diagram-status");
    const zoomInButton = document.getElementById("zoom-in");
    const zoomOutButton = document.getElementById("zoom-out");
    const fitButton = document.getElementById("fit-view");
    const actualSizeButton = document.getElementById("actual-size");
    const svg = content.querySelector("svg");

    if (svg) {{
      const nodes = Array.from(svg.querySelectorAll("[data-node-id]"));
      const edges = Array.from(svg.querySelectorAll("[data-edge-source][data-edge-target]"));
      const PADDING = 28;
      const PAN_STEP = 60;
      const SCALE_STEP = 1.16;
      const MIN_SCALE = 0.08;
      const MAX_SCALE = 3.5;
      let rawBounds;
      try {{
        rawBounds = svg.getBBox();
      }} catch (e) {{
        rawBounds = {{ x: 0, y: 0, width: 0, height: 0 }};
      }}
      const normalizedBounds = (Number.isFinite(rawBounds.width) && rawBounds.width > 0 && Number.isFinite(rawBounds.height) && rawBounds.height > 0)
        ? rawBounds
        : null;

      let scale = 1;
      let translateX = 0;
      let translateY = 0;
      let fitScale = 1;
      let isSpacePressed = false;
      let isDragging = false;
      let activePointerId = null;
      let dragStartX = 0;
      let dragStartY = 0;
      let dragOriginX = 0;
      let dragOriginY = 0;
      let shouldAutoFitOnResize = true;
      let selectedNodeId = null;
      let hasDragged = false;

      if (normalizedBounds) {{
        svg.style.transform = `translate(${{-normalizedBounds.x}}px, ${{-normalizedBounds.y}}px)`;
        svg.style.transformOrigin = "top left";
        content.style.width = `${{normalizedBounds.width}}px`;
        content.style.height = `${{normalizedBounds.height}}px`;
      }}

      const getCanvasSize = () => {{
        if (normalizedBounds) {{
          return {{ width: normalizedBounds.width, height: normalizedBounds.height }};
        }}

        const viewBox = svg.viewBox && svg.viewBox.baseVal;
        if (viewBox && viewBox.width && viewBox.height) {{
          return {{ width: viewBox.width, height: viewBox.height }};
        }}

        let box;
        try {{
          box = svg.getBBox();
        }} catch (e) {{
          box = {{ x: 0, y: 0, width: 800, height: 600 }};
        }}
        return {{ width: box.width || 1, height: box.height || 1 }};
      }};

      const clampScale = (nextScale) => Math.min(MAX_SCALE, Math.max(MIN_SCALE, nextScale));

      const applyTransform = () => {{
        content.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
        const zoomPercent = Math.round(scale * 100);
        status.textContent = `Zoom ${{zoomPercent}}%`;
      }};

      const centerForScale = (nextScale) => {{
        const canvas = getCanvasSize();
        const viewportRect = viewport.getBoundingClientRect();
        return {{
          x: (viewportRect.width - canvas.width * nextScale) / 2,
          y: (viewportRect.height - canvas.height * nextScale) / 2,
        }};
      }};

      const fitToViewport = () => {{
        const canvas = getCanvasSize();
        const viewportRect = viewport.getBoundingClientRect();
        const usableWidth = Math.max(120, viewportRect.width - PADDING * 2);
        const usableHeight = Math.max(120, viewportRect.height - PADDING * 2);
        fitScale = clampScale(Math.min(usableWidth / canvas.width, usableHeight / canvas.height));
        scale = fitScale;
        const centered = centerForScale(scale);
        translateX = centered.x;
        translateY = centered.y;
        shouldAutoFitOnResize = true;
        applyTransform();
        status.textContent = `Fit ${{Math.round(scale * 100)}}%`;
      }};

      const resetToActualSize = () => {{
        scale = 1;
        const centered = centerForScale(scale);
        translateX = centered.x;
        translateY = centered.y;
        shouldAutoFitOnResize = false;
        applyTransform();
      }};

      const zoomAtPoint = (factor, clientX, clientY) => {{
        const viewportRect = viewport.getBoundingClientRect();
        const pointerX = clientX - viewportRect.left;
        const pointerY = clientY - viewportRect.top;
        const nextScale = clampScale(scale * factor);
        const scaleRatio = nextScale / scale;

        translateX = pointerX - (pointerX - translateX) * scaleRatio;
        translateY = pointerY - (pointerY - translateY) * scaleRatio;
        scale = nextScale;
        shouldAutoFitOnResize = false;
        applyTransform();
      }};

      const panBy = (dx, dy) => {{
        translateX += dx;
        translateY += dy;
        shouldAutoFitOnResize = false;
        applyTransform();
      }};

      fitToViewport();

      const nodeMap = new Map();
      const nodeCenterCache = new Map();
      for (const node of nodes) {{
        const nodeId = node.dataset.nodeId;
        if (!nodeMap.has(nodeId)) nodeMap.set(nodeId, []);
        nodeMap.get(nodeId).push(node);
      }}

      const getNodeCenter = (nodeId) => {{
        if (nodeCenterCache.has(nodeId)) return nodeCenterCache.get(nodeId);

        const relatedNodes = nodeMap.get(nodeId) || [];
        if (!relatedNodes.length) return null;

        let totalX = 0;
        let totalY = 0;
        let count = 0;

        for (const related of relatedNodes) {{
          try {{
            const box = related.getBBox();
            if (!Number.isFinite(box.x) || !Number.isFinite(box.y)) continue;
            totalX += box.x + box.width / 2;
            totalY += box.y + box.height / 2;
            count += 1;
          }} catch (e) {{
            // Ignore if element is not rendered / hidden
          }}
        }}

        const center = count ? {{ x: totalX / count, y: totalY / count }} : null;
        nodeCenterCache.set(nodeId, center);
        return center;
      }};

      const getFlowDirectionClass = (sourceId, targetId) => {{
        const sourceCenter = getNodeCenter(sourceId);
        const targetCenter = getNodeCenter(targetId);
        if (!sourceCenter || !targetCenter) return "edge-flow-forward";

        const dx = targetCenter.x - sourceCenter.x;
        const dy = targetCenter.y - sourceCenter.y;

        if (Math.abs(dx) >= Math.abs(dy)) {{
          return dx >= 0 ? "edge-flow-forward" : "edge-flow-reverse";
        }}

        return dy >= 0 ? "edge-flow-forward" : "edge-flow-reverse";
      }};

      const resetState = () => {{
        selectedNodeId = null;
        for (const node of nodes) {{
          node.classList.remove("is-dimmed", "is-active", "is-connected");
        }}
        for (const edge of edges) {{
          edge.classList.remove(
            "is-dimmed",
            "is-connected",
            "edge-incoming",
            "edge-outgoing",
            "edge-neutral",
            "edge-flow-forward",
            "edge-flow-reverse"
          );
        }}
      }};

      const focusNode = (nodeId) => {{
        resetState();
        selectedNodeId = nodeId;

        for (const node of nodes) {{
          node.classList.add("is-dimmed");
        }}
        for (const edge of edges) {{
          edge.classList.add("is-dimmed");
        }}

        for (const active of nodeMap.get(nodeId) || []) {{
          active.classList.remove("is-dimmed");
          active.classList.add("is-active");
        }}

        for (const edge of edges) {{
          const source = edge.dataset.edgeSource;
          const target = edge.dataset.edgeTarget;
          if (source !== nodeId && target !== nodeId) continue;

          edge.classList.remove("is-dimmed");
          edge.classList.add("is-connected");

          const directed = edge.dataset.edgeKind === "directed";
          if (!directed || source === target) {{
            edge.classList.add("edge-neutral");
          }} else if (source === nodeId) {{
            edge.classList.add("edge-outgoing");
            edge.classList.add(getFlowDirectionClass(source, target));
          }} else {{
            edge.classList.add("edge-incoming");
            edge.classList.add(getFlowDirectionClass(source, target));
          }}

          for (const relatedId of [source, target]) {{
            for (const related of nodeMap.get(relatedId) || []) {{
              related.classList.remove("is-dimmed");
              related.classList.add(relatedId === nodeId ? "is-active" : "is-connected");
            }}
          }}
        }}
      }};

      for (const node of nodes) {{
        node.addEventListener("click", (event) => {{
          if (hasDragged) return;
          event.stopPropagation();
          focusNode(node.dataset.nodeId);
        }});
      }}

      svg.addEventListener("click", (event) => {{
        if (hasDragged) return;
        const clickedNode = event.target.closest("[data-node-id]");
        if (clickedNode) return;
        resetState();
      }});

      viewport.addEventListener("click", (event) => {{
        if (hasDragged) return;
        if (!event.target.closest("[data-node-id]")) {{
          resetState();
        }}
      }});

      zoomInButton.addEventListener("click", () => {{
        const rect = viewport.getBoundingClientRect();
        zoomAtPoint(SCALE_STEP, rect.left + rect.width / 2, rect.top + rect.height / 2);
      }});

      zoomOutButton.addEventListener("click", () => {{
        const rect = viewport.getBoundingClientRect();
        zoomAtPoint(1 / SCALE_STEP, rect.left + rect.width / 2, rect.top + rect.height / 2);
      }});

      fitButton.addEventListener("click", fitToViewport);
      actualSizeButton.addEventListener("click", resetToActualSize);

      viewport.addEventListener("wheel", (event) => {{
        if (event.ctrlKey || event.metaKey || event.altKey) {{
          event.preventDefault();
          const factor = Math.exp(-event.deltaY * 0.0015);
          zoomAtPoint(factor, event.clientX, event.clientY);
          return;
        }}

        event.preventDefault();
        const panX = event.shiftKey ? -event.deltaY : -event.deltaX;
        const panY = event.shiftKey ? 0 : -event.deltaY;
        panBy(panX, panY);
      }}, {{ passive: false }});

      viewport.addEventListener("pointerdown", (event) => {{
        const isOverNode = event.target.closest("[data-node-id]");
        const wantsPan = event.button === 1 || (event.button === 0 && (isSpacePressed || !isOverNode)) || event.pointerType === "touch";
        if (!wantsPan) return;

        event.preventDefault();
        isDragging = true;
        hasDragged = false;
        activePointerId = event.pointerId;
        dragStartX = event.clientX;
        dragStartY = event.clientY;
        dragOriginX = translateX;
        dragOriginY = translateY;
        viewport.classList.add("is-dragging");
        viewport.setPointerCapture(event.pointerId);
      }});

      viewport.addEventListener("pointermove", (event) => {{
        if (!isDragging || event.pointerId !== activePointerId) return;
        const dx = event.clientX - dragStartX;
        const dy = event.clientY - dragStartY;
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {{
          hasDragged = true;
        }}
        translateX = dragOriginX + dx;
        translateY = dragOriginY + dy;
        shouldAutoFitOnResize = false;
        applyTransform();
      }});

      const endDrag = (event) => {{
        if (!isDragging) return;
        if (event && activePointerId !== null && event.pointerId !== activePointerId) return;
        isDragging = false;
        activePointerId = null;
        viewport.classList.remove("is-dragging");
        setTimeout(() => {{
          hasDragged = false;
        }}, 0);
      }};

      viewport.addEventListener("pointerup", endDrag);
      viewport.addEventListener("pointercancel", endDrag);
      viewport.addEventListener("pointerleave", endDrag);

      const updatePanModeClass = () => {{
        viewport.classList.toggle("is-pan-mode", isSpacePressed && !isDragging);
      }};

      window.addEventListener("keydown", (event) => {{
        if (event.target && /input|textarea|select/i.test(event.target.tagName)) return;

        if (event.code === "Space") {{
          event.preventDefault();
        }}

        if (event.code === "Space" && !event.repeat) {{
          isSpacePressed = true;
          updatePanModeClass();
        }}

        if (event.key === "+" || event.key === "=") {{
          event.preventDefault();
          const rect = viewport.getBoundingClientRect();
          zoomAtPoint(SCALE_STEP, rect.left + rect.width / 2, rect.top + rect.height / 2);
        }} else if (event.key === "-" || event.key === "_") {{
          event.preventDefault();
          const rect = viewport.getBoundingClientRect();
          zoomAtPoint(1 / SCALE_STEP, rect.left + rect.width / 2, rect.top + rect.height / 2);
        }} else if (event.key === "0") {{
          event.preventDefault();
          fitToViewport();
        }} else if (event.key === "1") {{
          event.preventDefault();
          resetToActualSize();
        }} else if (event.key === "ArrowLeft") {{
          event.preventDefault();
          panBy(PAN_STEP, 0);
        }} else if (event.key === "ArrowRight") {{
          event.preventDefault();
          panBy(-PAN_STEP, 0);
        }} else if (event.key === "ArrowUp") {{
          event.preventDefault();
          panBy(0, PAN_STEP);
        }} else if (event.key === "ArrowDown") {{
          event.preventDefault();
          panBy(0, -PAN_STEP);
        }}
      }});

      window.addEventListener("keyup", (event) => {{
        if (event.code === "Space") {{
          event.preventDefault();
          isSpacePressed = false;
          updatePanModeClass();
        }}
      }});

      window.addEventListener("resize", () => {{
        if (shouldAutoFitOnResize) fitToViewport();
      }});
    }}
  </script>
</body>
</html>
"""


def build_interactive_html_file(
    engine: str, svg_text: str, output_path: pathlib.Path, title: str
) -> dict[str, str | int]:
    annotated_svg, metadata = annotate_svg(engine=engine, svg_text=svg_text)
    html = build_html_document(svg_markup=annotated_svg, title=title, metadata=metadata)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Wrap a Kroki SVG in an interactive HTML viewer."
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.1.0")
    parser.add_argument(
        "--engine", required=True, help="Kroki engine used to render the SVG."
    )
    parser.add_argument("--input", required=True, help="Path to the rendered SVG file.")
    parser.add_argument(
        "--output", required=True, help="Path to write the interactive HTML."
    )
    parser.add_argument("--title", help="Viewer title. Defaults to the SVG stem.")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)
    title = args.title or input_path.stem.replace("-", " ").title()
    svg_text = input_path.read_text(encoding="utf-8")

    try:
        metadata = build_interactive_html_file(
            engine=args.engine,
            svg_text=svg_text,
            output_path=output_path,
            title=title,
        )
    except (ParseError, ValueError, KeyError, UnicodeDecodeError) as exc:
        print(f"Interactive build failed: {exc}", file=sys.stderr)
        return 1

    print(f"Interactive HTML: {output_path}")
    print(
        "Interactive summary:"
        f" engine={metadata['engine']}"
        f" tier={metadata['tier']}"
        f" nodes={metadata['nodes']}"
        f" edges={metadata['edges']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
