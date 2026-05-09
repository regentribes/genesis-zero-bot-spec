#!/usr/bin/env python3
"""
Gherkin Spec Pipeline

Accepts arbitrary information and transforms it into:
- Wiki entries (sources/concepts)
- ADRs (Architecture Decision Records)
- Gherkin .feature files (living specification)

Usage:
    python3 pipeline.py --input <source> --types wiki,adr,gherkin [--validate] [--output <dir>]
"""

import argparse
import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Add skills directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generators.wiki_generator import WikiGenerator
from generators.adr_generator import ADRGenerator
from generators.gherkin_generator import GherkinGenerator
from validators.gherkin_validator import GherkinValidator

GHERKIN_BINARY = "/tmp/ghokin"
WIKI_VAULT = Path.home() / ".openclaw/wiki/main"
ADR_DIR = Path.home() / ".openclaw/workspace-genesis/docs/adrs"
GHERKIN_OUT = Path.home() / ".openclaw/workspace-genesis/docs/gherkin"


def run_command(cmd, cwd=None):
    """Run shell command, return stdout or raise on non-zero exit."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout


def extract_content(input_source):
    """Extract text content from any source using kreuzberg if available."""
    if input_source.startswith("http://") or input_source.startswith("https://"):
        # Use kreuzberg to extract
        cmd = f"cd {Path(__file__).parent.parent.parent} && python3 -c \"\nimport subprocess, json, sys
url = '{input_source}'
result = subprocess.run(['python3', '-m', 'kreuzberg', url], capture_output=True, text=True)
print(result.stdout if result.returncode == 0 else result.stderr)
\""
        try:
            return run_command(cmd)
        except Exception:
            # Fallback: use web_fetch-style extraction via curl
            import urllib.request
            try:
                req = urllib.request.Request(input_source, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    content = resp.read().decode('utf-8', errors='replace')
                    # Basic HTML stripping
                    import re
                    text = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
                    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
                    text = re.sub(r'<[^>]+>', ' ', text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    return text[:50000]  # Limit size
            except Exception as e:
                return f"[ERROR extracting URL: {e}]"
    elif Path(input_source).is_file():
        path = Path(input_source)
        if path.suffix == ".md":
            return path.read_text(encoding="utf-8")
        elif path.suffix in [".txt", ".log"]:
            return path.read_text(encoding="utf-8")
        else:
            return f"[Binary file {path.suffix} - use kreuzberg for extraction]"
    else:
        # Raw text
        return input_source


def get_next_number(target_dir, prefix=""):
    """Get next sequential number for a file in target directory."""
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        return 1
    files = list(target_dir.glob(f"{prefix}*.md")) + list(target_dir.glob(f"{prefix}*.feature"))
    nums = []
    for f in files:
        try:
            nums.append(int(f.stem.split("-")[0]))
        except ValueError:
            pass
    return (max(nums) + 1) if nums else 1


def format_number(n, digits=4):
    """Format number with leading zeros."""
    return str(n).zfill(digits)


def pipeline(input_source, output_types, validate=True, output_dir=None):
    """Main transformation pipeline."""
    
    print(f"[*] Extracting content from: {input_source}")
    raw_content = extract_content(input_source)
    
    if not raw_content or raw_content.startswith("[ERROR"):
        print(f"[!] Extraction failed: {raw_content}")
        return {"status": "error", "reason": raw_content or "empty content"}
    
    print(f"[*] Extracted {len(raw_content)} characters")
    
    results = {
        "status": "ok",
        "outputs": {}
    }
    
    # Determine output directory
    base_out = Path(output_dir) if output_dir else GHERKIN_OUT
    
    # --- Wiki Pipeline ---
    if "wiki" in output_types:
        print("[*] Generating wiki entries...")
        try:
            wiki_gen = WikiGenerator(WIKI_VAULT)
            wiki_files = wiki_gen.generate(raw_content, source_type="gherkin-pipeline")
            results["outputs"]["wiki"] = wiki_files
            print(f"    → {len(wiki_files)} wiki files created")
        except Exception as e:
            results["outputs"]["wiki"] = {"error": str(e)}
            print(f"    → Wiki generation failed: {e}")
    
    # --- ADR Pipeline ---
    if "adr" in output_types:
        print("[*] Generating ADRs...")
        try:
            adr_gen = ADRGenerator(ADR_DIR)
            adr_files = adr_gen.generate(raw_content)
            results["outputs"]["adr"] = adr_files
            print(f"    → {len(adr_files)} ADR files created")
        except Exception as e:
            results["outputs"]["adr"] = {"error": str(e)}
            print(f"    → ADR generation failed: {e}")
    
    # --- Gherkin Pipeline ---
    if "gherkin" in output_types:
        print("[*] Generating Gherkin spec files...")
        gherkin_out = base_out / "features"
        gherkin_out.mkdir(parents=True, exist_ok=True)
        
        try:
            gherkin_gen = GherkinGenerator(gherkin_out)
            feature_files = gherkin_gen.generate(raw_content, validate=validate)
            
            validation_results = []
            if validate:
                print("[*] Validating with ghokin...")
                validator = GherkinValidator(GHERKIN_BINARY)
                
                for f in feature_files:
                    fmt_result = validator.format_file(f)
                    check_result = validator.check_file(f)
                    if not check_result["passed"]:
                        # Iterate: fix and re-check
                        fixed = validator.iterative_fix(f, max_iterations=3)
                        check_result = validator.check_file(f) if fixed else {"passed": False}
                    validation_results.append({
                        "file": f.name,
                        "passed": check_result["passed"],
                        "errors": check_result.get("errors", [])
                    })
            
            results["outputs"]["gherkin"] = {
                "files": [f.name for f in feature_files],
                "validation": validation_results,
                "count": len(feature_files)
            }
            print(f"    → {len(feature_files)} .feature files created")
            
            # Update index
            update_gherkin_index(gherkin_out, feature_files)
            
        except Exception as e:
            results["outputs"]["gherkin"] = {"error": str(e)}
            print(f"    → Gherkin generation failed: {e}")
    
    return results


def update_gherkin_index(out_dir, feature_files):
    """Update the living spec index."""
    index_path = out_dir.parent / "index.md"
    
    lines = [
        "# Living Gherkin Specification Index",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Features",
        ""
    ]
    
    for f in sorted(feature_files):
        title = f.stem.replace("-", " ").title()
        rel_path = f"features/{f.name}"
        lines.append(f"- [{title}]({rel_path})")
    
    lines.append("")
    index_path.write_text("\n".join(lines))
    print(f"    → Updated index: {index_path}")


def main():
    parser = argparse.ArgumentParser(description="Gherkin Spec Pipeline")
    parser.add_argument("--input", required=True, help="URL, file path, or raw text")
    parser.add_argument("--types", default="gherkin", help="Comma-separated: wiki,adr,gherkin")
    parser.add_argument("--validate", action="store_true", help="Run ghokin validation")
    parser.add_argument("--output", help="Output directory override")
    parser.add_argument("--feature-name", help="Feature name override for Gherkin")
    
    args = parser.parse_args()
    
    types = [t.strip() for t in args.types.split(",")]
    
    result = pipeline(args.input, types, validate=args.validate, output_dir=args.output)
    
    print("\n[*] Results:")
    print(json.dumps(result, indent=2))
    
    if result["status"] != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()