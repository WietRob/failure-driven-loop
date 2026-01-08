#!/usr/bin/env python3
"""
Naming Validator for Traceability Enforcer

Validates test file naming conventions that encode traceability.

Usage:
    # Validate all files
    python3 validate_naming.py --all

    # Validate specific file
    python3 validate_naming.py --file tests/unit/TC-UT-086_component.py

    # Validate by level
    python3 validate_naming.py --level UT

    # JSON output for CI/CD
    python3 validate_naming.py --all --json

Part of: Failure-Driven Enforcement Loop
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Optional, Dict, Any

# Valid test levels
VALID_LEVELS = {"UT", "IT", "ST", "AT"}

# Naming pattern
NAMING_PATTERN = re.compile(r"^TC-(UT|IT|ST|AT)-(\d+)_(.+)\.py$")


class NamingValidator:
    """Validates test file naming conventions."""

    def __init__(self) -> None:
        self.results: List[Dict[str, Any]] = []

    def validate_filename(self, filepath: Path) -> Dict[str, Any]:
        """Validate a single file's naming convention."""
        result: Dict[str, Any] = {
            "file": str(filepath),
            "valid": False,
            "level": None,
            "id": None,
            "component": None,
            "errors": [],
            "recommendation": None,
        }

        # Check if file exists
        if not filepath.exists():
            result["errors"].append(f"File not found: {filepath}")
            return result

        # Extract filename
        filename = filepath.name

        # Match naming pattern
        match = NAMING_PATTERN.match(filename)
        if not match:
            result["errors"].append("Invalid naming format")
            result["errors"].append("Expected: TC-{LEVEL}-{ID}_{component}.py")
            result["errors"].append(f"Found: {filename}")
            result["recommendation"] = "Rename to match TC-LEVEL-ID_component.py pattern"
            return result

        # Extract components
        level = match.group(1)
        id_str = match.group(2)
        component = match.group(3)

        # Validate level
        if level not in VALID_LEVELS:
            result["errors"].append(f"Invalid level: {level}")
            result["recommendation"] = "Level must be one of: UT, IT, ST, AT"
            return result

        # Validate ID is numeric
        if not id_str.isdigit():
            result["errors"].append(f"ID must be numeric: {id_str}")
            return result

        # All checks passed
        result["valid"] = True
        result["level"] = level
        result["id"] = id_str
        result["component"] = component

        return result

    def validate_all(self, directory: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Validate all test files in directory."""
        results: List[Dict[str, Any]] = []

        if directory is None:
            # Default to tests/ directory
            directory = Path(__file__).parent.parent.parent / "tests"

        if not directory.exists():
            return [{"error": f"Directory not found: {directory}"}]

        # Find all .py files
        test_files = list(directory.rglob("*.py"))

        for filepath in test_files:
            result = self.validate_filename(filepath)
            results.append(result)

        return results

    def validate_by_level(
        self, level: str, directory: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Validate files by test level."""
        results: List[Dict[str, Any]] = []

        if level not in VALID_LEVELS:
            return [{"error": f"Invalid level: {level}. Must be one of: UT, IT, ST, AT"}]

        if directory is None:
            directory = Path(__file__).parent.parent.parent / "tests"

        if not directory.exists():
            return [{"error": f"Directory not found: {directory}"}]

        # Find files matching level
        pattern = f"*-{level}-*.py"
        test_files = list(directory.rglob(pattern))

        for filepath in test_files:
            result = self.validate_filename(filepath)
            if result.get("level") == level:
                results.append(result)

        return results

    def print_results(self, results: List[Dict[str, Any]], json_output: bool = False) -> None:
        """Print validation results."""
        if json_output:
            print(json.dumps(results, indent=2))
            return

        # Count results
        valid_count = sum(1 for r in results if r.get("valid", False))
        invalid_count = len(results) - valid_count

        print(f"\n{'=' * 60}")
        print("NAMING VALIDATION RESULTS")
        print(f"{'=' * 60}")
        print(f"Total files: {len(results)}")
        print(f"✅ Valid: {valid_count}")
        print(f"❌ Invalid: {invalid_count}")
        print()

        # Print invalid files first
        invalid_results = [r for r in results if not r.get("valid", False)]
        valid_results = [r for r in results if r.get("valid", False)]

        # Print invalid
        if invalid_results:
            print("❌ INVALID FILES:")
            print("-" * 60)
            for result in invalid_results:
                print(f"\nFile: {result['file']}")
                for error in result.get("errors", []):
                    print(f"  - {error}")
                if result.get("recommendation"):
                    print(f"  💡 {result['recommendation']}")

        # Print valid (summary only)
        if valid_results:
            print(f"\n✅ VALID FILES ({len(valid_results)} shown as summary):")
            print("-" * 60)
            for result in valid_results[:5]:  # Show first 5
                level = result.get("level", "?")
                id_num = result.get("id", "???")
                component = result.get("component", "???")
                print(f"  TC-{level}-{id_num}_{component}.py")
            if len(valid_results) > 5:
                print(f"  ... and {len(valid_results) - 5} more")

        print()

        # Summary
        if invalid_count > 0:
            print(f"⚠️  {invalid_count} file(s) have naming violations")
            print("   Run with --json for machine-readable output")
        else:
            print("✅ All files pass naming validation")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate test file naming conventions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate all files
    python3 validate_naming.py --all

    # Validate specific file
    python3 validate_naming.py --file tests/unit/TC-UT-086_component.py

    # Validate by level
    python3 validate_naming.py --level UT
    python3 validate_naming.py --level IT

    # JSON output for CI/CD
    python3 validate_naming.py --all --json

Valid levels: UT (Unit Test), IT (Integration Test), ST (System Test), AT (Acceptance Test)

Part of: Failure-Driven Enforcement Loop
        """,
    )

    parser.add_argument("--file", "-f", help="Validate specific file")
    parser.add_argument("--all", "-a", action="store_true", help="Validate all test files")
    parser.add_argument(
        "--level", "-l", choices=["UT", "IT", "ST", "AT"], help="Validate by test level"
    )
    parser.add_argument("--json", "-j", action="store_true", help="JSON output for CI/CD")
    parser.add_argument("--directory", "-d", help="Directory to validate (default: tests/)")

    args = parser.parse_args()

    # Initialize validator
    validator = NamingValidator()

    # Determine what to validate
    if args.file:
        # Validate specific file
        filepath = Path(args.file)
        results = [validator.validate_filename(filepath)]

    elif args.level:
        # Validate by level
        directory = Path(args.directory) if args.directory else None
        results = validator.validate_by_level(args.level, directory)

    elif args.all:
        # Validate all
        directory = Path(args.directory) if args.directory else None
        results = validator.validate_all(directory)

    else:
        # Default: validate all
        results = validator.validate_all()

    # Print results
    validator.print_results(results, args.json)

    # Exit with error code if any failures
    invalid_count = sum(1 for r in results if not r.get("valid", False))
    if invalid_count > 0:
        exit(1)


if __name__ == "__main__":
    main()
