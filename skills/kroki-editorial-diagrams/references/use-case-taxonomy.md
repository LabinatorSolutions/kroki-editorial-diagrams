# Use-Case Taxonomy Reference

Identify your diagramming intent and map it to the recommended engine family.

---

## 1. Intent Mapping Directory

### System Structure & Containers

* **Intent**: Map microservices, databases, borders, APIs, and cloud services.
* **Ideal Family**: C4 Container / General Architecture.
* **Preferred Engine**: `d2` or `c4plantuml`.

### Process & Logic Flow

* **Intent**: Map algorithmic pipelines, logical decision branches, user onboarding flows, or continuous integration steps.
* **Ideal Family**: Flowchart.
* **Preferred Engine**: `mermaid` (clean simple lines) or `plantuml` (custom shapes).

### Message Passing Over Time

* **Intent**: Show sequence of service calls, timing triggers, API round-trips, or client-server authentication handshakes.
* **Ideal Family**: Sequence Diagram.
* **Preferred Engine**: `plantuml` (deep timing and activation lifelines).

### Database Schemas

* **Intent**: Map relational keys, columns, foreign connections, and table attributes.
* **Ideal Family**: ERD.
* **Preferred Engine**: `erd` (clean structural output) or `plantuml` (database class shapes).

### Lifecycle Machine States

* **Intent**: Show logical transition states of an entity (e.g. Order created → Pending → Dispatched → Shipped).
* **Ideal Family**: State Diagram.
* **Preferred Engine**: `plantuml` or `mermaid`.

### Business Process & Workflow Compliance

* **Intent**: Model formal business processes with swimlanes, BPMN events, gateways, and tasks for compliance or handoff documentation.
* **Ideal Family**: BPMN.
* **Preferred Engine**: `bpmn`.
* **Note**: BPMN output cannot be styled via this skill's design tokens. Use only when the audience requires standard BPMN notation; prefer `mermaid` flowcharts or `plantuml` activity diagrams for internal process documentation.
