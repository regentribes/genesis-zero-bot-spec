#!/usr/bin/env python3
"""
Build HTML site from Gherkin .feature files.
Reads docs/*.feature, outputs syntax-highlighted HTML to _site/.
Aligned with adrs build.py style: dark/light theme, CSS vars, pure B/W minimal.
"""

import re
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path(__file__).parent / "docs"
SITE_DIR = Path(__file__).parent / "_site"
ASSETS_DIR = Path(__file__).parent / "assets"

THEME_TOGGLE = '<button id="theme-toggle" aria-label="Toggle theme" onclick="toggleTheme()">&#9790;</button>'
THEME_SCRIPT = '''<script>
function toggleTheme(){
  var b=document.body,d=b.classList.contains("dark");
  b.classList.toggle("dark");b.classList.toggle("light");
  var dark=d?"dark":"light";
  var v=[["--bg",dark?"#000000":"#ffffff"],["--text",dark?"#888888":"#333333"],
         ["--heading",dark?"#ffffff":"#000000"],["--muted",dark?"#555555":"#888888"],
         ["--border",dark?"#222222":"#e0e0e0"],["--code-bg",dark?"#0a0a0a":"#f5f5f5"],
         ["--pre-bg",dark?"#0a0a0a":"#f5f5f5"],["--pre-text",dark?"#888888":"#333333"],
         ["--table-border",dark?"#222222":"#e0e0e0"],["--table-header-bg",dark?"#111111":"#f5f5f5"]];
  for(var i=0;i<v.length;i++){b.style.setProperty(v[i][0],v[i][1]);
    document.documentElement.style.setProperty(v[i][0],v[i][1]);}
  localStorage.setItem("theme",b.classList.contains("dark")?"dark":"light");
}
document.addEventListener("DOMContentLoaded",function(){
  var s=localStorage.getItem("theme");
  var isDark=!s||s==="dark"||(!s&&window.matchMedia("(prefers-color-scheme:dark)").matches);
  if(isDark){document.body.className="dark"}else{document.body.className="light"}
  var dark=document.body.classList.contains("dark");
  var v=[["--bg",dark?"#000000":"#ffffff"],["--text",dark?"#888888":"#333333"],
         ["--heading",dark?"#ffffff":"#000000"],["--muted",dark?"#555555":"#888888"],
         ["--border",dark?"#222222":"#e0e0e0"],["--code-bg",dark?"#0a0a0a":"#f5f5f5"],
         ["--pre-bg",dark?"#0a0a0a":"#f5f5f5"],["--pre-text",dark?"#888888":"#333333"],
         ["--table-border",dark?"#222222":"#e0e0e0"],["--table-header-bg",dark?"#111111":"#f5f5f5"]];
  for(var i=0;i<v.length;i++){document.body.style.setProperty(v[i][0],v[i][1]);
    document.documentElement.style.setProperty(v[i][0],v[i][1]);}
});
</script>'''

SITE_HEADER = f'''<header class="site-header">
  <div class="container">
    <h1><a href="index.html">Gherkin Specs</a></h1>
    <p>RegenTribes living specifications</p>
    {THEME_TOGGLE}
  </div>
</header>'''

SITE_FOOTER = '''<footer>
  <p>Generated from wiki synthesis · validated with ghokin · deployed via GitHub Actions</p>
</footer>'''


def parse_feature(content):
    """Parse a .feature file into structured data."""
    lines = content.split('\n')
    
    feature_name = ""
    feature_description = []
    background_steps = []
    in_background = False
    scenarios = []
    current_scenario = None
    current_steps = []
    current_tags = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        
        # Feature
        if stripped.startswith("Feature:") and not current_scenario:
            feature_name = stripped[len("Feature:"):].strip()
            # Collect description lines until next keyword
            j = i + 1
            while j < len(lines):
              next_stripped = lines[j].strip()
              if next_stripped.startswith(("Scenario", "Background", "Given", "When", "Then", "And", "But", "@")):
                break
              if next_stripped:
                feature_description.append(next_stripped)
              j += 1
        
        # Background
        elif stripped.startswith("Background:"):
            in_background = True
            current_steps = []
        
        # Tags
        elif stripped.startswith("@"):
            tags = [t.strip() for t in stripped.split() if t.startswith("@")]
            if current_scenario:
                current_scenario['tags'].extend(tags)
            else:
                current_tags.extend(tags)
        
        # Scenario
        elif stripped.startswith("Scenario:"):
            if current_scenario and current_steps:
                current_scenario['steps'] = current_steps
                scenarios.append(current_scenario)
            
            title = stripped[len("Scenario:"):].strip()
            current_scenario = {
                'title': title,
                'steps': [],
                'tags': list(current_tags),
                'in_background': in_background
            }
            current_steps = []
            current_tags = []
            in_background = False
        
        # Step
        elif stripped.startswith(("Given ", "When ", "Then ", "And ", "But ")):
            keyword = stripped.split(" ", 1)[0]
            text = stripped[len(keyword + " "):]
            
            if in_background:
                background_steps.append({'keyword': keyword, 'text': text})
            else:
                if current_scenario is None:
                    # Scenario-less step, start implicit scenario
                    current_scenario = {'title': '(steps)', 'steps': [], 'tags': [], 'in_background': False}
                current_steps.append({'keyword': keyword, 'text': text})
        
        i += 1
    
    # Close last scenario
    if current_scenario and current_steps:
        current_scenario['steps'] = current_steps
        scenarios.append(current_scenario)
    
    return {
        'name': feature_name,
        'description': '\n'.join(feature_description),
        'background_steps': background_steps,
        'scenarios': scenarios
    }


def render_step_text(text):
    """Render step text with inline code highlighting."""
    # Wrap things in quotes as potential parameters
    result = text
    # Highlight quoted strings
    result = re.sub(r'"([^"]*)"', r'<code>"\1"</code>', result)
    return result


def render_scenario(scenario, background_steps):
    """Render a scenario with its steps."""
    all_steps = background_steps + scenario['steps']
    
    tags_html = ""
    if scenario.get('tags'):
        tag_links = ' '.join([f'<span class="tag">{t}</span>' for t in scenario['tags']])
        tags_html = f'<div class="tags">{tag_links}</div>'
    
    steps_html = []
    for step in all_steps:
        kw_class = step['keyword'].lower()
        steps_html.append(
            f'<div class="step">'
            f'<span class="step-keyword {kw_class}">{step["keyword"]}</span>'
            f'<span class="step-text">{render_step_text(step["text"])}</span>'
            f'</div>'
        )
    
    return f'''<div class="scenario">
  {tags_html}
  <div class="scenario-header">
    <span class="scenario-label">Scenario</span>
    <span class="scenario-title">{scenario["title"]}</span>
  </div>
  <div class="steps">{"".join(steps_html)}</div>
</div>'''


def render_feature(feature):
    """Render a feature with all scenarios."""
    desc_html = ""
    if feature['description']:
        # Only add As a prefix if description doesn't already start with it
        if feature['description'] and not feature['description'].strip().startswith('As a'):
            desc_html = f'<div class="feature-story"><strong>As a</strong> regenerative community member — {feature["description"][:200]}</div>'
        elif feature['description']:
            desc_html = f'<div class="feature-story">{feature["description"][:200]}</div>'
    
    scenarios_html = "".join(
        render_scenario(s, feature['background_steps']) for s in feature['scenarios']
    )
    
    return f'''<article class="feature">
  <div class="feature-header">
    <h2>{feature["name"]}</h2>
  </div>
  {desc_html}
  {scenarios_html}
</article>'''


def build_index(features):
    """Build the index page."""
    feature_links = []
    for f in features:
        slug = re.sub(r'[^a-z0-9]+', '-', f['name'].lower()).strip('-')
        feature_links.append(
            f'<li><a href="feature-{slug}.html">{f["name"]}</a> '
            f'<span class="count">{len(f["scenarios"])} scenarios</span></li>'
        )
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gherkin Specs — RegenTribes</title>
  <link rel="stylesheet" href="assets/style.css">
  {THEME_SCRIPT}
</head>
<body>
{SITE_HEADER}
<main>
  <h1 style="color:var(--heading);margin-bottom:2rem;font-size:1.5rem;">Living Specifications</h1>
  <p style="color:var(--muted);margin-bottom:2.5rem;">Behaviors expressed in Gherkin (Given/When/Then), validated with ghokin before every commit. Generated from wiki synthesis.</p>
  <ul style="list-style:none;padding:0;">
    {"".join(feature_links)}
  </ul>
  <style>
    ul li {{ padding: 0.5rem 0; border-bottom: 1px solid var(--border); }}
    ul li:last-child {{ border-bottom: none; }}
    ul li a {{ color: var(--heading); text-decoration: none; font-weight: 500; }}
    ul li a:hover {{ color: var(--text); }}
    ul li .count {{ color: var(--muted); font-size: 0.8rem; margin-left: 0.5rem; }}
  </style>
</main>
{SITE_FOOTER}
</body>
</html>'''


def build_feature_page(feature):
    """Build individual feature page."""
    slug = re.sub(r'[^a-z0-9]+', '-', feature['name'].lower()).strip('-')
    
    content = render_feature(feature)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{feature["name"]} — Gherkin Spec</title>
  <link rel="stylesheet" href="assets/style.css">
  {THEME_SCRIPT}
</head>
<body>
{SITE_HEADER}
<main>
  <p style="margin-bottom:1.5rem;"><a href="index.html" style="color:var(--muted);">← All Specs</a></p>
  {content}
</main>
{SITE_FOOTER}
</body>
</html>'''


def main():
    SITE_DIR.mkdir(exist_ok=True)
    
    # Copy assets
    if ASSETS_DIR.exists():
        import shutil
        site_assets = SITE_DIR / "assets"
        site_assets.mkdir(exist_ok=True)
        for f in ASSETS_DIR.glob("*"):
            shutil.copy2(f, site_assets / f.name)
    
    # Find all .feature files
    feature_files = sorted(DOCS_DIR.glob("*.feature"))
    print(f"Building {len(feature_files)} feature files...")
    
    features = []
    for fp in feature_files:
        content = fp.read_text(encoding="utf-8")
        feature = parse_feature(content)
        features.append(feature)
        
        # Build individual page
        slug = re.sub(r'[^a-z0-9]+', '-', feature['name'].lower()).strip('-')
        html = build_feature_page(feature)
        SITE_DIR.joinpath(f"feature-{slug}.html").write_text(html, encoding="utf-8")
        print(f"  [✓] {fp.name} → feature-{slug}.html ({len(feature['scenarios'])} scenarios)")
    
    # Build index
    index_html = build_index(features)
    SITE_DIR.joinpath("index.html").write_text(index_html, encoding="utf-8")
    
    print(f"\nBuilt {len(features)} features → {SITE_DIR}/")
    print(f"Index: {SITE_DIR}/index.html")


if __name__ == "__main__":
    main()
