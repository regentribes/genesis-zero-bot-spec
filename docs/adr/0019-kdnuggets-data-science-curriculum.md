# ADR 0017: Adopt KDnuggets Cheat Sheet Collection as Community Learning Reference

**Date:** 2026-05-08  
**Status:** Proposed  
**Deciders:** RegenTribe / Integral Collective  

---

## Context

RegenTribe is building practical data science competency across community members working on the Farmers IoT Toolkit and neighbourhood-scale regenerative systems. Members need structured, accessible reference material for technical interviews, assessment prep, and ongoing skill development across SQL, ML, data engineering, and related domains.

KDnuggets published a curated collection of 100+ data science cheat sheets (March 2022) covering 12 categories. We must decide whether and how to adopt this as a community learning resource.

---

## Decision

**Adopt the KDnuggets cheat sheet collection as a supplementary community learning reference**, integrated into the existing NVIDIA certification learning pathway.

---

## Options

### Option 1: Full 12-Category Adoption *(chosen)*

Adopt all 12 categories and the VIP bonus as community reference material.

**Pros:**
- Comprehensive coverage across all data science domains
- Supports multiple learning pathways (Python, R, Julia)
- Low cost (free resource)
- Matches NVIDIA certification curriculum structure

**Cons:**
- 100+ sheets is overwhelming without curation
- Some URLs may be stale (2022 publication)
- No single authoritative source — sheets linked from various authors/locations

### Option 2: Selective Adoption (ML + NLP + Data Engineering Only)

Adopt only 3 of 12 categories most relevant to the IoT Toolkit and community metrics work.

**Pros:**
- Focused, less overwhelming
- Directly maps to active community projects

**Cons:**
- Excludes SQL, Statistics, Big Data — foundational skills the community may need
- Requires judgment calls about what's "relevant" that may exclude curious members

### Option 3: Curated Subset Only

Maintain a hand-picked list of 15-20 "best in class" sheets per category, curated by an assigned curriculum owner.

**Pros:**
- Quality-controlled, not overwhelming
- Stale URLs managed by a responsible party

**Cons:**
- Creates maintenance burden and single-point-of-failure governance
- Limits discovery — members can't browse freely

---

## Consequences

### If Option 1 is adopted:

- A `data-science-learning/` directory will be added to the wiki with the collection as a top-level source
- Members are encouraged to use the collection alongside NVIDIA certifications
- A lightweight "cheat sheet tracker" (Gherkin spec in `docs/011-data-science-learning-progress.feature`) will track individual progress
- Wiki will link individual sheets to their canonical URLs; a curator will audit URLs quarterly

### Risks:

- **Stale links:** URLs will drift. Mitigation: audit + update quarterly.
- **Information overload:** Without guidance, members may not know where to start. Mitigation: pair with NVIDIA cert roadmap.

---

## Notes

- The KDnuggets collection PDF itself is a catalog, not the cheat sheet content. Individual sheets live at external URLs.
- Julia is positioned as a future-forward language in the collection — particularly relevant for high-performance computing on edge hardware (Raspberry Pi, HP nodes).
- RegenNeighbourhood applications: community metrics (SQL/BI), sensor pipelines (Data Engineering/Big Data), predictive maintenance (ML), governance communication (NLP).

---

## Wiki Provenance

**Wiki source:** [[sources/0019-kdnuggets-data-science-cheatsheets|Sources/0019 — KDnuggets Data Science Cheat Sheets]] (ingested 2026-05-08)
**Wiki concepts:** [[concepts/0018-nvidia-learning-paths-2026|NVIDIA Learning Paths for AI Skills Development]]
**Spec cross-reference:** `feature-010` (AI Skills Verification) — NVIDIA certification alignment
**Spec cross-reference:** `feature-011` (Data Science Learning Progress) — KDnuggets curriculum integration

---

*Written in ASD-STE100 simplified technical English.*
