#!/usr/bin/env python3
"""
Feedback Logger for Failure-Driven Enforcement Loop

Logs recurring errors to enable pattern detection and rule enforcement.

Usage:
    # Interactive mode (recommended)
    python3 scripts/log_feedback.py --interactive

    # Non-interactive mode
    python3 scripts/log_feedback.py --type mistake --context "..." --feedback "..." --category Testing --severity high

    # Help
    python3 scripts/log_feedback.py --help

Part of: Failure-Driven Enforcement Loop
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def log_feedback(correction_type, context, user_feedback, category, severity="medium"):
    """
    Log feedback to JSONL file.

    Args:
        correction_type: mistake | repetition | clarification
        context: What went wrong
        user_feedback: The correction applied
        category: Testing | Architecture | Security | Performance | API | Naming | Documentation
        severity: low | medium | high
    """
    # Ensure logs directory exists
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "feedback.jsonl"

    # Generate session ID (date-based)
    session_id = f"s{datetime.now().strftime('%Y%m%d')}"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "type": correction_type,
        "context": context,
        "feedback": user_feedback,
        "category": category,
        "severity": severity,
    }

    # Append to log (never overwrite)
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print("✅ Feedback logged!")
    print(f"   Category: {category}")
    print(f"   Severity: {severity}")
    print(f"   Type: {correction_type}")
    print(f"   Log: {log_file}")

    return entry


def interactive_mode():
    """Interactive mode for easier logging."""
    print("\n🎯 Failure-Driven Feedback Tracker")
    print("=" * 50)

    # Type
    print("\nCorrection Type:")
    print("  1. mistake       - Something was wrong")
    print("  2. repetition   - Had to repeat the same correction")
    print("  3. clarification - Needed more clarity")
    type_choice = input("\nSelect (1-3): ").strip()
    type_map = {"1": "mistake", "2": "repetition", "3": "clarification"}
    correction_type = type_map.get(type_choice, "mistake")

    # Context
    context = input("\nWhat went wrong? (context): ").strip()
    if not context:
        print("❌ Context is required!")
        return

    # Feedback
    user_feedback = input("\nWhat was the correction?: ").strip()
    if not user_feedback:
        print("❌ Feedback is required!")
        return

    # Category
    print("\nCategory:")
    categories = [
        "Testing",
        "Architecture",
        "Security",
        "Performance",
        "API",
        "Naming",
        "Documentation",
    ]
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    category_choice = input("\nSelect (1-7): ").strip()
    category = (
        categories[int(category_choice) - 1]
        if category_choice.isdigit() and 1 <= int(category_choice) <= 7
        else "Testing"
    )

    # Severity
    print("\nSeverity:")
    print("  1. low     - Minor issue")
    print("  2. medium  - Important")
    print("  3. high    - Critical (e.g., causes failures)")
    severity_choice = input("\nSelect (1-3): ").strip()
    severity_map = {"1": "low", "2": "medium", "3": "high"}
    severity = severity_map.get(severity_choice, "medium")

    # Confirm
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"   Type: {correction_type}")
    print(f"   Context: {context}")
    print(f"   Feedback: {user_feedback}")
    print(f"   Category: {category}")
    print(f"   Severity: {severity}")
    print("=" * 50)

    confirm = input("\nLog this feedback? (y/n): ").strip().lower()
    if confirm == "y":
        log_feedback(correction_type, context, user_feedback, category, severity)
    else:
        print("❌ Cancelled")


def main():
    parser = argparse.ArgumentParser(
        description="Log feedback for failure-driven pattern detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode (recommended)
    python3 scripts/log_feedback.py --interactive

    # Non-interactive
    python3 scripts/log_feedback.py \\
        --type mistake \\
        --context "pytest fixture placed before import" \\
        --feedback "All imports must come before @pytest.fixture decorators" \\
        --category Testing \\
        --severity high

    # Quick log
    python3 scripts/log_feedback.py \\
        --type repetition \\
        --context "Forgot validator" \\
        --feedback "Add to checklist" \\
        --category Testing

Part of: Failure-Driven Enforcement Loop
        """,
    )

    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode (easiest)"
    )
    parser.add_argument(
        "--type", "-t", choices=["mistake", "repetition", "clarification"], help="Correction type"
    )
    parser.add_argument("--context", "-c", help="What went wrong")
    parser.add_argument("--feedback", "-f", help="The correction applied")
    parser.add_argument(
        "--category",
        "-cat",
        choices=[
            "Testing",
            "Architecture",
            "Security",
            "Performance",
            "API",
            "Naming",
            "Documentation",
        ],
        help="Category of the error",
    )
    parser.add_argument(
        "--severity",
        choices=["low", "medium", "high"],
        default="medium",
        help="Severity (default: medium)",
    )

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        interactive_mode()
        return

    # Non-interactive mode - validate required args
    if not all([args.type, args.context, args.feedback, args.category]):
        parser.error("Non-interactive mode requires: --type, --context, --feedback, --category")

    log_feedback(
        correction_type=args.type,
        context=args.context,
        user_feedback=args.feedback,
        category=args.category,
        severity=args.severity,
    )


if __name__ == "__main__":
    main()
