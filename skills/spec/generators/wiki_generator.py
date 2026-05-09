#!/usr/bin/env python3
"""
Wiki Generator — converts raw content to wiki vault entries.

Follows wiki-maintainer skill structure exactly:
- sources/NNNN-slug.md for raw content (canonical)
- concepts/NNNN-slug.md for claims + relationships (metadata only)
- Frontmatter with id, pageType, provenance, tags
- Zero duplication — concepts reference sources
"""

import re
from pathlib import Path
from datetime import datetime


class WikiGenerator:
    
    WIKI_VAULT = Path.home() / ".openclaw/wiki/main"
    
    # Source types for frontmatter
    SOURCE_TYPES = [
        "gherkin-pipeline",
        "telegram-export",
        "adr",
        "article",
        "notes",
        "seminar",
        "documentation"
    ]
    
    def __init__(self, vault_path=None):
        self.vault = Path(vault_path) if vault_path else self.WIKI_VAULT
    
    def generate(self, raw_content, source_type="gherkin-pipeline"):
        """
        Generate wiki entries from raw content.
        Returns list of created file paths.
        """
        files_created = []
        
        # Clean and prepare content
        content = self._clean_content(raw_content)
        
        # Determine next number
        next_num = self._get_next_number()
        
        # Create slug from content
        slug = self._content_to_slug(content)
        
        # Create source file
        source_file = self._create_source(next_num, slug, content, source_type)
        if source_file:
            files_created.append(source_file)
        
        # Create concept file (claims extracted from content)
        concept_file = self._create_concept(next_num, slug, content, source_type)
        if concept_file:
            files_created.append(concept_file)
        
        return files_created
    
    def _clean_content(self, content):
        """Strip HTML, normalize whitespace."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Truncate very long content
        if len(text) > 50000:
            text = text[:50000] + "\n\n[... truncated ...]"
        return text
    
    def _get_next_number(self):
        """Get next sequential number."""
        sources_dir = self.vault / "sources"
        if not sources_dir.exists():
            return 1
        
        files = list(sources_dir.glob("[0-9]*.md"))
        nums = []
        for f in files:
            try:
                nums.append(int(f.name.split("-")[0]))
            except ValueError:
                pass
        
        return (max(nums) + 1) if nums else 1
    
    def _content_to_slug(self, content):
        """Create URL-safe slug from content."""
        first_line = content.split("\n")[0][:60]
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', first_line)
        slug = re.sub(r'\s+', '-', slug).lower().strip("-")
        return slug[:60] or "content"
    
    def _create_source(self, num, slug, content, source_type):
        """Create canonical source file."""
        sources_dir = self.vault / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)
        
        num_str = str(num).zfill(4)
        filename = f"{num_str}-{slug}.md"
        filepath = sources_dir / filename
        
        # First 200 chars of content for title
        title = content[:80].split("\n")[0].strip()
        if len(title) > 60:
            title = title[:60] + "..."
        
        frontmatter = f"""---
id: source.{num_str}-{slug}
pageType: source
title: "{title}"
canonicalPath: sources/{filename}
sourceType: {source_type}
entityType: source
confidence: 0.75
updatedAt: "{datetime.now().strftime('%Y-%m-%d')}"
provenance:
  - source: gherkin-pipeline
    extractedBy: genesis
    privacyTier: public
tags:
  - gherkin
  - spec
  - pipeline
sourceIds: []
relatedConcepts: []
---

{content}
"""
        
        try:
            filepath.write_text(frontmatter, encoding="utf-8")
            return filepath
        except Exception as e:
            print(f"    [!] Source write failed: {e}")
            return None
    
    def _create_concept(self, num, slug, content, source_type):
        """Create concept file with extracted claims."""
        concepts_dir = self.vault / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        
        num_str = str(num).zfill(4)
        filename = f"{num_str}-{slug}-concept.md"
        filepath = concepts_dir / filename
        
        # Extract simple claims (sentences with key terms)
        claims = self._extract_claims(content)
        
        title = f"Gherkin Spec: {slug[:50]}"
        
        frontmatter = f"""---
id: concept.{num_str}-{slug}
pageType: concept
title: "{title}"
confidence: 0.75
updatedAt: "{datetime.now().strftime('%Y-%m-%d')}"
tags:
  - gherkin
  - specification
  - behavior-driven
sourceIds:
  - source.{num_str}-{slug}
relatedConcepts: []
---

## Claims

{claims}

## Related Source

[[sources/{num_str}-{slug}.md]] — raw content
"""
        
        try:
            filepath.write_text(frontmatter, encoding="utf-8")
            return filepath
        except Exception as e:
            print(f"    [!] Concept write failed: {e}")
            return None
    
    def _extract_claims(self, content):
        """Extract structured claims from content."""
        # Simple extraction: sentences with key terms
        sentences = re.split(r'[.!?\n]', content)
        claims = []
        
        key_terms = ["given", "when", "then", "scenario", "feature", 
                     "user", "system", "expect", "should", "must",
                     "behavior", "specification", "test"]
        
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 30 and any(term in sent.lower() for term in key_terms):
                claims.append(f"- {sent.strip()}")
        
        if not claims:
            # Fallback: first 5 significant sentences
            for sent in sentences[:5]:
                sent = sent.strip()
                if len(sent) > 30:
                    claims.append(f"- {sent.strip()}")
        
        return "\n".join(claims[:10]) if claims else "- No claims extracted"