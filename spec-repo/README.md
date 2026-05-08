# Genesis Gherkin Specs

Living specification documents for RegenTribes systems, written in Gherkin (BDD) format with ghokin validation gates.

## What This Is

Gherkin specs translate raw knowledge (wiki sources, ADRs, research syntheses) into executable specifications:
- One behavior per scenario
- Given/When/Then as Arrange/Act/Assert
- Validated with ghokin before every commit

## Repo Structure

```
genesis-zero-bot-spec/
├── docs/           ← .feature files (one per system)
├── assets/         ← CSS (pure B/W minimal, aligned with wiki + ADR)
├── build.py        ← generates _site/ with syntax-highlighted Gherkin
├── _config.yml     ← GitHub Pages config
└── .github/workflows/pages.yml
```

## Build & Deploy

Push to main → GitHub Actions runs build.py → syntax-highlighted HTML to _site/ → GitHub Pages at:
```
https://regentribes.github.io/genesis-zero-bot-spec/
```

## Style

Aligned with wiki-zero-bot and adrs-zero-bot:
- Pure black/white theme, dark default
- Same typography (system sans-serif, 17px base)
- Same border/bg color tokens
- Prism.js for Gherkin syntax highlighting

## Validation Gate

Every feature file passes through:
1. `ghokin fmt replace` — 2-space indent, keyword casing
2. `ghokin check` — exit 0 = valid Gherkin
3. Auto-fix on failure, repeat up to 3 iterations
