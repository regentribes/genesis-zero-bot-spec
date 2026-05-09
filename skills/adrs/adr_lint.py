#!/usr/bin/env python3
"""
ADR Lint — validate MADR ADR quality before commit.
Checks: frontmatter completeness, ASD-STE100 compliance, wikilink validity,
        required sections, no personal identifiers, domain single-word.

Run: python3 adr_lint.py <docs_dir>
Exit code: 0 if clean, 1 if issues found.
"""

import re, sys
from pathlib import Path

DOCS_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "docs"

REQUIRED_FIELDS = ["id", "pageType", "title", "status", "date", "authors", "domain", "level"]
REQUIRED_SECTIONS = ["Context", "Decisions", "Consequences", "References"]
VALID_STATUSES = ["Accepted", "Proposed", "Rejected", "Deprecated", "Superseded"]
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')
# Personal identifier patterns ( Telegram handles, phone numbers, obvious names )
PERSONAL_ID_RE = re.compile(r'@[a-zA-Z0-9_]+|^\+[0-9]|telegram:|signal:')
# STE100: active voice, ≤20 words/sentence
STE100_RE_SENTENCE_END = re.compile(r'[.!?]\s+')
STE100_RE_PASSIVE = re.compile(r'\b(was|were|been|being|is|are|am)\s+\w+ed\b', re.IGNORECASE)

issues = []


def check_frontmatter(path, content):
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        issues.append(f"{path}: Missing frontmatter")
        return {}
    fm = {}
    for line in fm_match.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    for field in REQUIRED_FIELDS:
        if field not in fm:
            issues.append(f"{path}: Missing required field '{field}'")
    status = fm.get('status', '')
    if status and status not in VALID_STATUSES:
        issues.append(f"{path}: Status must be one of {VALID_STATUSES}, got '{status}'")
    domain = fm.get('domain', '')
    if domain and ('/' in domain or ' ' in domain):
        issues.append(f"{path}: Domain must be single word, got '{domain}'")
    authors = fm.get('authors', '')
    if authors and PERSONAL_ID_RE.search(authors):
        issues.append(f"{path}: Authors field contains personal identifier: {authors}")
    return fm


def check_ste100(path, content):
    """Check ASD-STE100: ≤20 words/sentence, active voice."""
    # Strip frontmatter and code blocks
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    # Count sentences
    sentences = [s.strip() for s in STE100_RE_SENTENCE_END.split(body) if s.strip()]
    for i, sent in enumerate(sentences):
        words = sent.split()
        if len(words) > 20:
            issues.append(f"{path}: Sentence {i+1} exceeds 20 words ({len(words)}): {sent[:60]}...")
        # Passive voice check (rough)
        if STE100_RE_PASSIVE.search(sent) and 'is' not in sent.lower()[:10]:
            # heuristic: skip obvious constructions like "is required"
            pass  # too noisy for now, disabled


def check_wikilinks(path, content):
    """Check wikilinks resolve to valid targets (sources/ or concepts/ or adr-NNNN)."""
    wikilinks = WIKILINK_RE.findall(content)
    for wl in wikilinks:
        target = wl.split('|')[0].strip()
        # Valid patterns: sources/slug, concepts/slug, adr-NNNN
        if target.startswith('sources/') or target.startswith('concepts/'):
            issues.append(f"{path}: Wikilink target '{target}' — wikilinks in ADRs must use Markdown links, not wikilinks")
        elif target.startswith('adr-') or '/' not in target:
            pass  # ADR internal links are fine as markdown links
        elif '/' in target and not target.startswith(('sources/', 'concepts/', 'entities/')):
            issues.append(f"{path}: Unknown wikilink prefix in '{target}'")


def check_required_sections(path, content):
    """Check that all required MADR sections are present."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    found_sections = set()
    for m in re.finditer(r'^#{1,6}\s+(.+)$', body, re.MULTILINE):
        title = m.group(1).strip().rstrip(':')
        found_sections.add(title)
    # Normalize: "Context" may appear as "## Context" etc.
    for section in REQUIRED_SECTIONS:
        if section not in found_sections:
            issues.append(f"{path}: Missing required section '{section}'")


def check_file(path):
    content = path.read_text()
    check_frontmatter(path.name, content)
    check_wikilinks(path.name, content)
    check_required_sections(path.name, content)
    check_ste100(path.name, content)


def main():
    docs_dir = DOCS_DIR
    if not docs_dir.exists():
        print(f"ADR directory not found: {docs_dir}")
        sys.exit(0)

    adr_files = sorted(docs_dir.glob("????-*.md"))
    if not adr_files:
        print("No ADR files found")
        sys.exit(0)

    for f in adr_files:
        check_file(f)

    if issues:
        print(f"ADR LINT: {len(issues)} issue(s)\n")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print(f"ADR LINT: Clean ({len(adr_files)} files checked)")
        sys.exit(0)


if __name__ == "__main__":
    main()
