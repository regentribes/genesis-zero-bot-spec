---
name: arch
description: |
  Maintain ArchiMate enterprise architecture models for the genesis-zero-bot-arch repository.
  Uses Archi headless (Docker container) for rendering and coArchi for git-based model storage.
  Generates HTML reports via deploy-archi-report GitHub Action. Always reply with direct link
  to deployed page after push.
triggers:
  - "archimate"
  - "architecture model"
  - "enterprise architecture"
  - "Archi model"
  - "archi diagram"
  - "view"
---

Use this skill when working with ArchiMate models in the `genesis-zero-bot-arch` repository.

## Arch Repository URLs

| Service | URL |
|---------|-----|
| GitHub repo | https://github.com/regentribes/genesis-zero-bot-arch |
| GitHub Pages | https://regentribes.github.io/genesis-zero-bot-arch/ |
| Archi report (root) | https://regentribes.github.io/genesis-zero-bot-arch/ |

## Repository Structure

```
genesis-zero-bot-arch/
├── model/              ← Symlink: model -> model-example/ (Archi directory format)
├── model-example/       ← Archi model with folder.xml at root
├── models/             ← .archimate XML files (coArchi format, single-file)
├── assets/             ← CSS (pure B/W minimal, aligned with wiki + ADR + spec)
├── build_index.py      ← Generates custom index.html for Archi report
├── _config.yml
├── .nojekyll
└── .github/workflows/
    └── deploy.yml      ← Runs Archi Docker + deploy-archi-report action
```

## Four-Output Pipeline

This skill produces the **arch** output. The other three outputs are managed by separate skills:

| Output | Repo | Skill | URL pattern |
|--------|------|-------|-------------|
| Wiki | `genesis-zero-bot-wiki` | `wiki` | `sources/NNNN-slug.html` |
| ADRs | `genesis-zero-bot-adrs` | `adrs` | `adr-NNNN.html` |
| Specs | `genesis-zero-bot-spec` | `spec` | `feature-*-slug.html` |
| Archi | `genesis-zero-bot-arch` | `arch` | `index.html` (root) |

All four repos share the same pure B/W minimal visual style.

## Deployment Workflow

GitHub Actions handles everything on push to `main` via a single `WoozyMasta/archimate-ci-image@5.7.0-1.0.6` action call:

```
1. Initialize gh-pages branch (if needed)
2. Build custom index (build_index.py)
3. Single action: HTML + PDF + DOCX + model export → gh-pages root
4. Add custom index alongside Archi reports
5. Trigger Pages deployment
```

**Output formats (all at gh-pages root):**
- `index.html` — custom index with model cards and links to the Archi viewer
- `ArchiMetal.pdf` — PDF report (JasperReports)
- `ArchiMetal.docx` — Word report (JasperReports)
- `ArchiMetal.archimate` — exported model file
- `css/`, `elements/`, `hints/`, `js/`, `lib/` — Archi viewer assets (iframe-based)

**Important:** The `model/` symlink points to `model-example/` so that `model/folder.xml` resolves inside the Archi Docker container. Never remove this symlink.

## Quick Test (Docker)

```bash
docker run --rm ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6 --help
```

## Generating HTML Report Locally

```bash
cd /tmp/genesis-zero-bot-arch
docker run --rm \
  -v $(pwd):/archi/project \
  -e ARCHI_PROJECT_PATH=/archi/project \
  -e ARCHI_HTML_REPORT_ENABLED=true \
  -e ARCHI_REPORT_PATH=/archi/project/.archi_report \
  ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6
```

## Arch Layers (3.2 Specification)

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

**Physical layer:** Water cycle (tank, sensors, drip irrigation), Food production (soil, compost, polyculture), Energy (solar, powerbank, microgrid), Shelter/materials (local materials, construction)

**Social layer:** Holon (local biome unit), Commons governance (Ostrom's 8 principles), Reputation system (evidence-based competition), Egregore (collective ideological entity)

**Knowledge layer:** Genesis Brain (SurrealDB knowledge graph), Agent skills (SKILL.md encoded institutional knowledge), MCP (Model Context Protocol for tool integration), Spatial addressing (graph traversal, not GPS coordinates)

**Infrastructure layer:** Edge nodes (HP EliteBook local VPS), Mesh radio (80-400ms latency), Raft consensus (leader election, delta-consensus CRDT), Federated mesh (no central cloud dependency)

### Integral Collective Node Architecture

- **OAD** — Open Architecture Design (strategy layer)
- **ITC** — Integral TRIZ Constructor (innovation layer)
- **CDS** — Collective Decision System (governance layer)
- **COS** — Commons Operating System (resource layer)
- **FRS** — Federation Rules System (protocol layer)

## Adding a New Arch Model

### Step 1 — Create model XML

Models are `.archimate` XML files following the Arch 3.2 schema.
Use coArchi format (git-mergeable single-file XML).

**Minimal model structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<archimate:model xmlns:archimate="http://www.archimatetool.com/archimate"
  name="Regenerative Neighbourhood"
  id="model-regen-neighbourhood"
  version="1.0.0">

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

### Step 2 — Add to model-example/ (Archi directory format)

For Archi to generate HTML reports, models must live in `model-example/` (accessed via `model/` symlink):

```bash
cd /tmp/genesis-zero-bot-arch
cp your-model.archimate model-example/your-model.archimate
# Or create as folder.xml structure in model-example/
```

### Step 3 — Commit and push

```bash
cd /tmp/genesis-zero-bot-arch
git add model-example/your-model.archimate
git commit -m "model: your model name"
git push origin main
```

CI automatically generates HTML report and deploys to Pages.

### Step 4 — Verify deployment

```bash
gh run list --repo regentribes/genesis-zero-bot-arch --limit 3
```

Live at: `https://regentribes.github.io/genesis-zero-bot-arch/`


**Always reply with the direct deployed link when the task is complete.**

## Tool Inventory

| Command | Purpose |
|---------|---------|
| `docker run ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6 --help` | Test Docker setup |
| `gh run list --repo regentribes/genesis-zero-bot-arch --limit 3` | Check Pages + CI deployment |
| Jasper reports (PDF, DOCX) auto-generated by CI | JasperReports via archimate-ci-image |

## Visual Style Alignment

All four repos (wiki, ADR, spec, arch) share the same pure B/W minimal CSS:

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

## Maintenance Rules

- Models use Arch 3.2 specification compliance
- coArchi format for git-based collaboration (mergeable XML)
- Export formats: SVG (diagrams), HTML (reports), PNG (images)
- CSS aligned with wiki/ADR/spec repos — same tokens, same theme toggle
- `model/` symlink must exist and point to `model-example/` for Archi HTML report generation
- Never commit `_site/` or HTML artifacts — CI builds them

---

*Last updated: 2026-05-08 · arch v2 (aligned to wiki)*