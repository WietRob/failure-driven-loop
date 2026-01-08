#!/usr/bin/env python3
"""
Link Validator for Traceability Enforcer

Validates bidirectional links between requirements and tests.

Usage:
    # Validate all links
    python3 validate_links.py --all

    # Validate specific requirement
    python3 validate_links.py --requirement SW-REQ-086

    # Validate specific test
    python3 validate_links.py --test TC-UT-086_component.py

    # JSON output for CI/CD
    python3 validate_links.py --all --json

Part of: Failure-Driven Enforcement Loop
"""

import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any


class LinkValidator:
    """Validates bidirectional links between requirements and tests."""

    def __init__(self) -> None:
        self.results: List[Dict[str, Any]] = []

    def parse_frontmatter(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Parse YAML frontmatter from markdown file."""
        if not filepath.exists():
            return None

        content = filepath.read_text()

        # Check for YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2:
                try:
                    return yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    return None

        return None

    def validate_requirement(
        self, requirement_id: str, requirements_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Validate a requirement's bidirectional links."""
        result: Dict[str, Any] = {
            "requirement": requirement_id,
            "valid": False,
            "tested_by": [],
            "missing_tests": [],
            "backward_links_found": [],
            "errors": [],
            "recommendation": None,
        }

        if requirements_dir is None:
            requirements_dir = Path(__file__).parent.parent.parent / "requirements"

        # Find requirement file
        req_files = list(requirements_dir.rglob(f"*{requirement_id}*.md"))

        if not req_files:
            result["errors"].append(f"Requirement file not found: {requirement_id}")
            result["recommendation"] = f"Create requirements file with ID: {requirement_id}"
            return result

        req_file = req_files[0]
        frontmatter = self.parse_frontmatter(req_file)

        if frontmatter is None:
            result["errors"].append(f"No frontmatter in {req_file}")
            result["recommendation"] = "Add YAML frontmatter with tested_by field"
            return result

        # Check tested_by field
        tested_by = frontmatter.get("tested_by", [])
        if not tested_by:
            result["errors"].append("tested_by field is empty")
            result["missing_tests"] = []
            result["recommendation"] = "Add test files to tested_by field"
            return result

        if not isinstance(tested_by, list):
            result["errors"].append("tested_by must be a list")
            return result

        result["tested_by"] = tested_by

        # Check each test file
        tests_dir = Path(__file__).parent.parent.parent / "tests"
        for test_file_name in tested_by:
            test_file = tests_dir / test_file_name
            if test_file.exists():
                # Check for Validates docstring
                content = test_file.read_text()
                if (
                    f"Validates: {requirement_id}" in content
                    or f"Tests: {requirement_id}" in content
                ):
                    result["backward_links_found"].append(test_file_name)
                else:
                    result["errors"].append(
                        f"Test {test_file_name} missing Validates: {requirement_id}"
                    )
            else:
                result["missing_tests"].append(test_file_name)
                result["errors"].append(f"Test file not found: {test_file_name}")

        # Determine validity
        if result["missing_tests"]:
            result["valid"] = False
        elif len(result["backward_links_found"]) == len(tested_by):
            result["valid"] = True
        else:
            result["valid"] = False

        return result

    def validate_test(
        self, test_file_name: str, tests_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Validate a test's backward link to requirement."""
        result: Dict[str, Any] = {
            "test": test_file_name,
            "valid": False,
            "requirement_id": None,
            "requirement_found": False,
            "errors": [],
            "recommendation": None,
        }

        if tests_dir is None:
            tests_dir = Path(__file__).parent.parent.parent / "tests"

        test_file = tests_dir / test_file_name

        if not test_file.exists():
            result["errors"].append(f"Test file not found: {test_file}")
            return result

        # Extract requirement ID from file content
        content = test_file.read_text()

        # Look for Validates: or Tests: docstring
        for line in content.split("\n"):
            if line.strip().startswith("Validates:") or line.strip().startswith("Tests:"):
                # Extract requirement ID
                parts = line.split(":")
                if len(parts) >= 2:
                    req_id = parts[1].strip()
                    result["requirement_id"] = req_id

                    # Check if requirement exists
                    requirements_dir = Path(__file__).parent.parent.parent / "requirements"
                    req_files = list(requirements_dir.rglob(f"*{req_id}*.md"))

                    if req_files:
                        result["requirement_found"] = True
                        result["valid"] = True
                    else:
                        result["errors"].append(f"Requirement {req_id} not found")
                        result["recommendation"] = f"Create requirement file: {req_id}"
                    break
        else:
            result["errors"].append("No Validates: or Tests: docstring found")
            result["recommendation"] = 'Add "Validates: REQ-ID" to test docstring'

        return result

    def validate_all(
        self, requirements_dir: Optional[Path] = None, tests_dir: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Validate all bidirectional links."""
        results: List[Dict[str, Any]] = []

        if requirements_dir is None:
            requirements_dir = Path(__file__).parent.parent.parent / "requirements"
        if tests_dir is None:
            tests_dir = Path(__file__).parent.parent.parent / "tests"

        # Validate all requirements
        if requirements_dir.exists():
            for req_file in requirements_dir.rglob("*.md"):
                frontmatter = self.parse_frontmatter(req_file)
                if frontmatter and "id" in frontmatter:
                    result = self.validate_requirement(frontmatter["id"], requirements_dir)
                    results.append(result)

        # Validate all tests
        if tests_dir.exists():
            for test_file in tests_dir.rglob("*.py"):
                result = self.validate_test(test_file.name, tests_dir)
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
        print("LINK VALIDATION RESULTS")
        print(f"{'=' * 60}")
        print(f"Total items: {len(results)}")
        print(f"✅ Valid links: {valid_count}")
        print(f"❌ Missing links: {invalid_count}")
        print()

        # Print invalid first
        invalid_results = [r for r in results if not r.get("valid", False)]
        valid_results = [r for r in results if r.get("valid", False)]

        # Print invalid
        if invalid_results:
            print("❌ INVALID LINKS:")
            print("-" * 60)
            for result in invalid_results:
                item_type = "Requirement" if "requirement" in result else "Test"
                item_id = result.get("requirement", result.get("test", "Unknown"))
                print(f"\n{item_type}: {item_id}")
                for error in result.get("errors", []):
                    print(f"  - {error}")
                if result.get("recommendation"):
                    print(f"  💡 {result['recommendation']}")

        # Print valid (summary)
        if valid_results:
            print(f"\n✅ VALID LINKS ({len(valid_results)} shown as summary):")
            print("-" * 60)
            for result in valid_results[:5]:
                item_type = "Requirement" if "requirement" in result else "Test"
                item_id = result.get("requirement", result.get("test", "Unknown"))
                if "tested_by" in result and result["tested_by"]:
                    print(f"  {item_type} {item_id} → {len(result['tested_by'])} test(s)")
                elif "requirement_id" in result:
                    print(f"  Test {item_id} → {result['requirement_id']}")
            if len(valid_results) > 5:
                print(f"  ... and {len(valid_results) - 5} more")

        print()

        # Summary
        if invalid_count > 0:
            print(f"⚠️  {invalid_count} item(s) have missing links")
            print("   Run with --json for machine-readable output")
        else:
            print("✅ All bidirectional links verified")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate bidirectional links between requirements and tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate all links
    python3 validate_links.py --all

    # Validate specific requirement
    python3 validate_links.py --requirement SW-REQ-086

    # Validate specific test
    python3 validate_links.py --test TC-UT-086_component.py

    # JSON output for CI/CD
    python3 validate_links.py --all --json

Part of: Failure-Driven Enforcement Loop
        """,
    )

    parser.add_argument("--requirement", "-req", help="Validate specific requirement ID")
    parser.add_argument("--test", "-t", help="Validate specific test file")
    parser.add_argument("--all", "-a", action="store_true", help="Validate all links")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output for CI/CD")
    parser.add_argument(
        "--requirements-dir", help="Directory containing requirements (default: requirements/)"
    )
    parser.add_argument("--tests-dir", help="Directory containing tests (default: tests/)")

    args = parser.parse_args()

    # Initialize validator
    validator = LinkValidator()

    # Determine what to validate
    if args.requirement:
        requirements_dir = Path(args.requirements_dir) if args.requirements_dir else None
        results = [validator.validate_requirement(args.requirement, requirements_dir)]

    elif args.test:
        tests_dir = Path(args.tests_dir) if args.tests_dir else None
        results = [validator.validate_test(args.test, tests_dir)]

    elif args.all:
        requirements_dir = Path(args.requirements_dir) if args.requirements_dir else None
        tests_dir = Path(args.tests_dir) if args.tests_dir else None
        results = validator.validate_all(requirements_dir, tests_dir)

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
