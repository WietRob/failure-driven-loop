#!/usr/bin/env python3
"""
Pattern Analyzer for Failure-Driven Enforcement Loop

Analyzes feedback logs to detect recurring error patterns and generate rule suggestions.

Usage:
    # Analyze all feedback
    python3 analyze_patterns.py

    # Analyze specific category
    python3 analyze_patterns.py --category Testing

    # Set custom threshold
    python3 analyze_patterns.py --min-frequency 5

    # Weekly report mode
    python3 analyze_patterns.py --weekly

Part of: Failure-Driven Enforcement Loop
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


class PatternAnalyzer:
    """Pattern analyzer for failure-driven enforcement loop."""

    # Detection patterns for common error categories
    DETECTION_PATTERNS = {
        # Testing Patterns
        "fixture_before_import": {
            "regex": r"@pytest\.fixture.*before.*import|NameError.*pytest|fixture.*import",
            "category": "Testing",
            "severity": "critical",
            "suggestion": "Add pytest fixture placement warning (imports must come before decorators)",
        },
        "private_method_test": {
            "regex": r"\._\w+|private method|_private|internal implementation",
            "category": "Testing",
            "severity": "high",
            "suggestion": "Emphasize: Never test private methods, only PUBLIC API",
        },
        "blackbox_violation": {
            "regex": r"from src\.|imported.*internal|not black.?box|subprocess missing",
            "category": "Testing",
            "severity": "high",
            "suggestion": "Strengthen BLACK-BOX ONLY rule with more examples",
        },
        "missing_validates": {
            "regex": r"validates:|missing.*validates|no validates field",
            "category": "Testing",
            "severity": "medium",
            "suggestion": "Add validates: field requirement to test templates",
        },
        # Architecture Patterns
        "dependency_violation": {
            "regex": r"dependency.*wrong.*direction|layer.*violation|hexagonal|clean arch",
            "category": "Architecture",
            "severity": "high",
            "suggestion": "Clarify dependency direction rules with diagrams",
        },
        "god_class": {
            "regex": r"god class|too many.*responsibilities|single responsibility|SRP violation",
            "category": "Architecture",
            "severity": "medium",
            "suggestion": "Add God Class anti-pattern detection",
        },
        # Security Patterns
        "plain_password": {
            "regex": r"password.*plain|unhashed|cleartext|not.*encrypted",
            "category": "Security",
            "severity": "critical",
            "suggestion": "Add password hashing requirements prominently",
        },
        "sql_injection": {
            "regex": r"sql.*injection|parameterized.*query|prepared statement",
            "category": "Security",
            "severity": "critical",
            "suggestion": "Emphasize parameterized queries in examples",
        },
        # Performance Patterns
        "n_plus_one": {
            "regex": r"n\+1|n plus one|query.*loop|multiple.*queries|batch",
            "category": "Performance",
            "severity": "high",
            "suggestion": "Add N+1 query pattern detection and solutions",
        },
        # API Patterns
        "rest_violation": {
            "regex": r"rest.*violation|wrong.*http.*method|status code|get.*with.*body",
            "category": "API",
            "severity": "medium",
            "suggestion": "Add REST principles decision tree",
        },
        # Naming Patterns
        "test_naming": {
            "regex": r"TC-[UAS][TI]|test.*naming|wrong.*prefix|naming convention",
            "category": "Naming",
            "severity": "medium",
            "suggestion": "Add naming convention validator script",
        },
        # Traceability Patterns
        "missing_frontmatter": {
            "regex": r"frontmatter|yaml header|metadata.*missing|validates:.*missing",
            "category": "Documentation",
            "severity": "high",
            "suggestion": "Add frontmatter validation checklist",
        },
    }

    def load_feedback_log(self, log_file):
        """Load and parse feedback.jsonl."""
        if not log_file.exists():
            return []

        entries = []
        with open(log_file) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return entries

    def detect_patterns(self, entries, min_frequency=3):
        """Detect patterns using regex matching."""
        pattern_matches = defaultdict(list)

        for entry in entries:
            # Combine context and feedback for pattern matching
            combined_text = f"{entry.get('context', '')} {entry.get('feedback', '')}".lower()

            for pattern_name, pattern_def in self.DETECTION_PATTERNS.items():
                if re.search(pattern_def["regex"], combined_text, re.IGNORECASE):
                    pattern_matches[pattern_name].append(entry)

        # Filter by minimum frequency
        return {k: v for k, v in pattern_matches.items() if len(v) >= min_frequency}

    def analyze_by_category(self, detected_patterns):
        """Group patterns by category."""
        by_category = defaultdict(list)

        for pattern_name, occurrences in detected_patterns.items():
            pattern_def = self.DETECTION_PATTERNS[pattern_name]
            category = pattern_def["category"]
            by_category[category].append(
                {
                    "name": pattern_name,
                    "count": len(occurrences),
                    "severity": pattern_def["severity"],
                    "suggestion": pattern_def["suggestion"],
                }
            )

        # Sort by count within each category
        for category in by_category:
            by_category[category].sort(key=lambda x: x["count"], reverse=True)

        return dict(by_category)

    def generate_report(self, entries, min_frequency=3, weekly_only=False):
        """Generate comprehensive pattern analysis report."""
        # Filter for weekly if requested
        if weekly_only:
            week_ago = datetime.now() - timedelta(days=7)
            entries = [e for e in entries if datetime.fromisoformat(e["timestamp"]) > week_ago]

        if not entries:
            return "No feedback entries found for the specified period."

        detected = self.detect_patterns(entries, min_frequency)
        by_category = self.analyze_by_category(detected)

        # Build report
        report = f"""# Feedback Pattern Analysis Report

**Generated:** {datetime.now().isoformat()}
**Total Entries:** {len(entries)}
**Patterns Detected:** {len(detected)}
**Threshold:** ≥{min_frequency} occurrences
{"**Period:** Last 7 days" if weekly_only else "**Period:** All time"}

## Executive Summary

"""

        # Priority patterns (critical/high severity)
        priority_patterns = []
        for patterns in by_category.values():
            priority_patterns.extend([p for p in patterns if p["severity"] in ["critical", "high"]])

        priority_patterns.sort(key=lambda x: (x["severity"] != "critical", -x["count"]))

        if priority_patterns:
            report += "### 🚨 Priority Patterns Requiring Immediate Attention\n\n"
            for p in priority_patterns[:5]:
                icon = "🔴" if p["severity"] == "critical" else "🟠"
                report += f"- {icon} **{p['name']}** ({p['count']}x)\n"
            report += "\n"

        # Category breakdown
        report += "## Pattern Analysis by Category\n\n"

        for category, patterns in sorted(by_category.items()):
            report += f"### {category} ({len(patterns)} patterns)\n\n"
            report += "| Pattern | Count | Severity | Action |\n"
            report += "|---------|-------|----------|--------|\n"

            for p in patterns[:5]:  # Top 5 per category
                severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                report += f"| {p['name']} | {p['count']} | "
                report += f"{severity_icon.get(p['severity'], '')} {p['severity']} | "
                report += f"{p['suggestion'][:50]}...\n"

            report += "\n"

        # Category impact analysis
        category_impact = Counter()
        for pattern_name, occurrences in detected.items():
            category = self.DETECTION_PATTERNS[pattern_name]["category"]
            category_impact[category] += len(occurrences)

        report += "## Category Impact Analysis\n\n"
        report += "Categories ranked by pattern occurrences:\n\n"
        for category, count in category_impact.most_common():
            report += f"1. **{category}**: {count} pattern occurrences\n"

        # Detailed suggestions
        report += "\n## Detailed Update Suggestions\n\n"

        suggestion_num = 1
        for category, patterns in sorted(by_category.items()):
            if patterns:
                report += f"### {category} Skills\n\n"
                for p in patterns[:3]:  # Top 3 per category
                    report += f"**{suggestion_num}. {p['name']}**\n"
                    report += f"- Occurrences: {p['count']}\n"
                    report += f"- Severity: {p['severity']}\n"
                    report += f"- Action: {p['suggestion']}\n\n"
                    suggestion_num += 1

        # Action items
        report += """## Recommended Actions

1. **Immediate** (Critical Patterns):
   - Review and update skills with critical severity patterns
   - Add prominent warnings for security/testing violations
   - Consider automated pre-commit hooks for pattern prevention

2. **This Week** (High Severity):
   - Update skill documentation for high-frequency patterns
   - Add examples demonstrating correct approaches
   - Create validation scripts where applicable

3. **Next Sprint** (Medium/Low):
   - Refine skill content based on medium severity patterns
   - Consider creating new skills for emerging pattern categories
   - Set up automated weekly pattern analysis

## Tracking Progress

Run weekly analysis to track improvement:
```bash
python3 analyze_patterns.py --weekly --min-frequency 2
```

Compare week-over-week to measure effectiveness of skill updates.
"""

        return report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze feedback patterns for failure-driven enforcement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze all feedback
    python3 analyze_patterns.py

    # Analyze specific category
    python3 analyze_patterns.py --category Testing

    # Weekly report
    python3 analyze_patterns.py --weekly

    # Custom threshold
    python3 analyze_patterns.py --min-frequency 5

Part of: Failure-Driven Enforcement Loop
        """,
    )

    parser.add_argument(
        "--category", "-cat", help="Filter by category (Testing, Architecture, Security, etc.)"
    )
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=3,
        help="Minimum pattern frequency (default: 3)",
    )
    parser.add_argument("--weekly", action="store_true", help="Analyze only last 7 days")
    parser.add_argument("--output", default="skill_update_suggestions.md", help="Output file path")

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = PatternAnalyzer()

    # Load feedback
    log_file = Path(__file__).parent.parent / "logs" / "feedback.jsonl"
    entries = analyzer.load_feedback_log(log_file)

    if not entries:
        print("No feedback entries found. Start logging feedback first!")
        print("Run: python3 scripts/log_feedback.py --interactive")
        return

    # Filter by category if requested
    if args.category:
        entries = [e for e in entries if e.get("category") == args.category]

    # Generate report
    report = analyzer.generate_report(entries, args.min_frequency, args.weekly)

    # Save report
    output_path = Path(__file__).parent.parent / args.output
    output_path.write_text(report)

    # Print summary
    print(f"\n{'=' * 60}")
    print("PATTERN ANALYSIS COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total entries analyzed: {len(entries)}")
    print(f"Report saved to: {output_path}")
    print(f"\nReview {args.output} for detailed suggestions")


if __name__ == "__main__":
    main()
