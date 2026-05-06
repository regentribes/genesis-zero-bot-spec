---
name: wiki-maintainer
description: Maintain the OpenClaw memory wiki vault with zero-bloat, zero-duplication storage architecture. Stores any document type at trillion scale.
---

Use this skill when working inside a memory-wiki vault.

## Architecture (First Principles)

**Core invariant: one document, one canonical location. Zero duplication.**

```
wiki vault/
├── adrs/           # Content layer: ADR files render as native GitHub Markdown
│   ├── 0000-*.md   ← GitHub renders these perfectly
│   └── ...
├── concepts/       # Claims layer: metadata + claims only
│   ├── adr-*.md    ← sourceIds → adrs/, links to adrs/ for full content
│   └── *.md
├── sources/        # Reference layer: lightweight index shells
│   ├── index.md
│   └── NNNN-*.md   ← canonicalPath + URL only, no content
└── entities/       # Entity pages
    ├── genesis.md
    └── regen-tribes-community.md
```

**Why this design:**
- `adrs/` files render on GitHub without code fences (proper headers, links, code blocks)
- `sources/` = metadata index. No content duplication.
- `concepts/` = claims + relationships. Links to `adrs/` for full content.
- Adding a document = one file in `adrs/`. Not two (content + wrapper). Not three (+source +concept).
- Scales to trillions: O(1) per document, no compounding complexity.

## Workflow

### Default Maintenance Loop

```text
openclaw wiki compile
openclaw wiki lint      # Must reach 0 issues
rumdl check docs/adr/   # Markdown style check
python3 skills/wiki-maintainer/tools/ste_audit.py   # ASD-STE100 audit
```

### ADR Lifecycle

```
1. Draft   → create docs/adr/XXXX-title.md in workspace repo
2. Stealth → copy to ~/.openclaw/wiki/main/adrs/XXXX-title.md
3. Index   → create sources/XXXX-title.md (metadata shell, 5 lines frontmatter)
4. Claims  → create concepts/adr-XXXX-title.md (claims + relationships)
5. Compile → openclaw wiki compile && wiki lint
6. Sync    → push wiki vault to GitHub + Radicle
7. Publish → push workspace docs/adr/ to GitHub
```

**The workflow creates ONE content file in `adrs/` plus TWO metadata shells.**
No content duplication. The ADR is the canonical file.

### ADR Creation Step-by-Step

**Step 1 — Write ADR in workspace repo (ASD-STE100, ≤20 words/sentence):**
```bash
cd ~/.openclaw/workspace-genesis
# Write docs/adr/XXXX-title.md using MADR format
# ASD-STE100: active voice, simple vocabulary, ≤20 words/sentence
```

**Step 2 — Copy to wiki vault adrs/ (the canonical content location):**
```bash
cp docs/adr/XXXX-title.md ~/.openclaw/wiki/main/adrs/
```

**Step 3 — Create metadata shell in sources/ (5 lines frontmatter + link):**
```bash
# sources/XXXX-title.md template:
cat > sources/XXXX-title.md << 'EOF'
---
id: source.XXXX-title-slug
pageType: source
title: ADR XXXX — Title
canonicalPath: adrs/XXXX-title.md
canonicalUrl: https://github.com/regentribes/genesis-zero-bot/blob/main/docs/adr/XXXX-title.md
sourceType: architecture-decision-record
entityType: source
confidence: 1.0
updatedAt: YYYY-MM-DD
tags:
  - adr
  - architecture
provenance:
  - source: workspace-docs
    path: docs/adr/XXXX-title.md
    weight: 1.0
sourceIds: []
relatedConcepts:
  - concept.adr-XXXX-title-slug
---

# ADR XXXX — Title

**Canonical location:** [[adrs/XXXX-title.md|View ADR in vault]] · [GitHub](canonicalUrl)

<!-- openclaw:wiki:related:start -->
<!-- openclaw:wiki:related:end -->
EOF
```

**Step 4 — Create concept page in concepts/ (claims + relationships only):**
```bash
# concepts/adr-XXXX-title.md template:
cat > concepts/adr-XXXX-title.md << 'EOF'
---
id: concept.adr-XXXX-title-slug
pageType: concept
entityType: concept
title: ADR XXXX — Title
status: proposed|accepted
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
  - source.XXXX-title-slug
claims:
  - id: claim.adr-XXXX.key-claim
    text: "<key decision claim>"
    status: supported
    confidence: 1.0
    evidence:
      - kind: source-doc
        sourceId: source.XXXX-title-slug
        privacyTier: public
relatedConcepts:
  - concept.adr-0000-oad-workflow-grammar
  - concept.ame-metonymic-activation
relatedSources:
  - source.XXXX-title-slug
---

# ADR XXXX — Title

**Status:** proposed|accepted  
**Date:** YYYY-MM-DD  
**Full document:** [[adrs/XXXX-title.md|View ADR]]  
**Source:** [[sources/XXXX-title-slug|Source page]]

## Key Decision

<key decision text in plain language>

## See Also

- [[adrs/XXXX-title.md|ADR XXXX — Full Document]]
- [[concepts/adr-0000-oad-workflow-grammar|ADR 0000 — OAD Workflow Grammar]]

## References

- [[adrs/XXXX-title.md|ADR XXXX — Title]]
- [GitHub](https://github.com/regentribes/genesis-zero-bot/blob/main/docs/adr/XXXX-title.md)
EOF
```

**Step 5 — Validate and push:**
```bash
# Wiki vault (GitHub mirror + Radicle)
cd ~/.openclaw/wiki/main
git add . && git commit -m "ADR XXXX: title" && git push origin main && git push rad main

# Workspace repo (canonical ADR source)
cd ~/.openclaw/workspace-genesis
git add docs/adr/XXXX-title.md && git commit -m "ADR XXXX: title"
git push origin main  # or: git push https://x-access-token:$(gh auth token)@github.com/regentribes/genesis-zero-bot.git main
```

## STE100 Enforcement

ASD-STE100 writing style is mandatory. All content must pass ste_detect.py.

**Detection rules:**
- Unapproved words — compared against `ASD-STE100/logic/asd_rules.json` (3689 words, 1793 approved)
- Long sentences — >20 words flagged
- Passive voice — `(is|are|was|were|be|been|being).*\w+ed`

**STE audit commands:**
```bash
# Full vault
python3 skills/wiki-maintainer/tools/ste_audit.py

# Single file
cat docs/adr/XXXX.md | python3 skills/wiki-maintainer/tools/ste_detect.py

# After any content change
rumdl check docs/adr/   # Must be 0 issues
openclaw wiki lint       # Must be 0 issues
```

## Wiki Storage: Complete Guide

### What goes where

| Document type | Storage location | Wikilink target | Renders on GitHub |
|---|---|---|---|
| ADR (canonical content) | `adrs/` | `[[adrs/XXXX-title]]` | ✅ Yes |
| Source metadata | `sources/` | `[[sources/XXXX-title]]` | ✅ Yes (metadata only) |
| Claims + relationships | `concepts/` | `[[concepts/adr-XXXX]]` | ✅ Yes |
| Entity | `entities/` | `[[entities/name]]` | ✅ Yes |

### Wikilink conventions

```
[[adrs/0000-filename|View ADR]]        ← full ADR content (renders as proper Markdown)
[[sources/0000-filename|Source]]      ← metadata index shell (canonicalPath + URL)
[[concepts/adr-0000|Concept]]          ← claims + relationships
[[entities/genesis|Genesis]]           ← entity page
```

### Cross-reference rules

- **Concept page** links to: `[[adrs/XXXX|View ADR]]` + `[[sources/XXXX|Source]]`
- **Source page** links to: `[[adrs/XXXX|View ADR]]` + `[[concepts/adr-XXXX|Concept]]`
- **ADR page** links to: other ADRs via `[[adrs/XXXX|ADR Title]]` or GitHub URLs
- **No nesting** — content lives in `adrs/`, never wrapped inside another file

### Why no code fences in sources/

The old `openclaw wiki ingest` wraps content in triple-backticks. This destroys GitHub Markdown rendering (headers become plain text). We bypass it for Markdown files.

For binary files (PDFs, spreadsheets, images):
- Use `openclaw wiki ingest` for non-Markdown files
- These get wrapped in code fences, which is correct for non-text assets

For Markdown files:
- Copy directly to `adrs/`. No code fences. Perfect rendering.

## Tool Inventory

| Tool | Purpose | Location |
|------|---------|----------|
| `rumdl` | Markdown linter (MD013/025/032 disabled) | `~/.local/bin/rumdl` |
| `ste_detect.py` | Per-sentence STE check | `skills/wiki-maintainer/tools/` |
| `ste_audit.py` | Full vault STE audit | `skills/wiki-maintainer/tools/` |
| `openclaw wiki compile` | Rebuild agent-digest.json | OpenClaw CLI |
| `openclaw wiki lint` | Validate wikilinks | OpenClaw CLI |
| `gh` | GitHub API + push | System (`/usr/bin/gh`) |

## Wiki Vault URLs

- **GitHub (wiki vault):** https://github.com/genesis-zero-bot/genesis-zero-bot-wiki
- **GitHub Pages:** https://genesis-zero-bot.github.io/genesis-zero-bot-wiki/
- **Radicle RID:** `rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X`
- **Radicle web:** https://app.radicle.xyz/nodes/rosa.radicle.xyz/rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X

## Wiki Maintenance Rules

- **Zero duplication:** content lives in `adrs/` only. Sources/ and concepts/ are metadata.
- **ASD-STE100:** all content files. No marketing language. No corporate speak. No academic filler.
- **Trillion-proof:** O(1) per document. No per-document overhead compounding.
- **GitHub-native rendering:** all content files must render on GitHub without code fences.
- **Managed blocks:** keep generated sections inside `<!-- openclaw:wiki:*:start -->` / `<!-- openclaw:wiki:*:end -->`.
- **Human notes:** keep `<!-- openclaw:human:start -->` / `<!-- openclaw:human:end -->` blocks intact.
- **Stable page identity:** do not rename pages after creation. Update frontmatter instead.
- **wikilinks:** use bare slugs. `[[adrs/0000-title]]`, not `[[sources/0000-title|View]]` for the full content link.

## Radicle Sync Validation

```bash
export PATH="$HOME/.radicle/bin:$PATH"
rad node routing | grep zYhRVEu5Zh85vcwvmxkZHJNQxn6X
rad seed rad:zYhRVEu5Zh85vcwvmxkZHJNQxn6X --scope all
```

---

*Last updated: 2026-05-06 · Architecture v2 (zero-bloat, zero-duplication)*
