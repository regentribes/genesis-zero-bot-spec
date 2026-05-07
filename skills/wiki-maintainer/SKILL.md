---
name: wiki-maintainer
description: Maintain the OpenClaw memory wiki vault. Zero-bloat, zero-duplication. Sources are canonical. GitHub Pages renders every page.
---

Use this skill when working inside the OpenClaw memory wiki vault at `~/.openclaw/wiki/main/`.

## ACTUAL Vault Architecture

**This is the canonical structure. Do not follow any other description.**

```
wiki vault/                              ← ~/.openclaw/wiki/main/
├── sources/        ← CANONICAL CONTENT (this is where content lives)
│   ├── NNNN-*.md   ← raw content, full text, with frontmatter
│   └── index.md
├── concepts/       ← CLAIMS + RELATIONSHIPS only (metadata, links to sources/)
│   ├── *.md
│   └── index.md
├── entities/       ← People and organizations
│   ├── *.md
│   └── index.md
├── syntheses/      ← Auto-generated reports
├── reports/        ← Auto-generated diagnostics (lint, stale, provenance)
├── index.md        ← Master catalog
└── manifest.json   ← Machine-readable index (regenerated after each operation)
```

**Critical rule: `sources/` is canonical. One document lives in one file in `sources/`.**
- `concepts/` pages have frontmatter + claims + wikilinks to `sources/` — they do NOT duplicate content
- `entities/` pages have frontmatter + description — they do NOT duplicate content
- GitHub Pages renders every file from `sources/` directly (no code fences)

## What Goes Where

| Document type | Canonical location | Wikilink target | Renders on GitHub |
|---|---|---|---|
| Raw content (Telegram export, ADR synthesis, any long-form) | `sources/NNNN-*.md` | `[[sources/NNNN-title]]` | ✅ Full content |
| Claims + relationships | `concepts/NAME.md` | `[[concepts/NAME]]` | ✅ Claims + links |
| Person or org | `entities/NAME.md` | `[[entities/NAME]]` | ✅ Description |

## Wikilink Conventions

All wikilinks MUST include the directory prefix (required for lint engine to resolve):
```
[[sources/0008-topic-57-mst-polcompball-egafutura|Topic 57 — Governance Spec]]
[[concepts/adr-0000-oad-workflow-grammar|ADR 0000 — OAD Workflow Grammar]]
[[entities/genesis|Genesis 🌿⚡]]
[[entities/regen-tribes-community|RegenTribes Community]]
```

Never use bare slugs without directory prefix.

## Guaranteed Zero-Lint Workflow

**After EVERY wiki operation, run all three checks in order:**

```bash
cd ~/.openclaw/wiki/main

# 1. Compile (rebuild agent digest + indexes)
openclaw wiki compile

# 2. Lint (validate wikilinks — MUST be 0 issues)
openclaw wiki lint

# 3. Style check
~/.local/bin/rumdl check .     # 0 issues required
```

If lint reports issues, the report tells you exactly which file and which wikilink is broken. Fix the target file to exist, or fix the wikilink to match the target filename exactly.

## Adding a New Document

**Step 1 — Create canonical content in `sources/` with proper frontmatter:**
```bash
# Frontmatter template for sources/:
cat > sources/NNNN-title-slug.md << 'EOF'
---
id: source.title-slug
pageType: source
title: "Descriptive Title Here"
canonicalPath: sources/NNNN-title-slug.md
sourceType: telegram-export-synthesis|adr|article|notes
entityType: source
confidence: 0.8
updatedAt: "YYYY-MM-DD"
provenance:
  - source: telegram-export|workspace|web
    extractedBy: kreuzberg|genesis|human
    privacyTier: public
tags:
  - tag1
  - tag2
sourceIds: []
relatedConcepts: []
---

# Title Here

Content goes here. No code fences for Markdown content.
EOF
```

**Step 2 — Create concept page in `concepts/` with claims:**
```bash
cat > concepts/title-slug.md << 'EOF'
---
id: concept.title-slug
pageType: concept
entityType: concept
title: "Descriptive Title"
status: active
date: "YYYY-MM-DD"
authors: Genesis
domain: dao-governance
level: system
confidence: 0.8
updatedAt: "YYYY-MM-DD"
tags:
  - tag1
sourceIds:
  - source.title-slug
claims:
  - id: claim.001
    text: "Key finding or decision"
    status: supported
    confidence: 0.8
    evidence:
      - kind: source-doc
        sourceId: source.title-slug
        privacyTier: public
relatedConcepts:
  - concept.other-concept
relatedSources:
  - source.title-slug
---

# Descriptive Title

**Status:** active  
**Date:** YYYY-MM-DD  
**Source:** [[sources/NNNN-title-slug|View source]]

## Key Claims

- Claim 1
- Claim 2

## See Also

- [[sources/NNNN-title-slug|Source — Full content]]
- [[concepts/other-concept|Other Concept]]
EOF
```

**Step 3 — Run the three checks:**
```bash
openclaw wiki compile && openclaw wiki lint && ~/.local/bin/rumdl check .
```

**Step 4 — Commit and push:**
```bash
cd ~/.openclaw/wiki/main
git add sources/NNNN-title-slug.md concepts/title-slug.md
git commit -m "docs(topic-NN): add title slug"
git push origin main
```

## GitHub Pages Rendering

GitHub Pages builds from the vault on every push via `.github/workflows/pages.yml`.

**The rendering pipeline:**
1. GitHub Actions checks out the vault
2. Python step converts wikilinks: `[[sources/file|Display]]` → `[Display](sources/file.html)`
3. Python step strips YAML frontmatter `---...---` (required for clean rendering)
4. Jekyll builds with kramdown + GFM
5. GitHub Pages serves the `_site/` directory

**Frontmatter rule:** Every `.md` file MUST have `---` frontmatter. The build step strips it. Without frontmatter, GitHub Pages does not know the file is a page.

## Tool Inventory

| Command | Purpose |
|---------|---------|
| `openclaw wiki compile` | Rebuild agent-digest.json and all indexes |
| `openclaw wiki lint` | Validate all wikilinks (0 issues = success) |
| `openclaw wiki ingest <file>` | Extract content from binary/non-Markdown files |
| `~/.local/bin/rumdl check .` | Markdown style (MD013/025/032 disabled) |
| `python3 skills/wiki-maintainer/tools/ste_audit.py` | ASD-STE100 full vault audit |
| `gh run list --repo genesis-zero-bot/genesis-zero-bot-wiki` | Check GitHub Pages build status |

## Wiki Vault URLs

| Service | URL |
|---------|-----|
| GitHub repo | https://github.com/genesis-zero-bot/genesis-zero-bot-wiki |
| GitHub Pages | https://genesis-zero-bot.github.io/genesis-zero-bot-wiki/ |
| Radicle RID | `rad:zYhRVEu5Zh85vcwvmxkZHJNQqn6X` |
| Radicle web | https://app.radicle.xyz/nodes/rosa.radicle.xyz/rad:zYhRVEu5Zh85vcwvmxkZHJNQqn6X |

## Maintenance Rules

- **One canonical location:** content goes in `sources/`, never duplicated
- **Directory prefix in wikilinks:** always `[[sources/...]]` or `[[concepts/...]]`
- **Frontmatter required:** every page needs `id`, `pageType`, `title`, `status`
- **ASD-STE100:** active voice, ≤20 words/sentence, no passive
- **Managed blocks:** preserve `<!-- openclaw:wiki:*:start -->` / `<!-- openclaw:wiki:*:end -->`
- **After any change:** compile → lint → rumdl (all three, in order)
- **manifest.json:** auto-generated, do not edit manually

## Radicle Sync

```bash
export PATH="$HOME/.radicle/bin:$PATH"
rad node routing | grep zYhRVEu5Zh85vcwvmxkZHJNQqn6X
rad seed rad:zYhRVEu5Zh85vcwvmxkZHJNQqn6X --scope all
```

---

*Last updated: 2026-05-07 · Architecture v3 (sources/ canonical, GitHub Pages active)*
