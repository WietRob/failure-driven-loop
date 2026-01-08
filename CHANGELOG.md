# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-08

### Added
- **Feedback_Tracker** - Detects recurring error patterns via `fdl-log-feedback`
- **Traceability Enforcer** - Validates naming conventions and bidirectional links via `fdl-validate-naming` and `fdl-validate-links`
- **Gap Visualizer** - Visualizes traceability chain gaps via `fdl-tree-analyzer`
- **Pattern Detection** - Analyzes feedback logs to identify recurring issues via `fdl-analyze-patterns`
- **5 CLI Commands** - `fdl-validate-naming`, `fdl-validate-links`, `fdl-log-feedback`, `fdl-analyze-patterns`, `fdl-tree-analyzer`
- **Comprehensive Documentation** - README, LOOP_EXPLANATION, QUICK_START, EXAMPLES, CONTRACTS, CONTRIBUTING, RELEASE_NOTES
- **Installation Tests** - Verification test suite (`TC-UT-001_verification.py`)
- **Trial Package** - Setup script, trial guide, and feedback collection template
- **pyproject.toml** - Full Python package configuration with CLI entry points

### Closed-Loop System
- **End-to-End Loop** - Failure → Feedback → Pattern → Enforcement → Gap → Fewer Failures
- **Automated Pattern Detection** - Detects recurring errors after ≥3 occurrences
- **CI/CD Integration** - All validation commands return exit codes for automation
- **JSON Output** - All commands support `--json` for machine-readable output

### Documentation
- **LOOP_EXPLANATION.md** - System overview with Non-Goals section
- **QUICK_START.md** - 5-minute getting started guide
- **EXAMPLES.md** - Real-world failure scenarios (including failure-first Scenario 0)
- **CONTRACTS.md** - Component specifications
- **RELEASE_NOTES.md** - Professional release announcement
- **CONTRIBUTING.md** - Contribution guidelines and code style

### Trial-Ready
- **TRIAL_SETUP.sh** - One-time environment setup script
- **TRIAL_GUIDE.md** - Facilitator script with agenda and feedback forms
- **TRIAL_FEEDBACK.md** - Structured signal capture template

### Validation
- **Installation Verified** - Package installs via `pip install -e .`
- **CLI Verified** - All 5 commands available and functional
- **Loop Closure Verified** - End-to-end demo executed successfully
- **Dry-Run Tested** - Simulated trial passed all criteria

### Identity Preserved
- **Closed-Loop Learning** - System learns from failures, not instruction
- **Minimal Scope** - 3 primitives + 1 enforcer, no feature creep
- **Failure-First** - Examples start with failures, not theoretical planning
- **Explicit Boundaries** - Non-Goals section prevents misinterpretation

---

[Unreleased]: https://github.com/curaops/failure-driven-loop/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/curaops/failure-driven-loop/releases/tag/v1.0.0
