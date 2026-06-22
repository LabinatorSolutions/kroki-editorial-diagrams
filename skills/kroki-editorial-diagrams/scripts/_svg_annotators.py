#!/usr/bin/env python3
import base64
import re
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import fromstring as _safe_fromstring

from _svg_utils import NS, clean_svg_text, append_class, soften_svg_background


def annotate_graphviz_like(root: ET.Element) -> tuple[int, int]:
    node_count = 0
    edge_count = 0

    for group in root.findall(".//svg:g", NS):
        classes = set((group.get("class") or "").split())
        title = group.find("svg:title", NS)
        title_text = (title.text or "").strip() if title is not None else ""

        if "node" in classes and title_text:
            group.set("data-node-id", title_text)
            append_class(group, "interactive-node")
            node_count += 1
            continue

        if "edge" not in classes or not title_text:
            continue

        match = re.match(r"^(.*?)\s*(-+>|--)\s*(.*?)$", title_text)
        if not match:
            continue

        source, operator, target = match.groups()
        group.set("data-edge-source", source.strip())
        group.set("data-edge-target", target.strip())
        group.set("data-edge-kind", "directed" if ">" in operator else "undirected")
        append_class(group, "interactive-edge")
        edge_count += 1

    return node_count, edge_count


def annotate_mermaid(root: ET.Element) -> tuple[int, int]:
    node_count = 0
    edge_count = 0

    for group in root.findall(".//svg:g", NS):
        classes = set((group.get("class") or "").split())
        group_id = group.get("id") or ""
        if "node" not in classes:
            continue

        match = re.match(r"^(?:.*?-)?flowchart-(.+)-\d+$", group_id)
        if not match:
            continue

        group.set("data-node-id", match.group(1))
        append_class(group, "interactive-node")
        node_count += 1

    edge_candidates = list(root.findall(".//svg:path", NS)) + list(
        root.findall(".//svg:g", NS)
    )
    for element in edge_candidates:
        classes = set((element.get("class") or "").split())
        if "flowchart-link" not in classes:
            continue

        edge_id = element.get("id") or ""
        match = re.match(r"^(?:.*?-)?L_([^_]+)_([^_]+)_\d+$", edge_id)
        if not match:
            continue

        source, target = match.groups()
        directed = "marker-end" in element.attrib or "marker-start" in element.attrib
        element.set("data-edge-source", source)
        element.set("data-edge-target", target)
        element.set("data-edge-kind", "directed" if directed else "undirected")
        append_class(element, "interactive-edge")
        edge_count += 1

    return node_count, edge_count


def annotate_sequence(root: ET.Element) -> tuple[int, int]:
    node_ids: set[str] = set()
    edge_count = 0

    for group in root.findall(".//svg:g", NS):
        classes = set((group.get("class") or "").split())

        if "participant-head" in classes or "participant-lifeline" in classes:
            node_id = group.get("data-entity-uid")
            if not node_id:
                continue
            group.set("data-node-id", node_id)
            append_class(group, "interactive-node")
            node_ids.add(node_id)
            continue

        if "message" not in classes:
            continue

        source = group.get("data-entity-1")
        target = group.get("data-entity-2")
        if not source or not target:
            continue

        edge_kind = "undirected" if source == target else "directed"
        group.set("data-edge-source", source)
        group.set("data-edge-target", target)
        group.set("data-edge-kind", edge_kind)
        append_class(group, "interactive-edge")
        edge_count += 1

    return len(node_ids), edge_count


def annotate_plantuml_description(root: ET.Element) -> tuple[int, int]:
    node_count = 0
    edge_count = 0

    for group in root.findall(".//svg:g", NS):
        classes = set((group.get("class") or "").split())

        if "entity" in classes:
            node_id = group.get("id")
            if not node_id:
                continue
            group.set("data-node-id", node_id)
            append_class(group, "interactive-node")
            node_count += 1
            continue

        if "link" not in classes:
            continue

        source = group.get("data-entity-1")
        target = group.get("data-entity-2")
        if not source or not target:
            continue

        group.set("data-edge-source", source)
        group.set("data-edge-target", target)
        group.set("data-edge-kind", "directed")
        append_class(group, "interactive-edge")
        edge_count += 1

    return node_count, edge_count


def annotate_d2(root: ET.Element) -> tuple[int, int]:
    node_count = 0
    edge_count = 0

    def is_base64(s: str) -> bool:
        if not re.match(r"^[A-Za-z0-9+/=]+$", s):
            return False
        try:
            padded = s + "=" * (-len(s) % 4)
            decoded = base64.b64decode(padded.encode("ascii"), validate=True)
            decoded_str = decoded.decode("utf-8")
            if not decoded_str:
                return False
            return all(c.isprintable() or c in "\t\r\n" for c in decoded_str)
        except Exception:
            return False

    def decode_base64(s: str) -> str:
        padded = s + "=" * (-len(s) % 4)
        return base64.b64decode(padded.encode("ascii")).decode("utf-8", errors="ignore")

    for group in root.findall(".//svg:g", NS):
        classes = (group.get("class") or "").split()
        for cls in classes:
            if is_base64(cls):
                decoded = decode_base64(cls)
                if "->" in decoded or "-&gt;" in decoded:
                    match = re.match(r"^\((.+?)\s*(?:->|-&gt;)\s*(.+?)\)(?:\[\d+\])?$", decoded)
                    if match:
                        source, target = match.groups()
                        group.set("data-edge-source", source.strip())
                        group.set("data-edge-target", target.strip())
                        group.set("data-edge-kind", "directed")
                        append_class(group, "interactive-edge")
                        edge_count += 1
                else:
                    group.set("data-node-id", decoded.strip())
                    append_class(group, "interactive-node")
                    node_count += 1
                break

    return node_count, edge_count


def annotate_svg(engine: str, svg_text: str) -> tuple[str, dict[str, str | int]]:
    cleaned = clean_svg_text(svg_text)
    root = _safe_fromstring(cleaned)
    soften_svg_background(root)

    if engine == "graphviz":
        node_count, edge_count = annotate_graphviz_like(root)
        tier = "full" if edge_count else "best-effort"
    elif engine == "d2":
        node_count, edge_count = annotate_d2(root)
        tier = "full" if edge_count else "best-effort"
    elif engine == "erd":
        node_count, edge_count = annotate_graphviz_like(root)
        tier = "best-effort"
    elif engine == "mermaid":
        node_count, edge_count = annotate_mermaid(root)
        tier = "best-effort"
    elif engine == "plantuml" and root.get("data-diagram-type") == "SEQUENCE":
        node_count, edge_count = annotate_sequence(root)
        tier = "full"
    elif engine in {"plantuml", "c4plantuml"}:
        node_count, edge_count = annotate_plantuml_description(root)
        tier = "full" if edge_count else "best-effort"
    elif engine == "structurizr":
        node_count, edge_count = annotate_plantuml_description(root)
        tier = "full" if edge_count else "best-effort"
    else:
        node_count = 0
        edge_count = 0
        tier = "limited"

    root.set("data-interactive-engine", engine)
    root.set("data-interactive-tier", tier)
    return ET.tostring(root, encoding="unicode"), {
        "engine": engine,
        "nodes": node_count,
        "edges": edge_count,
        "tier": tier,
    }
