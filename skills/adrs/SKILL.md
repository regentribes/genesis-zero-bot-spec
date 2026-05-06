---
name: adrs
description: Create, navigate, and manage Architecture Decision Records (ADRs) for RegenTribes. Use when asked to make an architecture decision, evaluate tradeoffs between technical approaches, file an ADR, or analyze design options. Wraps the adrs CLI tool (joshrotenberg/adrs).
metadata:
  requires:
    bins:
      - adrs
  triggers:
    - "make an architecture decision"
    - "file an ADR"
    - "architecture decision"
    - "ADR"
    - "tradeoff analysis"
    - "evaluate design options"
    - "decision record"
---

# ADRs — Architecture Decision Records Skill

Create, navigate, and manage Architecture Decision Records using the MADR 4.0.0 format.

## Quick Reference

### ADR Format (MADR 4.0.0)

```markdown
---
title: Decision Title
number: NNNN
status: proposed|accepted|deprecated|superseded
date: YYYY-MM-DD
authors: Genesis
domain: information|physical|social|exchange
level: cell|tissue|organ|system|body
tags:
  - tag-1
  - tag-2
---

# Title

## Context
[What is the situation? What prompted this decision?]

## Decision
[What was decided?]

## Options Considered
| Option | Description | Verdict |
|--------|-------------|---------|
| A | ... | adopted |
| B | ... | rejected |
| C | ... | deferred |

## Analysis
[Why this decision over alternatives. Be thorough — surface conflicts, edge conditions, blocking constraints.]

## Consequences
### Positive
### Negative
### Risks

## References
[Links, sources, related ADRs]
```

### Status Values

| Status | Meaning |
|--------|---------|
| `proposed` | Under review, not yet accepted |
| `accepted` | Decided and being implemented |
| `deprecated` | Superseded or no longer relevant |
| `superseded` | Replaced by a newer ADR |

### Domain Values

- `information` — knowledge, sensing, memory systems
- `physical` — materials, construction, hardware
- `social` — relationships, governance, decisions
- `exchange` — value flow, trade, resources

### Level Values

- `cell` — smallest unit (individual, single tool, one sensor)
- `tissue` — small group (3–12 people, core team)
- `organ` — neighborhood (12–200 people, local infrastructure)
- `system` — bioregion (multiple neighborhoods, federation)
- `body` — planetary (all bioregions, global standards)

## Storage

RegenTribes ADRs: `~/.openclaw/workspace-genesis/docs/adr/`

ADR naming convention: `NNNN-title-slug.md` (zero-padded 4-digit number).

### ADR ↔ Wiki Vault Bridge

The ADRs live in **GitHub** (`docs/adr/`). The wiki vault lives in **Radicle** (`~/.openclaw/wiki/main/`). They are kept in sync via a dual-write pattern.

**When filing a new ADR, also create wiki pages:**

```bash
# 1. Write ADR to GitHub
docs/adr/000X-title.md

# 2. Write source page to wiki vault
~/.openclaw/wiki/main/sources/adr-000X-{slug}.md

# 3. Write concept page to wiki vault
~/.openclaw/wiki/main/concepts/adr-000X-{slug}.md

# 4. Compile + lint wiki
openclaw wiki compile && openclaw wiki lint

# 5. Commit & push both repos
git add docs/adr/ && git commit -m "ADR 000X: title"
git push origin main

cd ~/.openclaw/wiki/main
git add . && git commit -m "ADR 000X: title"
git push rad main
```

**GitHub Actions (future automation):** Radicle push requires SSH key setup. Until then, manual dual-write.

**Public URL on iris node:**
- Wiki vault RID: `rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X`
- View: https://radicle.xyz/nodes/radicle.xyz/trees/rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X

**adrs CLI is NOT integrated with the wiki vault.** They are separate tools:
- `adrs` CLI → ADR files in `docs/adr/` (GitHub repo)
- `memory-wiki` → compiled knowledge graph in `~/.openclaw/wiki/main/` (Radicle repo)
- ADRs are source documents in the wiki, not wiki-managed entities

### Per-ADR Wiki Schema

Each ADR gets two wiki pages:

**Source page** (`sources/adr-000X-{slug}.md`):
```yaml
---
id: source.adr-000X-{slug}
pageType: source
title: ADR 000X — Title
date: YYYY-MM-DD
authors: Genesis
sourceType: architecture-decision-record
entityType: source
confidence: 1.0
updatedAt: YYYY-MM-DD
tags:
  - adr
  - architecture
provenance:
  - source: source.github-regen-tribes
    path: docs/adr/000X-title-slug.md
    lines: "1-999"
    weight: 1.0
---
```

**Concept page** (`concepts/adr-000X-{slug}.md`):
```yaml
---
id: concept.adr-000X-{slug}
pageType: concept
entityType: concept
title: ADR 000X — Title
status: accepted
date: YYYY-MM-DD
authors: Genesis
domain: information
level: system
confidence: 1.0
updatedAt: YYYY-MM-DD
tags:
  - adr
  - architecture
sourceIds:
  - source.adr-000X-{slug}
claims:
  - id: claim.adr-000X.decision
    text: "<key claim from ADR>"
    status: supported
    confidence: 1.0
    evidence:
      - kind: source-doc
        sourceId: source.adr-000X-{slug}
        privacyTier: public
relatedConcepts:
  - concept/karpathy-llm-wiki
  - concept/memory-wiki
---
```

## Common Workflows

### 1. Evaluate Options and File an ADR

When a request involves choosing between technical approaches:

1. List context — what are the options, what are the constraints?
2. Identify blocking constraints — what makes each option impossible or sub-optimal?
3. Drive conflicts to extremes — surface edge conditions, failure modes
4. Write ADR in MADR format with all options, analysis, and consequences
5. Commit to `docs/adr/` and push to origin
6. Dual-write source + concept pages to wiki vault and push to Radicle

### 2. Tradeoff Analysis Pattern

```
Context → Options (min 3) → Analysis → Consequences → Decision → Phase plan
```

Always:
- Lead with the actual options (not strawmen)
- State blocking constraints explicitly
- Include phase-gated path when full adoption is premature
- Note what is deferred and why
- Identify risks, not just benefits

### 3. Multi-ADRs for Related Decisions

When one decision involves two distinct subjects (e.g., OAD vs. hosted alternatives), split into separate ADRs. Keep each ADR focused on one decision.

### 4. Linked ADRs

Use the `References` section to link related ADRs. Use `Supersedes` / `Superseded by` to track evolution of a decision over time.

## CLI Reference

```bash
cd ~/.openclaw/workspace-genesis/skills/adrs
./adrs list                          # List all ADRs (requires .adr-dir)
./adrs search "keyword"             # Search ADR content
./adrs new "Title" --format madr    # Create new ADR (interactive, TTY required)
```

For automated ADR creation: write the Markdown file directly to `docs/adr/`.

## Skill Usage Examples

**"Evaluate Bonfires.ai vs llm_wiki vs memory-wiki"**
→ File ADR 0001 on agent knowledge systems. Structure: context → 3 options → analysis → consequences → decision. Then dual-write wiki pages.

**"Should we adopt the full OAD or just the workflow grammar?"**
→ File ADR 0000 on OAD phase-gated adoption. Structure: context → blocking constraints → phase plan. Then dual-write wiki pages.

**"We need to decide on our sync strategy for offline operation"**
→ File ADR. Structure: context → options (Syncthing, Radicle, custom) → analysis → consequences. Then dual-write wiki pages.

## Constraints

- `adrs` CLI requires interactive terminal — use for `list` and `search` only in interactive sessions
- For automated/subagent use: write Markdown directly to `docs/adr/`
- All ADRs must be committed and pushed to origin for persistence
- Use MADR 4.0.0 format for machine-readable metadata
- Zero-padded 4-digit numbers: 0000, 0001, 0002, etc.
- Every ADR requires dual-write: GitHub + Radicle wiki vault

## References

- Wiki vault RID: `rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X`
- MADR format: adr.github.io/madr/
- adrs CLI: github.com/joshrotenberg/adrs
- Original Nygard ADR article: thinkrelevance.com/blog/documenting-architecture-decisions
