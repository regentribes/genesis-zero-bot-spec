---
name: archimate-skill
description: |
  Transform arbitrary information (URLs, files, raw text) into ArchiMate models, wiki entries, ADRs, and Gherkin specs
  in the context of regenerative neighbourhoods and Integral Collective nodes.
  Uses Archi headless (Docker container) for rendering and coArchi for git-based model storage.
---

Use this skill when transforming content into ArchiMate models for regenerative community architecture.

## Repos

| Service | URL |
|---------|-----|
| Archimate repo | https://github.com/regentribes/genesis-zero-bot-archimate |
| Wiki repo | https://github.com/regentribes/genesis-zero-bot-wiki |
| ADR repo | https://github.com/regentribes/genesis-zero-bot-adrs |
| Spec repo | https://github.com/regentribes/genesis-zero-bot-spec |

## Archimate Repo Structure

```
genesis-zero-bot-archimate/
├── models/           ← .archimate XML files (coArchi format)
├── exports/          ← rendered output (SVG, HTML, PNG)
├── scripts/          ← JArchi automation scripts
├── templates/        ← reusable ArchiMate model templates
├── assets/           ← CSS (aligned with wiki/ADR/spec — pure B/W minimal)
├── build.py          ← generates rendered output from models
├── _config.yml
└── .github/workflows/pages.yml
```

## Pipeline: From Arbitrary Information to Four Outputs

```
Input (URL, file, raw text)
    │
    ├─► Extract → Raw content
    │        │
    │   ┌────┴────────────────────────────────────┐
    │   │                                         │
    │  [Wiki Generator]                      [ArchiMate Generator]
    │  sources/concepts                      models/*.archimate
    │  in wiki vault                          relationships + views
    │   │                                         │
    │  [ADR Generator]                      [Gherkin Generator]
    │  docs/*.md (MADR 4.0.0)               docs/*.feature
    │  in adrs repo                          in spec repo
    │   │                                         │
    │   └──────────────┬──────────────────────────┘
    │                 │
    │            [Render Pipeline]
    │   Archi Docker container (coArchi)
    │   SVG diagrams, HTML reports, PNG exports
    │   JArchi scripts for model generation
    │   → exports/ directory
    │   → GitHub Pages deployment
```

## Toolchain

### Docker: Archi Headless (archimate-ci-image)

Uses `ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6` for headless model processing.

**Quick test:**
```bash
docker run --rm ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6 --help
```

**Render HTML report from a git-based model:**
```bash
mkdir -p ./report
chmod o+rw ./report

docker run --rm \
  -v $(pwd)/report:/archi/report \
  -e GIT_REPOSITORY=https://github.com/regentribes/genesis-zero-bot-archimate.git \
  -e ARCHI_HTML_REPORT_ENABLED=true \
  -e ARCHI_EXPORT_MODEL_ENABLED=true \
  ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6
```

**Local model export:**
```bash
docker run --rm \
  -v $(pwd)/models:/archi/project \
  -v $(pwd)/exports:/archi/report \
  ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6
```

**Environment variables:**
- `ARCHI_PROJECT_PATH=/archi/project` — model location
- `ARCHI_HTML_REPORT_ENABLED=true` — generate HTML report
- `ARCHI_HTML_REPORT_PATH` — output path for HTML
- `ARCHI_CSV_REPORT_ENABLED=true` — generate CSV report
- `ARCHI_EXPORT_MODEL_ENABLED=true` — export as .archimate XML
- `ARCHI_APP=com.archimatetool.commandline.app` — CLI mode
- `GIT_REPOSITORY` — clone from git (coArchi plugin)
- `ARCHI_PROJECT_PATH` — local path override

### JArchi (archi-scripting-plugin)

JavaScript scripting plugin for Archi. Installed in the Docker container.

**Key scripts (from ThomasRohde/archi-scripts):**
- `Generate Model.ajs` — AI-powered model generation from description
- `Expand Model.ajs` — expand existing model around a selected element
- `Generate Capability Model.ajs` — hierarchical capability model via AI
- `Smart Style Sync.ajs` — apply visual styling based on element properties
- `Model Health Check.ajs` — validate model integrity
- `Export View to Draw.io.ajs` — convert views to draw.io format

**JArchi API reference:** https://github.com/archimatetool/archi-scripting-plugin/wiki

### ArchiMate MCP Server (thijs-hakkenberg/archimate-mcp)

Node.js MCP server for LLM-to-ArchiMate interaction.

**Setup:**
```bash
git clone https://github.com/thijs-hakkenberg/archimate-mcp.git
cd archimate-mcp && npm install && npm run build

# Add to OpenClaw MCP config
# command: node, args: [/path/to/archimate-mcp/dist/index.js]
```

**Tools provided:**
- `archimate_create_model` / `archimate_open_model` / `archimate_save_model`
- `archimate_create_*_element` (motivation, strategy, business, application, technology, implementation)
- `archimate_create_relationship` — validates against ArchiMate 3.2 spec
- `archimate_list_views` / `archimate_create_view` / `archimate_add_to_view`
- `archimate_export_mermaid` / `archimate_export_diagram` (SVG/PNG) / `archimate_export_html_deck`
- `archimate_impact_analysis` — dependency analysis for architecture changes

**Note:** MCP server requires pre-compiled TypeScript (dist/index.js). The scripting plugin (jArchi) is a separate binary distribution from archimatetool.com/plugins/#jArchi — NOT compiled from the archi-scripting-plugin repo.

## ArchiMate Layers (3.2 Specification)

| Layer | Elements | Use for |
|-------|---------|---------|
| **Motivation** | Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint, Meaning, Value | Why, governance, values |
| **Strategy** | Resource, Capability, ValueStream, CourseOfAction | Strategic positioning |
| **Business** | Actor, Role, Collaboration, Service, Process, Function, Event, Object, Product | Community members, activities |
| **Application** | Component, Collaboration, Interface, Service, Function, DataObject | Software systems |
| **Technology** | Node, Device, SystemSoftware, Path, Network, Artifact, Facility | Infrastructure |
| **Implementation** | WorkPackage, Deliverable, Plateau, Gap, ImplementationEvent | Migration planning |

**Relationships:** Composition, Aggregation, Assignment, Realization, Serving, Access, Influence, Association, Triggering, Flow, Specialization

## Regenerative Neighbourhood Domain Model

### Core concepts to model

**Physical layer:**
- Water cycle (tank, sensors, drip irrigation)
- Food production (soil, compost, polyculture)
- Energy (solar, powerbank, microgrid)
- Shelter/materials (local materials, construction)

**Social layer:**
- Holon (local biome unit)
- Commons governance (Ostrom's 8 principles)
- Reputation system (evidence-based competition)
- Egregore (collective ideological entity)

**Knowledge layer:**
- Genesis Brain (SurrealDB knowledge graph)
- Agent skills (SKILL.md encoded institutional knowledge)
- MCP (Model Context Protocol for tool integration)
- Spatial addressing (graph traversal, not GPS coordinates)

**Infrastructure layer:**
- Edge nodes (HP EliteBook local VPS)
- Mesh radio (80-400ms latency)
- Raft consensus (leader election, delta-consensus CRDT)
- Federated mesh (no central cloud dependency)

### Integral Collective Node Architecture

**OAD** — Open Architecture Design (strategy layer)
**ITC** — Integral TRIZ Constructor (innovation layer)
**CDS** — Collective Decision System (governance layer)
**COS** — Commons Operating System (resource layer)
**FRS** — Federation Rules System (protocol layer)

## Adding a New ArchiMate Model

### Step 1 — Create model directory

```bash
mkdir -p models/regen-neighbourhood/
```

### Step 2 — Create model XML

Models are `.archimate` XML files following the ArchiMate 3.2 schema.
Use coArchi-compatible format (git-mergeable).

**Minimal model structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<archimate:model xmlns:archimate="http://www.archimatetool.com/archimate"
  name="Regenerative Neighbourhood"
  id="model-regen-neighbourhood"
  version="1.0.0">

  <!-- Properties -->
  <property key="domain" value="regenerative-community"/>
  <property key="layer" value="all"/>

  <!-- Business Layer: Community members and activities -->
  <business-actor id="actor-holon" name="Holon Unit" documentation="Local biome self-governance"/>
  <business-process id="process-commons" name="Commons Governance" documentation="Ostrom-principle operation"/>
  <business-service id="service-water" name="Water Cycle Service" documentation="Circular water management"/>

  <!-- Application Layer: Software systems -->
  <application-component id="app-genesis" name="Genesis Brain" documentation="SurrealDB knowledge graph"/>

  <!-- Technology Layer: Infrastructure -->
  <node id="node-edge" name="Edge Node" documentation="HP EliteBook local VPS"/>
  <artifact id="art-sensor" name="Sensor Data" documentation="DHT22 + soil moisture readings"/>

  <!-- Relationships -->
  <relationship id="rel-serves" type="serving"
    source="#app-genesis" target="#actor-holon"/>

</archimate:model>
```

### Step 3 — Add to views

Create `<view>` elements with `<diagram>` references.
Use JArchi scripts for automatic layout.

### Step 4 — Render and export

```bash
# Via Docker
docker run --rm \
  -v $(pwd)/models:/archi/project \
  -v $(pwd)/exports:/archi/report \
  ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6

# Or via build.py locally
python3 build.py
```

### Step 5 — Commit and push

```bash
git add models/
git commit -m "model: regen-neighbourhood v1.0"
git push origin main
```

## Visual Style Alignment

All four repos (wiki, ADR, spec, archimate) share the same pure B/W minimal CSS:

```css
:root {
  --bg: #000000;
  --text: #888888;
  --heading: #ffffff;
  --muted: #555555;
  --border: #222222;
  --code-bg: #0a0a0a;
}
body.light {
  --bg: #ffffff;
  --text: #333333;
  --heading: #000000;
  --muted: #888888;
  --border: #e0e0e0;
  --code-bg: #f5f5f5;
}
```

Dark default, localStorage theme toggle, 860px max-width.
When editing CSS: update all four repos.

## Reference Repositories

| Repo | Purpose |
|------|---------|
| bian-official/public | BIAN API specifications (banking domain reference) |
| wilmerkrisp/patterns | ArchiMate pattern catalog (analysis, design, DDD patterns) |
| ThomasRohde/archi-scripts | JArchi automation scripts (model generation, export) |
| archimatetool/archi-modelrepository-plugin | coArchi plugin for git-based model collaboration |
| WoozyMasta/archimate-ci-image | Docker container for headless Archi |
| thijs-hakkenberg/archimate-mcp | MCP server for LLM ↔ ArchiMate interaction |

## Tool Inventory

| Command | Purpose |
|---------|---------|
| `docker run ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6 --help` | Test Docker setup |
| `python3 build.py` (in archimate repo) | Build HTML/SVG/PNG exports from models |
| `gh run list --repo regentribes/genesis-zero-bot-archimate --limit 3` | Check Pages deployment |
| `/tmp/ghokin check docs/*.feature` | Validate Gherkin specs |
| `openclaw wiki compile` / `openclaw wiki lint` | Wiki vault maintenance |

## Maintenance Rules

- Models use ArchiMate 3.2 specification compliance
- coArchi format for git-based collaboration (mergeable XML)
- JArchi scripts for automation where possible
- Export formats: SVG (diagrams), HTML (reports), PNG (images)
- CSS aligned with wiki/ADR/spec repos — same tokens, same theme toggle
- All four outputs (wiki, ADR, spec, archimate) are synchronized from the same input

---

*Last updated: 2026-05-08 · Archimate skill v1.0*