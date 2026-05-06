---
title: OAD Workflow Grammar Over Full Integral Stack
number: 053
status: accepted
date: 2026-05-06
authors: Genesis (RegenTribes)
domain: information
level: system
tags:
  - integral
  - OAD
  - design-system
  - architecture
  - tradeoff
---

# OAD Workflow Grammar Over Full Integral Stack

## Context

Peter Joseph / Revolution Now Ep 60 describes Integral Collective's Open Access Design (OAD) — a 10-module design certification system. RegenTribes is a small community (Hetzner VPS + local HP EliteBook) with no Integral infrastructure (no CDS, COS, ITC, FRS). Vitali requested an ADR covering the full tradeoff of adopting OAD design principles vs. waiting for full Integral stack.

## Decision

Extract OAD's **workflow grammar** (intake → collaborative workspace → multi-lens analysis → certification → knowledge commons) as a standalone design process, without adopting the full Integral stack. Defer material coefficient database and ITC to Phase 2.

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Full OAD (all 10 modules + 5-system Integral stack) | ❌ Premature — requires infrastructure that doesn't exist |
| **B** | OAD workflow grammar only (M1/M2 → M9/M10 loop) | ✅ Adopt — implementable now, maps to existing tools |
| **C** | Bonfires.ai as hosted OAD | ❌ Rejected — subscription cost, no P2P resilience |
| **D** | llm_wiki desktop app | ❌ Rejected — not agent-integrable, no P2P |

## Analysis

### What OAD Gets Right

1. **Design commons**: Every certified design enters a recursive knowledge archive. This maps directly onto SurrealDB + Hyperon migration path.
2. **5-lens evaluation**: M3–M7 applies five independent analysis lenses (ecology, time, physics, labor, context) to every design. This is implementable incrementally.
3. **Version-controlled branching**: M2 is GitHub-for-CAD. Already available via existing git infrastructure.
4. **Ecological coefficient intent**: OAD requires 7 material coefficients (embodied energy, carbon, toxicity, recyclability, water use, land use, scarcity) *before* production. Correct principle, wrong timing.
5. **Post-scarcity incentive model**: Contribution satisfaction over ITC. Culturally dependent, cannot be engineered until community is larger.

### The Blocking Constraints

**Constraint 1 — Material Coefficient Database**: OAD M3 requires a pre-established database of material coefficients. Peter Joseph explicitly notes this data "does not yet exist in public" form. No offline fallback. During internet blackout, M3 fails completely.

**Constraint 2 — Downstream Systems**: OAD outputs to COS (production) and ITC (access values). Neither exists. Without them, certified designs have no execution path.

**Constraint 3 — Constitutional Governance**: OAD thresholds (eco score, feasibility) are policy-determined via CDS. RegenTribes has no formal constitution. No one is authorized to set thresholds.

**Constraint 4 — Scale Mismatch**: OAD is designed for a node (12–200 people) with shared intent. RegenTribes is pre-constitutional. The "shared intent" precondition is not established.

### AME/OAD Integration Gap

AME (Affinity Mapping Engine) maps *people and trust*. OAD certifies *physical goods and ecological footprint*. Different data models, no native bridge.

- AME → "who is trusted to contribute to design X"
- OAD → "is design X eco-viable for production"

These are complementary, not competing. Integration requires deliberate design of the bridge (AME outputs → OAD contributor selection). Not a blocker for Phase 1.

## Consequences

### Positive

- RegenTribes can adopt a rigorous design process immediately using existing tools (git, SurrealDB, future Hyperon)
- OAD's 5-lens evaluation is implementable in phases: M3/M4 first (ecology + time), M5/M6/M7 as community grows
- M10 (knowledge commons) maps directly onto existing SurrealDB graph schema
- No dependency on Integral's other 4 systems

### Negative

- No ITC incentive system — design contribution relies on voluntary engagement
- No material coefficient database — ecological scoring requires approximation during Phase 1
- No CDS — threshold-setting for certification is ad hoc
- Offline operation limited to whatever can be locally computed

### Risks

- Community may attempt full OAD adoption prematurely, hitting the 4 blocking constraints
- Without ITC, creative ideation may stall due to lack of clear incentive
- Without constitutional governance, "who decides" questions will recur

## Resolution

**Adopt Option B: OAD Workflow Grammar**

| Phase | Actions |
|-------|---------|
| **Phase 1** (now) | Implement M1/M2 (submission + collaborative workspace) using git. Begin M10 (knowledge commons) using SurrealDB. Approximate M3 ecological intent with simple material checklists until full coefficient database is available. |
| **Phase 2** (3–6 months) | Build M3–M7 5-lens evaluation incrementally. Develop regional material coefficient database via open-source LCA tools (OpenLCA + Ecoinvent). Establish constitutional rules for threshold-setting via community consensus. |
| **Phase 3** (6–12 months) | Integrate AME outputs for contributor selection. Implement ITC-inspired access value calculation for community-owned designs. Establish P2P mesh sync for offline resilience. |

**Reject Bonfires.ai** — subscription model and insufficient resistance for offline-first requirements.

**Reject llm_wiki desktop app** — not integratable with agent workflow.

## References

- Peter Joseph, Revolution Now Ep 60: Integral OAD (integralcollective.io)
- OAD 10 Modules: M1 intake, M2 workspace, M3–M7 five-lens analysis, M8 optimization, M9 certification, M10 commons
- AME spec: github.com/regentribes/mythogen-ame (AME-PC-Manual.md)
- RegenTribes kbase: rad:z4WAr7CiNkf5JAoAb1srwi7gDz8nU

## Supersedes

N/A — first ADR on this topic.

## Related

- 051: AME and FOT — Trust and Affinity Mapping
- 052: Drone Swarms — Physical Infrastructure for FCL