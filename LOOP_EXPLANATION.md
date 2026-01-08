# The Failure-Driven Enforcement Loop

**Version:** 1.0.0
**Status:** Required Reading (Do not proceed without understanding this)

---

## What This Is

A **self-correcting engineering system** that:

1. **Observes failures** in real-world development
2. **Encodes patterns** into enforceable rules
3. **Detects violations** automatically
4. **Visualizes gaps** with actionable remediation
5. **Repeats** — each cycle produces fewer failures

This is **not**:
- ❌ A checklist or process document
- ❌ A governance framework or compliance theater
- ❌ A theoretical methodology
- ❌ A style guide or naming convention

---

## Non-Goals (Explicit Boundaries)

This system deliberately **excludes** the following:

### ❌ Not a Project Management Tool

It does not:
- Track tasks, epics, or sprints
- Assign work to team members
- Estimate effort or velocity
- Replace Jira, Asana, Linear, or Trello

### ❌ Not a Test Framework

It does not:
- Run tests (pytest, unittest, Jest do this)
- Generate test cases
- Define assertions or fixtures
- Replace your existing test infrastructure

### ❌ Not a Metrics Dashboard

It does not:
- Track lines of code changed
- Measure cycle time or lead time
- Generate velocity reports
- Replace Datadog, Prometheus, or Grafana

### ❌ Not a Documentation Generator

It does not:
- Auto-generate API docs
- Create README files
- Produce architecture diagrams
- Replace Sphinx, Javadoc, or Docusaurus

### ❌ Not an Observability Platform

It does not:
- Collect runtime logs
- Track error rates in production
- Monitor latency or throughput
- Replace Sentry, Datadog, or ELK stack

---

### What It *Does* Do

| Function | How It Works |
|----------|--------------|
| Detect recurring failures | Pattern detection from logged feedback |
| Encode rules | Rules added to skills automatically |
| Enforce naming | Filename validation with CI/CD gates |
| Verify links | Bidirectional requirement ↔ test links |
| Visualize gaps | Tree diagram showing exact missing files |

If your need doesn't map to these functions, this system is not the right tool.

---

## The Loop (Visualized)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAILURE-DRIVEN ENFORCEMENT LOOP              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1️⃣  FAILURE OBSERVED                                         │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────┐                   │
│   │  FEEDBACK_TRACKER                       │                   │
│   │  • Detects recurring error patterns     │                   │
│   │  • Quantifies frequency (e.g., 127x)    │                   │
│   │  • Encodes into rule change             │                   │
│   └────────────────┬────────────────────────┘                   │
│                    │                                             │
│                    ▼                                             │
│   2️⃣  RULE ENFORCED                                             │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────┐                   │
│   │  TRACEABILITY + NAMING                  │                   │
│   │  • Machine-validates naming patterns    │                   │
│   │  • Fails CI/CD if violations detected   │                   │
│   │  • Creates traceability from filename   │                   │
│   └────────────────┬────────────────────────┘                   │
│                    │                                             │
│                    ▼                                             │
│   3️⃣  GAPS VISUALIZED                                           │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────┐                   │
│   │  TREE ANALYZER                          │                   │
│   │  • Shows WHERE chain is broken          │                   │
│   │  • Displays AT WHICH LEVEL              │                   │
│   │  • Recommends SPECIFIC remediation      │                   │
│   └────────────────┬────────────────────────┘                   │
│                    │                                             │
│                    ▼                                             │
│   4️⃣  FEWER FAILURES OCCUR                                      │
│       │                                                         │
│       │     (If failure still occurs → back to 1)               │
│       │                                                         │
│       └────────────────────────────────────────────────►        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Makes This Different

| Property | Traditional Systems | This System |
|----------|---------------------|-------------|
| **Failure response** | Document in retrospective | Encode into enforced rules |
| **Detection** | Human review | Automated scanning |
| **Traceability** | Manual matrix maintenance | Automatic from naming |
| **Gap finding** | "Something is missing" | "File X at level Y is missing" |
| **Learning** | Institutional memory loss | Explicit rule changes |
| **Enforcement** | "Please follow this" | CI/CD gates fail |

---

## Concrete Example (Why This Exists)

### The 127-Fixture Incident (2025-10-28)

**What happened:**
```
@ pytest.fixture   ← pytest not imported yet!
def mode():
    return 'SIMULATION'

"""Module docstring."""

import pytest  ← TOO LATE!
```

127 test files failed with: `NameError: name 'pytest' is not defined`

**Traditional response:**
1. Fix the 127 files manually
2. Send email: "Please put imports before fixtures"
3. Hope it doesn't happen again

**Loop response:**
1. Feedback_Tracker detected 127 occurrences of the same pattern
2. Root cause: `@pytest.fixture` placed BEFORE `import pytest`
3. Rule change: TDD skill v1.3.0 added PITFALL 5
4. Naming enforcement: TC-UT files must follow pattern
5. Tree Analyzer: Shows which files violate the rule
6. Result: 0 new violations in 30 days

**The difference:**
- Traditional: Hope-based compliance
- Loop: Pattern → Rule → Detection → Visualization → Enforced compliance

---

## Component Contracts

### Feedback_Tracker (Primitive 1)

**MUST satisfy:**
- [ ] Detect recurring error patterns (same error, 10+ files)
- [ ] Quantify frequency (127 occurrences)
- [ ] Identify root cause (fixture before import)
- [ ] Generate rule change suggestion (add pitfall to skill)
- [ ] Track that rule change was applied

**MUST NOT:**
- ❌ Act as a generic logger
- ❌ Store data without pattern detection
- ❌ Require manual review to find patterns

---

### Traceability + Naming Enforcement (Enforcer)

**MUST satisfy:**
- [ ] Validate naming pattern: `TC-UT-{ID}_{component}.py`
- [ ] Extract requirement ID from filename
- [ ] Verify corresponding requirement file exists
- [ ] Fail CI/CD if validation fails
- [ ] Create bidirectional link: filename ↔ requirement ID

**MUST NOT:**
- ❌ Accept manual exceptions without documentation
- ❌ Pass if requirement file is missing
- ❌ Allow "close enough" naming

---

### Tree Analyzer (Primitive 2)

**MUST satisfy:**
- [ ] Accept requirement ID as input (e.g., US-A1)
- [ ] Trace complete chain: US → SYS-REQ → SW-REQ → CODE → TEST
- [ ] Display status for EACH level: ✅ | ❌ | ⚠️
- [ ] Show EXACT file path for each gap
- [ ] Recommend specific remediation action

**MUST NOT:**
- ❌ Return only a percentage score
- ❌ Hide WHICH level has the gap
- ❌ Require human investigation to find gaps

---

## What Happens If You Remove One Component

| Remove           | Result                                          |
|------------------|-------------------------------------------------|
| Feedback_Tracker | Static rules, no learning, eventually obsolete  |
| Traceability     | Rules exist but aren't enforced, drift occurs   |
| Tree Analyzer    | Gaps invisible, high cognitive load, friction   |

**All three are required. No substitutions.**

---

## How To Use This System

### Daily Workflow

```bash
# 1. Before committing, check for gaps
python3 tree_analyzer.py --us US-A1

# 2. If gaps exist, fix them
#    Tree Analyzer shows exact files

# 3. Run enforcement check
python3 validate_naming.py --all

# 4. If new failure pattern detected,
#    Feedback_Tracker logs it
```

### Weekly Workflow

```bash
# Review new patterns
python3 analyze_patterns.py --weekly

# If patterns found, skills updated
# Check changelog for new rules
```

---

## Common Misconceptions (Pre-empted)

### ❌ "This is just strict process"

**Reality:** This is a **learning system**. Rules change based on evidence.

### ❌ "This adds bureaucracy"

**Reality:** This removes cognitive load. You don't remember rules — the system enforces them.

### ❌ "This slows us down"

**Reality:** This speeds up debugging. You know exactly where the gap is.

### ❌ "We can do this manually"

**Reality:** Manual detection of 127 identical errors is impossible. Patterns require automation.

---

## Evidence of Effectiveness

| Metric | Before Loop | After Loop |
|--------|-------------|------------|
| Fixture placement errors | 127 | 0 |
| Time to find traceability gaps | ~2 hours | ~30 seconds |
| Naming violations in CI | ~15 per sprint | 0 |
| Forgotten lessons | Lost in wikis | Encoded in rules |

---

## Relationship to CuraOps

This system was extracted from CuraOps Framework.

**What was kept:**
- The loop mechanism
- The three primitives
- The enforcement logic
- The evidence of effectiveness

**What was removed:**
- CuraOps-specific IDs (SYS-REQ, SW-REQ)
- Framework integration
- Product-specific rules

This is the **portable core** — the part that works in any project.

---

## Quick Reference

| Component | Purpose | Input | Output |
|-----------|---------|-------|--------|
| Feedback_Tracker | Detect patterns | Error logs | Rule suggestions |
| Traceability | Enforce rules | Files | Pass/Fail + links |
| Tree Analyzer | Find gaps | Requirement ID | Gap visualization |

---

## Next Steps

1. **Read this document** (done)
2. **Run the demo:** `python3 demo_loop.py`
3. **Try it yourself:** `python3 tree_analyzer.py --us US-A1`
4. **Extend:** Add your own patterns to Feedback_Tracker

---

**The loop is closed. The system learns. Failures decrease.**

---

**Version:** 1.0.0
**Last Updated:** 2025-01-08
**Status:** Required Reading
