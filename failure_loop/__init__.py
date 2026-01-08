"""
Failure-Driven Enforcement Loop

A self-correcting engineering system that:
1. Observes failures in real-world development
2. Encodes patterns into enforceable rules
3. Detects violations automatically
4. Visualizes gaps with actionable remediation
5. Repeats - each cycle produces fewer failures

Components:
- feedback_tracker: Detect recurring error patterns
- traceability_enforcer: Validate naming and bidirectional links
- gap_visualizer: Visualize traceability chain gaps

Usage:
    from failure_loop import FeedbackTracker, TraceabilityEnforcer, GapVisualizer

Or via CLI:
    fdl-validate-naming --all
    fdl-log-feedback --interactive
    fdl-tree-analyzer --us US-A1
"""

__version__ = "1.0.0"
