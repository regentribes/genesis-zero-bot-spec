#!/usr/bin/env python3
"""
ASD-STE100 sentence auditor for wiki vault.
Runs ste_detect against every sentence in every concept page.
Reports all STE violations found.
No AI rewrite — detection only.
"""
import json, sys, re
from pathlib import Path

ASD_DIR = Path("/tmp/ASD-STE100")
WIKI_DIR = Path.home() / ".openclaw/wiki/main"

def load_ste_dict():
    rules_path = ASD_DIR / "logic" / "asd_rules.json"
    with open(rules_path) as f:
        return json.load(f)

def split_sentences(text):
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except:
            nltk.download('punkt_tab', quiet=True)
            nltk.download('punkt', quiet=True)
        return nltk.sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\s+', text)

def detect_ste(text, ste_data):
    sentences = split_sentences(text)
    results = []
    for i, sent in enumerate(sentences):
        words = re.findall(r'\w+', sent)
        issues = []
        for word in words:
            w = word.lower()
            if w in ste_data and not ste_data[w].get("is_approved", False):
                issues.append(f"UNAPPROVED:{word}")
        if len(words) > 20:
            issues.append(f"TOOLONG:{len(words)}w")
        if re.search(r'\b(is|are|was|were|be|been|being)\b.*\b\w+ed\b', sent, re.IGNORECASE):
            issues.append("PASSIVE")
        if issues:
            results.append({"sent_num": i + 1, "text": sent, "issues": issues})
    return results

def audit_vault():
    ste_data = load_ste_dict()
    total_violations = 0
    pages_checked = 0
    
    for subdir in ["concepts", "sources", "entities"]:
        d = WIKI_DIR / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            text = f.read_text()
            # Strip frontmatter
            if text.startswith('---'):
                end_idx = text.find('\n---\n', 4)
                if end_idx != -1:
                    text = text[end_idx + 5:]
            
            # Strip headers
            text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
            
            results = detect_ste(text, ste_data)
            if results:
                print(f"\n{f.name}: {len(results)} STE violations")
                for r in results:
                    truncated = r['text'][:80] + ('...' if len(r['text']) > 80 else '')
                    print(f"  [{', '.join(r['issues'])}] {truncated}")
                total_violations += len(results)
            pages_checked += 1
    
    print(f"\n--- ASD-STE100 Audit Summary ---")
    print(f"Pages checked: {pages_checked}")
    print(f"Total STE violations: {total_violations}")
    
    if total_violations > 0:
        sys.exit(1)
    else:
        print("All pages: STE clean")
        sys.exit(0)

if __name__ == "__main__":
    audit_vault()
