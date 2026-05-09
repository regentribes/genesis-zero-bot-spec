#!/usr/bin/env python3
"""
STE100 sentence detector.
Runs against each sentence in input text.
Reports: unapproved words, long sentences (>20 words), passive voice.
No AI rewrite — detection only.
"""
import json, sys, re
from pathlib import Path

ASD_DIR = Path("/tmp/ASD-STE100")

def load_ste_dict():
    rules_path = ASD_DIR / "logic" / "asd_rules.json"
    with open(rules_path) as f:
        return json.load(f)

def split_sentences(text):
    """Split text into sentences using NLTK or fallback."""
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
    """Run STE detection on text. Returns issues per sentence."""
    sentences = split_sentences(text)
    results = []
    
    for i, sent in enumerate(sentences):
        words = re.findall(r'\w+', sent)
        issues = []
        
        # Check unapproved words
        for word in words:
            w = word.lower()
            if w in ste_data and not ste_data[w].get("is_approved", False):
                issues.append(f"UNAPPROVED:{word}")
        
        # Check length
        if len(words) > 20:
            issues.append(f"TOOLONG:{len(words)}w")
        
        # Check passive voice (simplified)
        if re.search(r'\b(is|are|was|were|be|been|being)\b.*\b\w+ed\b', sent, re.IGNORECASE):
            issues.append("PASSIVE")
        
        if issues:
            results.append({"sentence_num": i + 1, "text": sent, "issues": issues})
    
    return results

def main():
    text = sys.stdin.read()
    ste_data = load_ste_dict()
    results = detect_ste(text, ste_data)
    
    if not results:
        print("STE check: PASS (no issues)")
        sys.exit(0)
    
    print(f"STE check: {len(results)} sentences with issues")
    for r in results:
        print(f"  [{', '.join(r['issues'])}] {r['text'][:100]}{'...' if len(r['text']) > 100 else ''}")
    
    sys.exit(1)

if __name__ == "__main__":
    main()
