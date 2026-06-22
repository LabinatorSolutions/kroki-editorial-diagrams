#!/usr/bin/env python3
import re
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
NS = {"svg": SVG_NS}

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def clean_svg_text(svg_text: str) -> str:
    svg_text = re.sub(r"<\?xml[^>]*\?>", "", svg_text, flags=re.IGNORECASE)
    svg_text = re.sub(r"<!DOCTYPE[^>]*>", "", svg_text, flags=re.IGNORECASE)
    svg_text = re.sub(r"<\?.*?\?>", "", svg_text, flags=re.DOTALL)
    return svg_text.strip()


def append_class(element: ET.Element, class_name: str) -> None:
    classes = set(filter(None, (element.get("class") or "").split()))
    classes.add(class_name)
    element.set("class", " ".join(sorted(classes)))


def soften_svg_background(root: ET.Element) -> None:
    style = root.get("style")
    if style:
        cleaned = re.sub(
            r"background\s*:\s*[^;]+;?", "", style, flags=re.IGNORECASE
        ).strip()
        root.set("style", cleaned)

    parent_map = {child: parent for parent in root.iter() for child in parent}

    def get_svg_viewbox(element) -> tuple[float, float, float, float] | None:
        curr = element
        while curr is not None:
            tag = curr.tag
            if tag == f"{{{SVG_NS}}}svg" or tag == "svg":
                vb = curr.get("viewBox")
                if vb:
                    try:
                        parts = [float(p) for p in vb.replace(",", " ").split()]
                        if len(parts) == 4:
                            return parts[0], parts[1], parts[2], parts[3]
                    except ValueError:
                        pass
            curr = parent_map.get(curr)
        # Fall back to root viewBox
        vb = root.get("viewBox")
        if vb:
            try:
                parts = [float(p) for p in vb.replace(",", " ").split()]
                if len(parts) == 4:
                    return parts[0], parts[1], parts[2], parts[3]
            except ValueError:
                pass
        return None

    rects = root.findall(".//svg:rect", NS)
    for rect in rects:
        try:
            rect_width = float(rect.get("width", "0"))
            rect_height = float(rect.get("height", "0"))
            rect_x = float(rect.get("x", "0"))
            rect_y = float(rect.get("y", "0"))
        except ValueError:
            continue

        vb_coords = get_svg_viewbox(rect)
        if not vb_coords:
            continue
        min_x, min_y, width, height = vb_coords

        style_value = rect.get("style", "")
        fill = rect.get("fill", "").lower()
        has_no_stroke = "stroke:none" in style_value.replace(" ", "").lower()
        fills_background = (
            abs(rect_x - min_x) <= max(2.0, abs(min_x) * 0.02)
            and abs(rect_y - min_y) <= max(2.0, abs(min_y) * 0.02)
            and abs(rect_width - width) <= max(2.0, width * 0.02)
            and abs(rect_height - height) <= max(2.0, height * 0.02)
        )

        if fills_background and (fill or has_no_stroke):
            parent = parent_map.get(rect)
            if parent is not None:
                parent.remove(rect)
            break

    polygons = root.findall(".//svg:polygon", NS)
    for polygon in polygons:
        points_value = polygon.get("points", "").strip()
        if not points_value:
            continue

        coords: list[tuple[float, float]] = []
        try:
            for pair in points_value.split():
                x_text, y_text = pair.split(",")
                coords.append((float(x_text), float(y_text)))
        except ValueError:
            continue

        if len(coords) < 4:
            continue

        vb_coords = get_svg_viewbox(polygon)
        if not vb_coords:
            continue
        min_x, min_y, width, height = vb_coords

        xs = [x for x, _ in coords]
        ys = [y for _, y in coords]
        poly_min_x = min(xs)
        poly_min_y = min(ys)
        poly_width = max(xs) - poly_min_x
        poly_height = max(ys) - poly_min_y
        fill = polygon.get("fill", "").lower()
        style_value = polygon.get("style", "")
        has_no_stroke = "stroke:none" in style_value.replace(" ", "").lower()
        fills_background = (
            abs(poly_min_x - min_x) <= max(6.0, abs(min_x) * 0.03)
            and abs(poly_min_y - min_y) <= max(6.0, abs(min_y) * 0.03)
            and abs(poly_width - width) <= max(6.0, width * 0.03)
            and abs(poly_height - height) <= max(6.0, height * 0.03)
        )

        if fills_background and (fill or has_no_stroke):
            parent = parent_map.get(polygon)
            if parent is not None:
                parent.remove(polygon)
            break
