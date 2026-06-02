# Kroki Safe Subset Reference

To prevent rendering errors, standardise on the tested Kroki engine versions and format properties defined here.

---

## 1. Engine & Output Format Matrix

The table reflects the current public `kroki.io` instance. Engines marked **companion** require a separate Docker container in self-hosted Kroki deployments.

| Engine        | SVG | PNG | PDF | JPG | Notes                                  |
|---------------|-----|-----|-----|-----|----------------------------------------|
| `plantuml`    | Yes | Yes | Yes | No  | Full styling via `<style>` block       |
| `c4plantuml`  | Yes | Yes | Yes | No  | Use `!include <C4Container>` (local)   |
| `d2`          | Yes | Yes | No  | No  | ELK/dagre layouts; sketch mode         |
| `mermaid`     | Yes | Yes | Yes | No  | **Companion server** required          |
| `graphviz`    | Yes | Yes | Yes | No  | DOT language; best for dense DAGs      |
| `bpmn`        | Yes | Yes | No  | No  | **Companion server** required          |
| `erd`         | Yes | Yes | No  | No  | Minimal styling options                |
| `structurizr` | Yes | Yes | No  | No  | C4 via native DSL; no remote includes  |
| `nomnoml`     | Yes | No  | No  | No  | Lightweight UML via `#` directives     |
| `wavedrom`    | Yes | Yes | No  | No  | **Companion server** required; JSON    |
| `vega`        | Yes | Yes | No  | No  | **Companion server** required; JSON    |
| `vegalite`    | Yes | Yes | No  | No  | **Companion server** required; JSON    |
| `ditaa`       | Yes | Yes | No  | No  | ASCII art → clean SVG                  |
| `svgbob`      | Yes | No  | No  | No  | ASCII art → crisp SVG                  |
| `goat`        | Yes | No  | No  | No  | ASCII art (Go); inline README diagrams |
| `pikchr`      | Yes | No  | No  | No  | Minimalist line-art PIC dialect        |
| `bytefield`   | Yes | No  | No  | No  | Bit/byte field protocol diagrams       |
| `excalidraw`  | Yes | Yes | No  | No  | **Companion server**; hand-drawn only  |
| `diagramsnet` | Yes | Yes | No  | No  | **Companion server**; experimental     |
| `wireviz`     | Yes | Yes | No  | No  | Wiring harness / cable diagrams        |
| `actdiag`     | Yes | Yes | No  | No  | Activity diagrams (BlockDiag family)   |
| `blockdiag`   | Yes | Yes | No  | No  | Block diagrams (BlockDiag family)      |
| `seqdiag`     | Yes | Yes | No  | No  | Sequence diagrams (BlockDiag family)   |
| `nwdiag`      | Yes | Yes | No  | No  | Network diagrams (BlockDiag family)    |
| `packetdiag`  | Yes | Yes | No  | No  | Packet format diagrams                 |
| `rackdiag`    | Yes | Yes | No  | No  | Rack unit diagrams                     |
| `symbolator`  | Yes | Yes | No  | No  | Hardware/HDL component symbols         |
| `umlet`       | Yes | Yes | No  | No  | UMLet XML format                       |

> **Companion server**: On the public `kroki.io` instance, companion-server engines work transparently. For self-hosted Kroki, you must run the appropriate companion Docker image (`yuzutech/kroki-mermaid`, `yuzutech/kroki-bpmn`, `yuzutech/kroki-excalidraw`, `yuzutech/kroki-diagramsnet`) alongside the gateway and configure the matching `KROKI_*_HOST` environment variable.

---

## 2. Request Methods

Kroki accepts both GET and POST requests.

### GET — Encoded URL (shareable, offline-ready)

The diagram source is encoded as: **deflate (raw, wbits=-15) → base64url → strip trailing `=`**

Python encoding:

```python
import zlib, base64
compressed = zlib.compressobj(level=9, wbits=-15)
data = compressed.compress(source.encode("utf-8")) + compressed.flush()
encoded = base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")
url = f"https://kroki.io/{engine}/{format}/{encoded}"
```

The render script's `--print-url-only` flag generates this URL for you. Paste it into any browser or share it directly.

### POST — Plain Text (used by this skill's render script)

Send the diagram source as the request body with `Content-Type: text/plain; charset=utf-8`. The output format is part of the URL path:

```http
POST https://kroki.io/{engine}/{format}
Content-Type: text/plain; charset=utf-8

<diagram source here>
```

This is what `render_kroki_diagram.py` does internally via `curl`. The `%` character trap is handled safely because `text/plain` prevents URL-decoding of percent signs.

### POST — JSON Body (alternative)

Send a JSON body to the root endpoint with all parameters inline:

```json
{
  "diagram_source": "...",
  "diagram_type": "graphviz",
  "output_format": "svg",
  "diagram_options": { "key": "value" }
}
```

---

## 3. Diagram Options

Some engines accept options that modify rendering behaviour without changing the diagram source. Kroki supports passing options via:

1. **HTTP headers** (POST text/plain): `Kroki-Diagram-Options-<Key>: <value>`
2. **Query parameters** (GET): `?key=value`
3. **`diagram_options` field** (POST JSON body)

The render script uses the HTTP header approach. Pass `--diagram-option key=value` (repeatable):

```bash
python3 scripts/render_kroki_diagram.py \
  --engine d2 \
  --input source.d2 \
  --output rendered.svg \
  --diagram-option theme=earth-tones \
  --diagram-option layout=elk
```

### D2 Options

| Option | Values | Default |
| --- | --- | --- |
| `theme` | `default` (0), `neutral-gray` (1), `cool-classics` (4), `earth-tones` (103), `dark-mauve` (200), `terminal` (300) — full list: d2lang.com/tour/themes | `default` |
| `layout` | `dagre`, `elk` | `dagre` |
| `sketch` | empty string flag — enables hand-drawn aesthetic | off |

### PlantUML Options

| Option | Values | Description |
| --- | --- | --- |
| `theme` | string | Prepends `!theme <value>` — e.g. `plain`, `minty`, `sketchy-outline` |
| `no-metadata` | empty string flag | Strips diagram source from SVG/PNG metadata |

---

## 4. Known Safe Syntax Constraints

* **`%` characters**: Always safe when POSTing with `Content-Type: text/plain`. Never strip or escape `%` manually.
* **Mermaid `<br/>` line breaks**: Use `<br/>` inside node labels; literal `\n` corrupts SVG XML output.
* **PlantUML `<style>` block**: Requires PlantUML ≥ 1.2020.x (Kroki ≥ 0.19). Older self-hosted instances need `skinparam` directives instead.
* **C4 stdlib include**: Use `!include <C4Container>` (local); the GitHub raw URL fails on self-hosted SECURE mode.
* **Mermaid frontmatter (`---\ntitle:...\n---`)**: Older Kroki-bundled Mermaid versions may reject YAML frontmatter. Use the `%%{init:...}%%` block instead.
