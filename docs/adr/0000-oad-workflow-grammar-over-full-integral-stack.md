---
title: Integral OAD Workflow Grammar — Phase-Gated Adoption
number: 0000
status: accepted
date: 2026-05-06
authors: Genesis
domain: information
level: system
tags:
  - integral
  - OAD
  - design-system
  - architecture
  - tradeoff
---

## Integral OAD Workflow Grammar — Phase-Gated Adoption

### Context

Peter Joseph describes the Integral Collective Open Access Design (OAD).
OAD is a 10-module design certification system.

The modules are:

- M1: intake
- M2: collaborative workspace
- M3–M7: five-lens analysis
- M8: optimization
- M9: certification
- M10: knowledge commons

OAD is the engineering backbone of the Integral parallel economy.
Its radical claim is this:

Every design must be certified against 7 ecological coefficients before anything is built.
The coefficients cover: embodied energy, carbon, toxicity, recyclability, water use, land use, scarcity.

Vitali requested evaluation of OAD as the design system for community hardware/tool development.

### Decision

Adopt OAD workflow grammar.
Do not adopt the full Integral stack yet.
Defer the material coefficient engine and ITC to Phase 2.

OAD workflow grammar:

```text
M1 (intake) → M2 (collaborative workspace) → M3–M7 (analysis) → M8 (optimization) → M9 (certification) → M10 (knowledge commons)
```

This grammar is portable.
It maps to existing tools:

- git for M2
- SurrealDB for M10
- open-source LCA tools for future M3

### Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Full OAD — all 10 modules + 5-system Integral stack (CDS, COS, ITC, FRS) | ❌ Premature — requires infrastructure that does not exist |
| **B** | OAD workflow grammar only — structural process without downstream systems | ✅ Adopt — implementable now, maps to existing tools |
| **C** | Defer entirely until full Integral stack exists | ❌ Rejected — process grammar is valuable independently |

### Analysis

#### What OAD Gets Right

1. **Design commons (M10)**: Every certified design enters a recursive knowledge archive.
This maps directly onto SurrealDB + Hyperon migration path.

2. **Five-lens evaluation (M3–M7)**: Five independent analysis lenses apply to every design.
The lenses are: ecology, time, physics, labor, context.
Implementable incrementally.

3. **Version-controlled branching (M2)**: GitHub-for-CAD.
Available now via existing git infrastructure.

4. **Ecological coefficient intent**: OAD requires 7 material coefficients before production.
The principle is correct.
The timing for Phase 1 is wrong.

5. **Post-scarcity incentive model**: Contribution satisfaction over monetary compensation.
This is culturally dependent.
It cannot be engineered until the community is larger.

#### The Four Blocking Constraints

OAD modules M3–M10 require pieces that do not exist yet.

| Constraint | Module | Why It Blocks |
|------------|--------|---------------|
| **No material coefficient database** | M3 | Proprietary data. No offline fallback. Fails during internet blackout. |
| **No COS/ITC/FRS** | M9/M10 | No execution path without downstream systems. |
| **No constitutional governance** | M9 thresholds | Policy-determined thresholds. No authorized setter yet. |
| **Scale mismatch** | All | OAD assumes 12–200 people with shared intent. Pre-constitutional community cannot meet this precondition. |

#### Phase-Gated Path

The workflow grammar is implementable in phases.

| Phase | Actions |
|-------|---------|
| **Phase 1** (now) | M1 + M2 using git. |

M10 using SurrealDB.
Approximate M3 ecological intent with checklists until coefficient database is available. |
| **Phase 2** (3–6 months) | Build M3–M7 incrementally.
Develop regional coefficient database via OpenLCA + Ecoinvent.
Establish constitutional threshold-setting. |
| **Phase 3** (6–12 months) | Integrate AME outputs for contributor trust scoring.
Implement ITC-inspired access value calculation.
P2P mesh sync for offline resilience. |

### Consequences

#### Positive

- RegenTribes gains a rigorous, proven design process immediately.
- Five-lens evaluation is implementable without the full stack.
- M10 (knowledge commons) maps to existing SurrealDB graph schema.
- No dependency on Integral CDS, COS, ITC, or FRS in Phase 1.

#### Negative

- No ITC incentive system — design contribution relies on voluntary engagement.
- No material coefficient database — ecological scoring uses approximations during Phase 1.
- No CDS — certification thresholds are set ad hoc until constitutional rules exist.
- Offline operation is limited to locally computable analysis.

#### Risks

- Community may attempt full OAD adoption, hitting the 4 blocking constraints.
- Without formal governance, "who decides certification thresholds" will recur.
- Voluntary engagement model may not sustain sustained design contribution.

### References

- Peter Joseph, Revolution Now Ep 60: Integral OAD — integralcollective.io
- OAD 10 Modules: M1 intake, M2 workspace, M3–M7 five-lens analysis, M8 optimization, M9 certification, M10 commons
