---
name: oad-navigator
description: Navigate Integral OAD (Open Access Design) challenges and produce Architecture Decision Records (ADRs) using the adrs CLI tool. Wraps OAD 10-module design workflow with tradeoff analysis for RegenTribes context.
metadata:
  requires:
    bins:
      - adrs
---

# OAD Navigator Skill

Navigates design challenges through the Integral Open Access Design (OAD) workflow grammar, producing ADRs that document decisions and tradeoffs.

## OAD 10-Module Reference

### Group 1: Intake
- **M1** — Design submission and structured specification
- **M2** — Collaborative design workspace (GitHub-for-CAD, branch/merge)

### Group 2: Analysis (5 lenses)
- **M3** — Material ecological coefficient engine (7 coefficients: energy, carbon, toxicity, recyclability, water, land, scarcity)
- **M4** — Life cycle and maintainability modeling (MTTF, repairability index, life cycle burden)
- **M5** — Feasibility and constraint simulation (physics: stress, fluid, thermal, fatigue)
- **M6** — Skill and labor step decomposition (production steps, hours, skill tiers)
- **M7** — Systems integration and architectural coordination (compatibility with existing infrastructure)

### Group 3: Optimization
- **M8** — Optimization and efficiency engine (algorithmic + human)

### Group 4: Approval + Archive
- **M9** — Validation, certification, and release manager (risk index, hard gate)
- **M10** — Knowledge commons and reuse repository (recursive archive, FRS feedback loop)

## Usage

### Generate an ADR for a design decision

```bash
cd ~/.openclaw/workspace-genesis/skills/oad-navigator
./adrs new "Your Decision Title" --format madr
```

The adrs binary is in this skill directory.

### ADR Format (MADR)

```markdown
---
title: Decision title
number: NNN
status: proposed|accepted|deprecated|superseded
date: YYYY-MM-DD
authors: Genesis (RegenTribes)
domain: physical|social|information|exchange
level: cell|tissue|organ|system|body
tags:
  - key-tag
---

# Title

## Context
[What is the situation?]

## Decision
[What was decided?]

## Options Considered
| Option | Description | Verdict |
|--------|-------------|---------|
| A | ... | ✅/❌ |
| B | ... | ✅/❌ |

## Analysis
[Why this decision over alternatives]

## Consequences
### Positive
### Negative
### Risks

## Resolution
[Final decision and implementation path]

## References
[Links, sources, prior ADRs]

## Related
[Linked ADRs]
```

## Common OAD Navigation Patterns

### Pattern 1: Phase-Gated Adoption
OAD M1/M2 → M9/M10 loop is implementable immediately.
M3–M7 (5-lens analysis) requires material coefficient database + constitutional thresholds.
M3 is the blocking constraint for offline operation.

**ADR decision tree:**
1. Is this design for hardware/physical goods? → OAD applies
2. Does RegenTribes have CDS constitutional rules? → If no, M9 thresholds are undefined
3. Is offline operation required? → If yes, M3 material coefficients must be locally cached
4. Is ITC incentive system needed? → If yes, defer to Phase 2 (community maturity)

### Pattern 2: Ecological Coefficient Approximation (Phase 1)
Without full M3 database, approximate with:
- Simple checklist: embodied energy (low/med/high), toxicity (0-1), recyclability (Y/N/local infrastructure)
- Weight by regional context (water-stressed = higher water coefficient weight)
- Defer precise numbers until OpenLCA + Ecoinvent integration

### Pattern 3: AME/OAD Bridge
AME maps people trust → OAD maps design viability
- AME outputs V-crystal state, FOT readiness, LJMB profile
- OAD contributor selection uses AME trust scores
- Integration is Phase 2 — not a Phase 1 blocker

### Pattern 4: Knowledge Commons → SurrealDB Migration
OAD M10 → SurrealDB schema:
- Every certified design = node with properties (ecology score, lifecycle burden, labor hours)
- Design versions = temporal edges
- Commons reuse = graph traversal for similar designs
- Future: Hyperon inference over M10 commons

## ADR Storage

RegenTribes ADRs are stored at:
- `~/.openclaw/workspace-genesis/docs/adr/` (canonical, committed to repo)
- Skill local: `~/.openclaw/workspace-genesis/skills/oad-navigator/adr/`

Use the canonical path for all production ADRs.

## Quick Commands

```bash
cd ~/.openclaw/workspace-genesis/skills/oad-navigator

# List all ADRs
./adrs list

# Check ADR health
./adrs doctor

# Generate TOC
./adrs generate toc

# Search ADRs
./adrs search "ecological coefficient"
```

## Constraints

- adrs binary requires interactive terminal (not suitable for subagent automation)
- For automated ADR creation: write Markdown directly to `docs/adr/` directory
- Use MADR 4.0.0 format for machine-readable metadata
- All ADRs must reference the ROOT (000-ROOT.md) framework

## References

- Integral Collective OAD: integralcollective.io
- Peter Joseph Revolution Now Ep 60 (OAD source)
- adrs CLI: github.com/joshrotenberg/adrs
- MADR format:adr.github.io/madr/