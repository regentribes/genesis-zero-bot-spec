#!/usr/bin/env python3
"""
Gherkin Validator — integrates ghokin for format validation with iterative improvement.

Validation pipeline:
1. ghokin fmt replace <file>  — normalize formatting
2. ghokin check <file>        — validate structure, exit code 0 = pass
3. If check fails: fix + re-validate (up to max_iterations)
4. Return pass/fail with errors
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, List, Any


class GherkinValidator:
    """
    Validates Gherkin .feature files using ghokin binary.
    Provides iterative improvement on failure.
    """
    
    def __init__(self, ghokin_binary="/tmp/ghokin"):
        self.ghokin = Path(ghokin_binary)
        if not self.ghokin.exists():
            raise FileNotFoundError(f"ghokin binary not found at {ghokin_binary}")
    
    def format_file(self, filepath: Path) -> Dict[str, Any]:
        """
        Run ghokin fmt to normalize formatting.
        Returns result dict.
        """
        cmd = f'"{self.ghokin}" fmt replace "{filepath}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        return {
            "command": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def check_file(self, filepath: Path) -> Dict[str, Any]:
        """
        Run ghokin check to validate Gherkin structure.
        Returns {"passed": bool, "errors": List[str]}
        """
        cmd = f'"{self.ghokin}" check "{filepath}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        passed = result.returncode == 0
        errors = []
        
        if not passed:
            # Parse errors from stderr
            errors = self._parse_errors(result.stderr + result.stdout)
        
        return {
            "passed": passed,
            "errors": errors,
            "returncode": result.returncode
        }
    
    def _parse_errors(self, output: str) -> List[str]:
        """Parse ghokin error output into structured errors."""
        errors = []
        
        # ghokin outputs file:line:col: message format
        pattern = r'([^:\n]+):(\d+):(\d+): (.+)'
        matches = re.finditer(pattern, output)
        
        for match in matches:
            errors.append({
                "file": match.group(1),
                "line": int(match.group(2)),
                "col": int(match.group(3)),
                "message": match.group(4)
            })
        
        if not errors:
            # Fallback: just return the output as single error
            lines = [l.strip() for l in output.split("\n") if l.strip()]
            errors = [{"raw": lines[:5]}]
        
        return errors
    
    def iterative_fix(self, filepath: Path, max_iterations: int = 3) -> bool:
        """
        Attempt to fix Gherkin issues iteratively.
        
        Process:
        1. Format file
        2. Check for errors
        3. If errors: apply common fixes
        4. Re-check
        5. Repeat up to max_iterations
        
        Returns True if eventually passes, False otherwise.
        """
        for iteration in range(max_iterations):
            # Format first
            fmt_result = self.format_file(filepath)
            if fmt_result["returncode"] != 0:
                print(f"    [!] Iteration {iteration+1}: fmt failed: {fmt_result.get('stderr', '')}")
            
            # Check
            check_result = self.check_file(filepath)
            
            if check_result["passed"]:
                print(f"    [✓] Iteration {iteration+1}: passed validation")
                return True
            
            # Apply fixes based on error types
            errors = check_result.get("errors", [])
            fixed = self._apply_fixes(filepath, errors)
            
            if not fixed:
                print(f"    [!] Iteration {iteration+1}: could not auto-fix errors")
                break
            
            print(f"    [→] Iteration {iteration+1}: applied fixes, re-checking...")
        
        # Final check
        final_result = self.check_file(filepath)
        return final_result["passed"]
    
    def _apply_fixes(self, filepath: Path, errors: List) -> bool:
        """
        Apply common fixes based on error patterns.
        Returns True if any fixes applied.
        """
        content = filepath.read_text(encoding="utf-8")
        original = content
        fixed = False
        
        for error in errors:
            if isinstance(error, dict) and "message" in error:
                msg = error["message"]
                line_num = error.get("line", 0)
                
                # Common fix patterns
                
                # Missing blank line between scenarios
                if "blank" in msg.lower() or "empty line" in msg.lower():
                    content = self._fix_blank_lines(content)
                    fixed = True
                
                # Indentation issues (should be 2 spaces)
                if "indent" in msg.lower() or "space" in msg.lower():
                    content = self._fix_indentation(content)
                    fixed = True
                
                # Keyword casing
                if "given" in msg.lower() or "when" in msg.lower() or "then" in msg.lower():
                    content = self._fix_keyword_casing(content)
                    fixed = True
                
                # Feature/Scenario format
                if "feature" in msg.lower() or "scenario" in msg.lower():
                    content = self._fix_feature_scenario_format(content)
                    fixed = True
        
        if fixed and content != original:
            filepath.write_text(content, encoding="utf-8")
        
        return fixed
    
    def _fix_blank_lines(self, content: str) -> str:
        """Add blank lines between scenarios."""
        lines = content.split("\n")
        result = []
        prev_is_blank = False
        
        for line in lines:
            stripped = line.strip()
            
            # Detect scenario/background/feature lines
            is_scenario_line = any(kw in stripped.lower() for kw in 
                ["scenario:", "background:", "feature:", "scenario outline:"])
            
            if is_scenario_line and prev_is_blank:
                # Don't add extra blank line before scenario
                pass
            elif stripped.startswith("Scenario") and not prev_is_blank:
                # Add blank line before scenario if missing
                if result and result[-1].strip():
                    result.append("")
            
            result.append(line)
            prev_is_blank = not stripped
        
        return "\n".join(result)
    
    def _fix_indentation(self, content: str) -> str:
        """Fix indentation to 2 spaces for steps."""
        lines = content.split("\n")
        result = []
        
        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            
            # If step keyword, ensure 2-space indent
            step_kws = ["Given", "When", "Then", "And", "But", "Scenario", "Background", "Feature"]
            if any(stripped.startswith(kw) for kw in step_kws):
                # Calculate expected indent
                if stripped.startswith("Feature:"):
                    expected = 0
                elif stripped.startswith("Scenario") or stripped.startswith("Background"):
                    expected = 2
                else:
                    expected = 4  # Steps under scenario
                
                if indent != expected:
                    line = " " * expected + stripped
            
            result.append(line)
        
        return "\n".join(result)
    
    def _fix_keyword_casing(self, content: str) -> str:
        """Fix Gherkin keyword casing."""
        # Replace incorrect keyword patterns
        replacements = [
            (r'\bgiven\b', 'Given'),
            (r'\bwhen\b', 'When'),
            (r'\bthen\b', 'Then'),
            (r'\band\b', 'And'),
            (r'\bbut\b', 'But'),
            (r'\bscenario\b', 'Scenario'),
            (r'\bbackground\b', 'Background'),
            (r'\bfeature\b(?!\s*:)', 'Feature'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def _fix_feature_scenario_format(self, content: str) -> str:
        """Fix Feature/Scenario format issues."""
        lines = content.split("\n")
        result = []
        
        for line in lines:
            stripped = line.strip()
            
            # Ensure Feature: has no leading spaces
            if stripped.startswith("Feature:"):
                result.append("Feature:" + stripped[len("Feature:"):].strip())
            # Ensure Scenario has 2-space indent
            elif stripped.startswith("Scenario"):
                if not line.startswith("  Scenario"):
                    line = "  " + stripped
                    # Remove any extra indentation
                    result.append(line)
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return "\n".join(result)
    
    def validate_and_fix(self, filepath: Path) -> Dict[str, Any]:
        """
        Complete validation pipeline with auto-fix.
        Returns detailed result.
        """
        if not filepath.exists():
            return {"status": "error", "reason": "file not found"}
        
        result = {
            "file": str(filepath),
            "format_passed": False,
            "check_passed": False,
            "iterations": 0,
            "final_passed": False,
            "errors": []
        }
        
        # Step 1: Format
        fmt_result = self.format_file(filepath)
        result["format_passed"] = fmt_result["returncode"] == 0
        
        # Step 2: Check
        check_result = self.check_file(filepath)
        result["check_passed"] = check_result["passed"]
        
        if check_result["passed"]:
            result["final_passed"] = True
            return result
        
        # Step 3: Iterative fix
        result["iterations"] = result["iterations"] + 1
        fixed = self.iterative_fix(filepath)
        result["final_passed"] = fixed
        
        if not fixed:
            result["errors"] = check_result.get("errors", [])
        
        return result