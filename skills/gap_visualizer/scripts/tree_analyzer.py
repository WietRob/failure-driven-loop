#!/usr/bin/env python3
"""
Tree Analyzer for Gap Visualizer

Visualizes traceability chains and identifies gaps with remediation suggestions.

Usage:
    # Visualize user story
    python3 tree_analyzer.py --us US-A1

    # Visualize system requirement
    python3 tree_analyzer.py --sys SYS-REQ-001

    # Visualize software requirement
    python3 tree_analyzer.py --sw SW-REQ-010

    # Output formats
    python3 tree_analyzer.py --us US-A1 --json
    python3 tree_analyzer.py --us US-A1 --markdown

    # Analyze all
    python3 tree_analyzer.py --all

Part of: Failure-Driven Enforcement Loop
"""

import argparse
import json
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class ChainStatus(Enum):
    """Status of a chain element."""

    COMPLETE = "COMPLETE"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class ChainNode:
    """Node in the traceability chain."""

    id: str
    status: ChainStatus = ChainStatus.UNKNOWN
    title: str = ""
    level: str = ""  # US, SYS, SW, CODE, TEST
    file_path: Optional[Path] = None
    children: List["ChainNode"] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    remediation: List[str] = field(default_factory=list)


class TreeAnalyzer:
    """Analyzes traceability chains and identifies gaps."""

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

    def find_requirement_file(self, req_id: str, requirements_dir: Path) -> Optional[Path]:
        """Find a requirement file by ID."""
        if not requirements_dir.exists():
            return None

        # Search patterns
        patterns = [
            f"*{req_id}*.md",
            f"*{req_id}.md",
        ]

        for pattern in patterns:
            matches = list(requirements_dir.rglob(pattern))
            if matches:
                return matches[0]

        return None

    def check_file_exists(self, filepath: Path) -> bool:
        """Check if a file exists."""
        return filepath.exists()

    def extract_docstring_requirement(self, filepath: Path) -> Optional[str]:
        """Extract requirement ID from file docstring."""
        if not filepath.exists():
            return None

        content = filepath.read_text()

        # Look for Validates: or Tests: in docstring
        for line in content.split("\n"):
            if line.strip().startswith("Validates:") or line.strip().startswith("Tests:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    return parts[1].strip()

        return None

    def build_chain(
        self,
        node_id: str,
        level: str,
        requirements_dir: Path,
        tests_dir: Path,
        code_dir: Path,
        visited: Optional[set] = None,
    ) -> ChainNode:
        """Build the traceability chain for a requirement."""
        if visited is None:
            visited = set()

        # Prevent infinite loops
        if node_id in visited:
            return ChainNode(id=node_id, status=ChainStatus.UNKNOWN, level=level)
        visited.add(node_id)

        node = ChainNode(id=node_id, level=level)

        # Find requirement file
        req_file = self.find_requirement_file(node_id, requirements_dir)

        if req_file:
            node.file_path = req_file
            frontmatter = self.parse_frontmatter(req_file)

            if frontmatter:
                node.title = frontmatter.get("title", "")

                # Determine status based on links
                has_children = False

                # For code files, check tests
                if level == "CODE":
                    test_name = (
                        f"TC-UT-{node_id.split('-')[-1]}_{frontmatter.get('title', 'unknown')}.py"
                    )
                    test_file = tests_dir / test_name

                    if self.check_file_exists(test_file):
                        node.status = ChainStatus.COMPLETE
                        has_children = True

                        # Check backward link
                        docstring_req = self.extract_docstring_requirement(test_file)
                        if docstring_req and docstring_req in node_id:
                            pass  # Link exists
                        else:
                            node.status = ChainStatus.PARTIAL
                            node.gaps.append(f"Test {test_name} missing Validates: {node_id}")
                            node.remediation.append(f'Add "Validates: {node_id}" to {test_name}')
                    else:
                        node.status = ChainStatus.MISSING
                        node.gaps.append(f"Test file not found: {test_name}")
                        node.remediation.append(f"Create: {test_file}")

                # For SW-REQ level
                elif level == "SW":
                    refined_in = frontmatter.get("refined_in", [])
                    tested_by = frontmatter.get("tested_by", [])

                    if refined_in or tested_by:
                        has_children = True

                        # Check code files
                        for code_file in refined_in:
                            code_path = code_dir / code_file
                            if self.check_file_exists(code_path):
                                code_node = self.build_chain(
                                    code_file,
                                    "CODE",
                                    requirements_dir,
                                    tests_dir,
                                    code_dir,
                                    visited.copy(),
                                )
                                node.children.append(code_node)
                            else:
                                missing_node = ChainNode(
                                    id=code_file,
                                    status=ChainStatus.MISSING,
                                    level="CODE",
                                    file_path=code_path,
                                )
                                missing_node.gaps.append(f"Code file not found: {code_file}")
                                missing_node.remediation.append(f"Create: {code_file}")
                                node.children.append(missing_node)

                        # Check test files
                        for test_file in tested_by:
                            test_path = tests_dir / test_file
                            if self.check_file_exists(test_path):
                                test_node = ChainNode(
                                    id=test_file,
                                    status=ChainStatus.COMPLETE,
                                    level="TEST",
                                    file_path=test_path,
                                )
                                node.children.append(test_node)
                            else:
                                missing_node = ChainNode(
                                    id=test_file,
                                    status=ChainStatus.MISSING,
                                    level="TEST",
                                    file_path=test_path,
                                )
                                missing_node.gaps.append(f"Test file not found: {test_file}")
                                missing_node.remediation.append(f"Create: {test_file}")
                                node.children.append(missing_node)

                        # Determine status
                        child_statuses = [c.status for c in node.children]
                        if all(s == ChainStatus.COMPLETE for s in child_statuses):
                            node.status = ChainStatus.COMPLETE
                        elif any(s == ChainStatus.MISSING for s in child_statuses):
                            node.status = ChainStatus.PARTIAL
                        else:
                            node.status = ChainStatus.PARTIAL
                    else:
                        node.status = ChainStatus.MISSING
                        node.gaps.append("No refined_in or tested_by links")
                        node.remediation.append("Add code files to refined_in")
                        node.remediation.append("Add test files to tested_by")

                # For SYS-REQ level
                elif level == "SYS":
                    traces_to = frontmatter.get("traces_to", [])

                    if traces_to:
                        has_children = True

                        for sw_req in traces_to:
                            sw_node = self.build_chain(
                                sw_req, "SW", requirements_dir, tests_dir, code_dir, visited.copy()
                            )
                            node.children.append(sw_node)

                        child_statuses = [c.status for c in node.children]
                        if all(s == ChainStatus.COMPLETE for s in child_statuses):
                            node.status = ChainStatus.COMPLETE
                        elif any(s == ChainStatus.MISSING for s in child_statuses):
                            node.status = ChainStatus.PARTIAL
                        else:
                            node.status = ChainStatus.PARTIAL
                    else:
                        node.status = ChainStatus.MISSING
                        node.gaps.append("No traces_to links")
                        node.remediation.append("Add system requirements to traces_to")

                # For US level
                elif level == "US":
                    traces_to = frontmatter.get("traces_to", [])

                    if traces_to:
                        has_children = True

                        for sys_req in traces_to:
                            sys_node = self.build_chain(
                                sys_req,
                                "SYS",
                                requirements_dir,
                                tests_dir,
                                code_dir,
                                visited.copy(),
                            )
                            node.children.append(sys_node)

                        child_statuses = [c.status for c in node.children]
                        if all(s == ChainStatus.COMPLETE for s in child_statuses):
                            node.status = ChainStatus.COMPLETE
                        elif any(s == ChainStatus.MISSING for s in child_statuses):
                            node.status = ChainStatus.PARTIAL
                        else:
                            node.status = ChainStatus.PARTIAL
                    else:
                        node.status = ChainStatus.MISSING
                        node.gaps.append("No traces_to links")
                        node.remediation.append("Add user story traces")

            else:
                node.status = ChainStatus.MISSING
                node.gaps.append("No frontmatter found")
        else:
            node.status = ChainStatus.MISSING
            node.gaps.append(f"Requirement file not found: {node_id}")

        return node

    def node_to_dict(self, node: ChainNode) -> Dict[str, Any]:
        """Convert ChainNode to dictionary."""
        return {
            "id": node.id,
            "status": node.status.value,
            "title": node.title,
            "level": node.level,
            "children": [self.node_to_dict(c) for c in node.children],
            "gaps": node.gaps,
            "remediation": node.remediation,
        }

    def print_tree(self, node: ChainNode, indent: int = 0, prefix: str = "") -> None:
        """Print tree visualization."""
        # Status icon
        icon = {
            ChainStatus.COMPLETE: "✅",
            ChainStatus.MISSING: "❌",
            ChainStatus.PARTIAL: "⚠️",
            ChainStatus.UNKNOWN: "❓",
        }.get(node.status, "❓")

        # Print node
        print(f"{prefix}{icon} {node.id}: {node.title}")

        # Print gaps
        for gap in node.gaps:
            print(f"{prefix}  GAP: {gap}")

        # Print children
        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = prefix + ("    " if is_last else "│   ")
            connector = "└── " if is_last else "├── "
            self.print_tree(child, indent + 1, child_prefix + connector)

    def print_remediation(self, node: ChainNode) -> None:
        """Print remediation suggestions."""
        if node.remediation:
            print("REMEDIATION:")
            for i, action in enumerate(node.remediation, 1):
                print(f"{i}. {action}")

        for child in node.children:
            self.print_remediation(child)

    def analyze(
        self,
        req_id: str,
        requirements_dir: Path = None,
        tests_dir: Path = None,
        code_dir: Path = None,
        output_format: str = "text",
    ) -> Dict[str, Any]:
        """Analyze a requirement's traceability chain."""
        if requirements_dir is None:
            requirements_dir = Path(__file__).parent.parent.parent / "requirements"
        if tests_dir is None:
            tests_dir = Path(__file__).parent.parent.parent / "tests"
        if code_dir is None:
            code_dir = Path(__file__).parent.parent.parent / "src"

        # Determine level from ID prefix
        if req_id.startswith("US-"):
            level = "US"
        elif req_id.startswith("SYS-"):
            level = "SYS"
        elif req_id.startswith("SW-"):
            level = "SW"
        else:
            level = "UNKNOWN"

        # Build chain
        root = self.build_chain(req_id, level, requirements_dir, tests_dir, code_dir)

        # Output based on format
        if output_format == "json":
            result = self.node_to_dict(root)
            print(json.dumps(result, indent=2))
            return result

        elif output_format == "markdown":
            result = self.node_to_dict(root)
            lines = self.to_markdown(root, 0)
            print("\n".join(lines))
            return result

        else:  # text
            print("\n" + "=" * 60)
            print(f"TRACEABILITY CHAIN: {req_id}")
            print("=" * 60)
            self.print_tree(root)
            print()
            self.print_remediation(root)
            print()

            # Summary
            if root.status == ChainStatus.COMPLETE:
                print("✅ Chain is complete")
            elif root.status == ChainStatus.MISSING:
                print("❌ Chain is missing critical elements")
            else:
                print("⚠️  Chain has gaps (see remediation above)")

            return self.node_to_dict(root)

    def to_markdown(self, node: ChainNode, indent: int) -> List[str]:
        """Convert node to markdown list items."""
        lines = []
        icon = {
            ChainStatus.COMPLETE: "✅",
            ChainStatus.MISSING: "❌",
            ChainStatus.PARTIAL: "⚠️",
            ChainStatus.UNKNOWN: "❓",
        }.get(node.status, "❓")

        lines.append(f"{'  ' * indent}- {icon} **{node.id}**: {node.title}")

        for child in node.children:
            lines.extend(self.to_markdown(child, indent + 1))

        return lines


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Visualize traceability chains and identify gaps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Visualize user story
    python3 tree_analyzer.py --us US-A1

    # Visualize system requirement
    python3 tree_analyzer.py --sys SYS-REQ-001

    # Visualize software requirement
    python3 tree_analyzer.py --sw SW-REQ-010

    # JSON output
    python3 tree_analyzer.py --us US-A1 --json

    # Markdown output
    python3 tree_analyzer.py --us US-A1 --markdown

    # Analyze all requirements
    python3 tree_analyzer.py --all

Part of: Failure-Driven Enforcement Loop
        """,
    )

    parser.add_argument("--us", help="User Story ID (e.g., US-A1)")
    parser.add_argument("--sys", help="System Requirement ID (e.g., SYS-REQ-001)")
    parser.add_argument("--sw", help="Software Requirement ID (e.g., SW-REQ-010)")
    parser.add_argument("--all", action="store_true", help="Analyze all requirements")
    parser.add_argument(
        "--format", "-f", choices=["text", "json", "markdown"], default="text", help="Output format"
    )
    parser.add_argument(
        "--requirements-dir", help="Directory containing requirements (default: requirements/)"
    )
    parser.add_argument("--tests-dir", help="Directory containing tests (default: tests/)")
    parser.add_argument("--code-dir", help="Directory containing code (default: src/)")

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = TreeAnalyzer()

    # Determine what to analyze
    if args.us:
        analyzer.analyze(
            args.us,
            Path(args.requirements_dir) if args.requirements_dir else None,
            Path(args.tests_dir) if args.tests_dir else None,
            Path(args.code_dir) if args.code_dir else None,
            args.format,
        )

    elif args.sys:
        analyzer.analyze(
            args.sys,
            Path(args.requirements_dir) if args.requirements_dir else None,
            Path(args.tests_dir) if args.tests_dir else None,
            Path(args.code_dir) if args.code_dir else None,
            args.format,
        )

    elif args.sw:
        analyzer.analyze(
            args.sw,
            Path(args.requirements_dir) if args.requirements_dir else None,
            Path(args.tests_dir) if args.tests_dir else None,
            Path(args.code_dir) if args.code_dir else None,
            args.format,
        )

    elif args.all:
        print("Analyzing all requirements... (coming soon)")
        print("For now, use --us, --sys, or --sw to analyze specific requirements")

    else:
        print("Error: Must specify --us, --sys, --sw, or --all")
        print("Example: python3 tree_analyzer.py --us US-A1")


if __name__ == "__main__":
    main()
