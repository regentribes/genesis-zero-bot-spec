#!/usr/bin/env python3
"""
Gherkin Spec CLI — command-line interface for the pipeline.

Usage:
    python3 cli.py --input <source> --types wiki,adr,gherkin [--validate]
    python3 cli.py --input "User clicks submit. System shows confirmation." --types gherkin
    python3 cli.py --input /path/to/file.md --types wiki,adr,gherkin --validate
"""

import sys
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Gherkin Spec Pipeline — transform arbitrary info into wiki/ADR/Gherkin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transform a URL into all three outputs
  python3 cli.py --input "https://example.com/article" --types wiki,adr,gherkin

  # Gherkin only from raw text
  python3 cli.py --input "User submits soil observation. System stores and replies." --types gherkin --validate

  # ADR only from document
  python3 cli.py --input /path/to/spec.md --types adr

  # Specify feature name
  python3 cli.py --input "authentication flow" --types gherkin --feature-name "User Authentication"
"""
    )
    
    parser.add_argument("--input", "-i", required=True, 
                        help="URL, file path, or raw text to transform")
    parser.add_argument("--types", "-t", default="gherkin",
                        help="Comma-separated: wiki,adr,gherkin (default: gherkin)")
    parser.add_argument("--validate", "-v", action="store_true",
                        help="Run ghokin validation on Gherkin output")
    parser.add_argument("--output", "-o",
                        help="Output directory override")
    parser.add_argument("--feature-name", "-f",
                        help="Override feature name for Gherkin generation")
    
    args = parser.parse_args()
    
    types = [t.strip() for t in args.types.split(",")]
    
    print(f"[*] Gherkin Spec Pipeline")
    print(f"    Input: {args.input[:80]}{'...' if len(args.input) > 80 else ''}")
    print(f"    Types: {', '.join(types)}")
    print(f"    Validate: {args.validate}")
    print()
    
    result = pipeline(
        args.input,
        types,
        validate=args.validate,
        output_dir=args.output
    )
    
    print()
    if result["status"] == "ok":
        print("[✓] Pipeline completed successfully")
        
        for output_type, output_data in result.get("outputs", {}).items():
            if isinstance(output_data, dict) and "error" in output_data:
                print(f"    [!] {output_type}: {output_data['error']}")
            elif isinstance(output_data, list):
                print(f"    → {output_type}: {len(output_data)} files")
            elif isinstance(output_data, dict):
                count = output_data.get("count", output_data.get("files", []).__len__())
                print(f"    → {output_type}: {count} files")
    else:
        print(f"[!] Pipeline failed: {result.get('reason', 'unknown')}")
        sys.exit(1)


if __name__ == "__main__":
    main()