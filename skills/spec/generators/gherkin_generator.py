#!/usr/bin/env python3
"""
Gherkin Generator — converts raw content into .feature files.

Follows automationpanda/gherkin-guidelines-for-ai rules:
- One behavior per scenario
- Given/When/Then as Arrange/Act/Assert
- Third person, present tense, subject-predicate
- Domain-level abstraction, no UI/API plumbing in steps
- State over navigation
- Concrete realistic example data
- < 10 steps per scenario
- 2-space indentation
"""

import re
from pathlib import Path
from datetime import datetime


class GherkinGenerator:
    """
    Converts raw text/content into Gherkin .feature files.
    """
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, raw_content, feature_name=None, validate=True):
        """
        Generate .feature files from raw content.
        
        Returns list of Path objects for created .feature files.
        """
        # Clean content
        content = self._clean_content(raw_content)
        
        # Parse into scenarios
        scenarios = self._parse_scenarios(content)
        
        # Create feature file
        if not scenarios:
            # If no structured scenarios found, create one from entire content
            scenarios = [{"title": "Default Scenario", "steps": self._content_to_steps(content)}]
        
        feature_title = feature_name or self._extract_feature_name(content) or "Generated Feature"
        feature_file = self._create_feature_file(feature_title, scenarios)
        
        return [feature_file] if feature_file else []
    
    def _clean_content(self, content):
        """Strip HTML, normalize."""
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_feature_name(self, content):
        """Extract feature name from content."""
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 80:
                # Remove markdown headers, numbers, punctuation
                cleaned = re.sub(r'^[#\d.\-]+\s*', '', line)
                if cleaned and not cleaned.startswith("http"):
                    return cleaned[:80]
        return None
    
    def _content_to_steps(self, content):
        """Convert unstructured content into Given/When/Then steps."""
        steps = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]', content)
        
        step_type_map = {
            0: "Given",
            1: "When", 
            2: "Then"
        }
        
        for i, sent in enumerate(sentences[:8]):
            sent = sent.strip()
            if len(sent) > 15:
                # Convert to third person, present tense
                step = self._to_gherkin_step(sent)
                if step:
                    step_type = step_type_map.get(i % 3, "And")
                    steps.append({"type": step_type, "text": step})
        
        return steps
    
    def _to_gherkin_step(self, text):
        """Convert sentence to Gherkin step format."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Make third person, present tense
        # Simple heuristic: if it starts with "the user" or "a user", keep it
        # Otherwise add "the system" or similar
        
        if len(text) < 10:
            return None
        
        # Capitalize first letter
        text = text[0].upper() + text[1:]
        
        # Add quotes around parameters
        text = re.sub(r'\b(\w+)\b', r'"\1"', text, count=2)
        
        return text
    
    def _parse_scenarios(self, content):
        """
        Parse structured scenarios from content.
        Looks for Given/When/Then patterns.
        """
        scenarios = []
        
        # Split on Scenario boundaries
        # Handle: "Scenario:", "Scenario Outline:", "### Scenario" (Gherkin in markdown)
        pattern = r'(?:^|\n)(?:scenario|scenario outline)[:\s]*(.+?)(?=\n(?:scenario|feature|$))'
        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        for match in matches:
            title = match.group(1).strip()
            block = match.group(0)
            
            # Extract steps
            steps = []
            step_pattern = r'(given|when|then|and|but)\s+(.+)'
            step_matches = re.finditer(step_pattern, block, re.IGNORECASE)
            
            for sm in step_matches:
                step_type = sm.group(1).capitalize()
                step_text = sm.group(2).strip()
                steps.append({"type": step_type, "text": step_text})
            
            if steps:
                scenarios.append({"title": title[:80], "steps": steps})
        
        return scenarios
    
    def _create_feature_file(self, feature_title, scenarios):
        """Create a .feature file with feature and scenarios."""
        if not scenarios:
            return None
        
        # Create safe filename
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', feature_title)
        slug = re.sub(r'\s+', '-', slug).lower().strip("-")[:50]
        filename = f"{slug}.feature"
        filepath = self.output_dir / filename
        
        lines = [
            f"Feature: {feature_title}",
            "",
            "  As a regenerative community",
            "  I want clear, testable specifications",
            "  So that implementation stays aligned with intent",
            "",
        ]
        
        for scenario in scenarios:
            # Scenario title
            lines.append(f"  Scenario: {scenario['title']}")
            lines.append("")
            
            # Steps
            for step in scenario["steps"]:
                type_map = {
                    "Given": "Given",
                    "When": "When", 
                    "Then": "Then",
                    "And": "And",
                    "But": "But"
                }
                step_type = type_map.get(step["type"], step["type"])
                
                # Ensure proper formatting: 2 spaces indent, quotes around params
                step_text = self._format_step_text(step["text"])
                lines.append(f"    {step_type} {step_text}")
            
            lines.append("")
        
        content = "\n".join(lines)
        
        try:
            filepath.write_text(content, encoding="utf-8")
            return filepath
        except Exception as e:
            print(f"    [!] Feature file write failed: {e}")
            return None
    
    def _format_step_text(self, text):
        """Format step text: add quotes, fix grammar."""
        # If no quotes, wrap first 1-2 obvious parameters
        if '"' not in text:
            # Look for numbers or IDs
            text = re.sub(r'(\d+)', r'"\1"', text, count=1)
        
        return text