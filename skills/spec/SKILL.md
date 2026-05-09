---
name: spec
description: |
  Transform arbitrary information into Gherkin .feature files (living specifications)
  for the genesis-zero-bot-spec repository. Validates with ghokin before every commit.
  Always reply with direct link to deployed page after push.
triggers:
  - "gherkin"
  - "spec"
  - "feature file"
  - "living specification"
  - "bdd"
  - "scenario"
  - "create a spec"
---

Use this skill when creating or updating Gherkin specifications in the `genesis-zero-bot-spec` repository.

## Spec Repository URLs

| Service | URL |
|---------|-----|
| GitHub repo | https://github.com/regentribes/genesis-zero-bot-spec |
| GitHub Pages (root) | https://regentribes.github.io/genesis-zero-bot-spec/ |

## Repository Structure

```
genesis-zero-bot-spec/
├── docs/           ← .feature files (one per system/behavior)
├── assets/         ← CSS (pure B/W minimal, aligned with wiki + ADR + arch)
├── build.py        ← generates _site/ with syntax-highlighted Gherkin HTML
├── _config.yml     ← GitHub Pages config
└── .github/workflows/pages.yml
```

## Four-Output Pipeline

This skill produces the **spec** output. The other three outputs are managed by separate skills:

| Output | Repo | Skill | URL pattern |
|--------|------|-------|-------------|
| Wiki | `genesis-zero-bot-wiki` | `wiki` | `sources/NNNN-slug.html` |
| ADRs | `genesis-zero-bot-adrs` | `adrs` | `adr-NNNN.html` |
| Specs | `genesis-zero-bot-spec` | `spec` | `feature-*-slug.html` |
| Archi | `genesis-zero-bot-arch` | `arch` | `html/index.html` |

All four repos share the same pure B/W minimal visual style.

## Visual Style (Aligned Across All Four Repos)

All four repos share the same pure B/W minimal style:
- Dark: pure black `#000000` bg, white `#ffffff` heading, gray `#888888` text
- Light: white `#ffffff` bg, black `#000000` heading, dark gray `#333333` text
- System font stack, 17px base, 860px max content width
- `var(--border)` = `#222222` dark / `#e0e0e0` light
- Dark theme default, localStorage persistence, `🌙` toggle

CSS is identical across all four repos. When editing CSS, update all four.

## Adding a New Feature (.feature file)

### Step 1 — Clone the spec repo (if not already cloned)

```bash
cd /tmp
git clone https://github.com/regentribes/genesis-zero-bot-spec.git --depth 1
```

### Step 2 — Create the file

Write to `docs/NNN-feature-name.feature`. Use 3-digit prefix.

**Feature template:**
```gherkin
Feature: [What the system does]

  As a [who benefits]
  I want [what it does]
  So that [why it matters]

  Background:
    Given [shared context]

  Scenario: [behavior name]
    Given [precondition]
    When [action]
    Then [observable outcome]
    And [additional outcome]
```

### Step 3 — Validate with ghokin (mandatory before commit)

```bash
cd /tmp/genesis-zero-bot-spec

# Check format
/tmp/ghokin check docs/NNN-feature-name.feature

# Auto-fix formatting
/tmp/ghokin fmt replace docs/NNN-feature-name.feature

# Re-check after fix
/tmp/ghokin check docs/NNN-feature-name.feature
# Must show: "is well formatted"
```

### Step 4 — Build and verify HTML

```bash
cd /tmp/genesis-zero-bot-spec
python3 build.py
# Check _site/feature-*.html renders correctly
```

### Step 5 — Commit and push

```bash
cd /tmp/genesis-zero-bot-spec
git add docs/NNN-feature-name.feature
git commit -m "spec(NNN): feature name"
git push origin main
```

### Step 6 — Check GitHub Pages deployment

```bash
gh run list --repo regentribes/genesis-zero-bot-spec --limit 3
```

If successful, the spec is live at:
```
https://regentribes.github.io/genesis-zero-bot-spec/
```

**Always reply with the direct deployed link when the task is complete.**

## Key Rules (automationpanda/gherkin-guidelines-for-ai)

- One behavior per scenario, < 10 steps
- Given = Arrange precondition, When = Act, Then = Assert outcome
- Third person, present tense, subject-predicate
- Domain-level abstraction — no UI/API/DB plumbing in step text
- State over navigation
- Observable `Then` outcomes — not "it works"
- Concrete realistic example data
- Scenario Outline only for genuine input variations

## Validation Gate (Iterative)

1. `ghokin fmt replace` — normalize (2-space indent, keyword casing, blank lines)
2. `ghokin check` — validate Gherkin structure, exit 0 = pass
3. If fail: auto-fix common issues → re-check
4. Repeat up to 3 iterations
5. Only publish after clean pass

## Tool Inventory

| Command | Purpose |
|---------|---------|
| `/tmp/ghokin check <file>` | Validate Gherkin structure |
| `/tmp/ghokin fmt replace <file>` | Auto-fix formatting |
| `python3 build.py` (in spec repo) | Build HTML site from .feature files |
| `gh run list --repo regentribes/genesis-zero-bot-spec --limit 3` | Check Pages deployment |

## CSS Alignment Notes

When editing CSS or HTML templates:
- Wiki CSS: `~/.openclaw/wiki/main/assets/main.css`
- ADR CSS: `/tmp/genesis-zero-bot-adrs/assets/style.css` (cloned repo)
- Spec CSS: `/tmp/genesis-zero-bot-spec/assets/style.css`
- Arch CSS: `/tmp/genesis-zero-bot-arch/assets/style.css`

All four share the same CSS variable scheme. Changes to one should propagate to all.

---

*Last updated: 2026-05-08 · spec v2 (short-name form, aligned to wiki)*