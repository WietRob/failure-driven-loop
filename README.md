# Failure-Driven Enforcement Loop

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/WietRob/failure-driven-loop/blob/master/LICENSE)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](https://github.com/WietRob/failure-driven-loop/actions)

**A failure-driven enforcement loop that learns from repeated mistakes and turns them into enforceable rules.**

---

## What This Is

The Failure-Driven Enforcement Loop is a minimal, closed-loop system that:
1. **Detects recurring failures** — learns from real mistakes
2. **Encodes patterns into rules** — automatic enforcement
3. **Visualizes gaps** — shows exactly what to fix
4. **Repeats** — each cycle produces fewer failures

### What This Is NOT

- ❌ A project management tool (Jira, Asana, Linear)
- ❌ A test framework (pytest, unittest, Jest)
- ❌ A metrics dashboard (Datadog, Grafana, Prometheus)
- ❌ A documentation generator (Sphinx, Javadoc)
- ❌ An observability platform (Sentry, ELK stack)

See [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md) for full details.

---

## Scope: Phase 1 (Complete)

**What's Included (v1.0.0):**

| Component | Type | Purpose |
|-----------|------|---------|
| **Feedback_Tracker** | Primitive | Detects patterns → encodes rules |
| **Traceability Enforcer** | Enforcer | Validates naming + links |
| **Gap Visualizer** | Primitive | Shows gaps → recommends fixes |

**Total:** 3 primitives + 1 enforcer

**What's NOT Included:**

- TDD/ATDD/BDD methodologies (development practices, not loop engine)
- Code review processes (team workflows, not loop engine)
- General refactoring patterns (broad patterns, not loop-specific)
- ImpactAnalyzer (planned for Phase 2, when needed)
- CuraOps framework skills (separate product)

**Why This Scope:**

The loop is **complete and self-sufficient**. Adding more features would dilute its identity as a minimal, failure-driven system.

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for Phase 1 status and future plans (Phase 2: Impact Analysis, Phase 3: Advanced Integration).

---

## Quick Start (2 Minutes)

**Try the loop in 2 minutes:**

```bash
# 1. Detect a naming violation
fdl-validate-naming --file tests/unit/test_auth.py

# 2. Log the failure
fdl-log-feedback \
  --type mistake \
  --context "Wrong filename" \
  --feedback "Use TC-UT-XXX_name.py pattern" \
  --category Naming \
  --severity medium

# 3. Analyze patterns (after 3 similar errors)
fdl-analyze-patterns

# 4. Fix and verify
mv tests/unit/test_auth.py tests/unit/TC-UT-001_auth.py
fdl-validate-naming --file tests/unit/TC-UT-001_auth.py
```

---

## How It Works

```
FAILURE OBSERVED
         ↓
┌─────────────────┐
│  FEEDBACK_TRACKER  ← Detects recurring patterns
│  • Encodes rule change
└─────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TRACEABILITY + NAMING  ← Validates compliance
│  • Fails CI/CD if violations
└─────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GAP_VISUALIZER  ← Shows WHERE broken
│  • Recommends specific fixes
└─────────┬────────┘
         │
         ▼
FEWER FAILURES → LOOP CONTINUES
```

---

## Install

```bash
# From source (dev)
git clone https://github.com/WietRob/failure-driven-loop.git
cd failure-driven-loop
pip install -e .

# Or from Git+PyPI (when PyPI is published)
pip install "git+https://github.com/WietRob/failure-driven-loop@v1.0.0"

# Verify installation
fdl-validate-naming --help
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `fdl-validate-naming` | Validate test file naming conventions |
| `fdl-validate-links` | Validate bidirectional requirement-test links |
| `fdl-log-feedback` | Log failures for pattern detection |
| `fdl-analyze-patterns` | Detect recurring patterns in feedback |
| `fdl-tree-analyzer` | Visualize traceability chain gaps |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md) | System overview (read first) |
| [QUICK_START.md](./docs/QUICK_START.md) | 5-minute getting started guide |
| [EXAMPLES.md](./docs/EXAMPLES.md) | Real-world failure scenarios |
| [CONTRACTS.md](./CONTRACTS.md) | Component specifications |

---

## Adoption Patterns

**Local Development:**
```bash
# Pre-commit hook: validate naming before commit
fdl-validate-naming --all

# Weekly pattern review: analyze and update rules
fdl-analyze-patterns --weekly
```

**CI/CD Integration:**
```yaml
# GitHub Actions example
- name: Validate naming
  run: fdl-validate-naming --all

- name: Validate links
  run: fdl-validate-links --all
```

---

## Requirements

- Python 3.10+
- pyyaml

---

## Contributing

We only accept features that strengthen loop closure. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## License

MIT

---

**The loop is closed. The system learns. Failures decrease.**
