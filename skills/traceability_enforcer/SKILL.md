---
name: "traceability_enforcer"
description: "Validate naming conventions that encode traceability and enforce bidirectional links. Use this for Naming Validation, Requirement ID Checking, Bidirectional Links, Test-Requirement Mapping, or CI/CD Gates. Core primitive of the Failure-Driven Enforcement Loop."
version: 1.0.0
created: 2025-01-08
updated: 2025-01-08
allowed-tools: [read, write, bash, grep, glob, python3]
---

# Skill: Traceability Enforcer

**Type:** Enforcer (Loop Component)
**Status:** Production-ready

## Purpose

The **Traceability Enforcer** is the second component in the Failure-Driven Enforcement Loop.

**It does TWO things:**
1. Validates naming patterns (e.g., `TC-UT-086_component.py`)
2. Verifies bidirectional links exist (requirement ↔ test)

This is **not**:
- ❌ A style guide (naming is about traceability, not style)
- ❌ A compliance checkbox (violations fail CI/CD)
- ❌ Optional (it's enforced automatically)

## The Loop Position

```
FAILURE OBSERVED (somewhere in the system)
         │
         ▼
┌─────────────────────┐
│  Feedback_Tracker   │ ← Detects recurring errors
│  • Detects pattern  │
│  • Quantifies count │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Traceability       │ ← You are here
│  Enforcer           │   Validates naming + links
│  • Validates naming │
│  • Checks links     │
└─────────┬───────────┘
          │
          ▼
GAPS VISUALIZED (by Tree Analyzer)
          │
          ▼
FEWER FAILURES → Loop continues
```

## Naming Convention

### Test Files

```
TC-{LEVEL}-{ID}_{component}.py
     │     │     │
     │     │     └─ Human-readable component name
     │     └─ Numeric ID (1, 2, 3...)
     └─ Test Level: UT | IT | ST | AT

Examples:
- TC-UT-086_component.py      (Unit Test)
- TC-IT-023_integration.py    (Integration Test)
- TC-ST-001_system.py         (System Test)
- TC-AT-012_acceptance.py     (Acceptance Test)
```

### Requirement Files

```
REQ-{LEVEL}-{ID}.md
   │     │     │
   │     │     └─ Numeric ID (1, 2, 3...)
   │     └─ Requirement Level: REQ | SW-REQ | SYS-REQ | US
   └─ Prefix: REQ

Examples:
- REQ-001_requirements.md
- SW-REQ-086_component.md
- SYS-REQ-001_authentication.md
- US-A1_user_login.md
```

### Why Naming Matters

**Naming is not cosmetic. Naming is enforcement.**

| Without Naming | With Naming |
|----------------|-------------|
| "test_component.py" → What does it test? | "TC-UT-086_component.py" → Tests SW-REQ-086 |
| "Make sure tests trace to requirements" | Filename encodes the trace |
| Human review required | Automated validation |
| Drift happens | Violations fail CI/CD |

## Bidirectional Links

Every test MUST link to its requirement, and every requirement MUST link to its tests.

### Test File (links TO requirement)

```python
"""
TC-UT-086: Component functionality

Validates: SW-REQ-086 (Component functionality)
Level: Unit Test (TC-UT)

Traceability: SW-REQ-086 → SYS-REQ-001 → US-A1
"""
```

### Requirement File (links TO test)

```yaml
---
id: SW-REQ-086
title: Component functionality
traced_from: SYS-REQ-001
tested_by:
  - TC-UT-086_component.py
---
```

### Validation Rules

| Check | Requirement | Result |
|-------|-------------|--------|
| Naming format | `TC-{LEVEL}-{ID}_{name}.py` | PASS/FAIL |
| ID extraction | ID must be parseable | PASS/FAIL |
| Requirement exists | Corresponding REQ file exists | PASS/FAIL |
| Link forward | Requirement has `tested_by:` | PASS/FAIL |
| Link backward | Test has `Validates:` | PASS/FAIL |

## Workflow

### Phase 1: Validate Naming

```bash
# Validate all test files
python3 scripts/validate_naming.py --all

# Validate specific file
python3 scripts/validate_naming.py --file tests/unit/TC-UT-086_component.py

# Validate by level
python3 scripts/validate_naming.py --level UT
```

**Output:**
```
Validating: tests/unit/TC-UT-086_component.py
✅ PASS: Valid naming format
✅ PASS: ID extracted (086)
✅ PASS: Requirement exists (SW-REQ-086)

Validating: tests/unit/test_component.py
❌ FAIL: Invalid naming format
❌ FAIL: Missing TC- prefix
❌ FAIL: Missing level identifier
```

---

### Phase 2: Validate Links

```bash
# Validate all bidirectional links
python3 scripts/validate_links.py --all

# Validate specific requirement
python3 scripts/validate_links.py --requirement SW-REQ-086
```

**Output:**
```
Validating: SW-REQ-086
✅ PASS: tested_by field exists
✅ PASS: TC-UT-086_component.py listed
✅ PASS: Test file contains Validates: SW-REQ-086
✅ PASS: Bidirectional link confirmed

Validating: SW-REQ-087
❌ FAIL: tested_by field empty
❌ FAIL: No test files listed
❌ FAIL: No backward link found
```

---

### Phase 3: CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/validation.yml
name: Traceability Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate Naming
        run: python3 scripts/validate_naming.py --all

      - name: Validate Links
        run: python3 scripts/validate_links.py --all
```

**Result:** PR fails if traceability violations exist.

---

## Scripts

### validate_naming.py

**Purpose:** Validate filename patterns

**Usage:**
```bash
# Validate all files
python3 scripts/validate_naming.py --all

# Validate specific file
python3 scripts/validate_naming.py --file tests/unit/TC-UT-086.py

# Validate by level
python3 scripts/validate_naming.py --level UT  # Unit tests only
python3 scripts/validate_naming.py --level IT  # Integration tests only
python3 scripts/validate_naming.py --level ST  # System tests only
python3 scripts/validate_naming.py --level AT  # Acceptance tests only

# JSON output (for CI/CD)
python3 scripts/validate_naming.py --all --json
```

**Validation Checks:**
1. Filename matches `TC-{LEVEL}-{ID}_{name}.py`
2. Level is valid (UT, IT, ST, AT)
3. ID is numeric
4. Requirement file exists (derived from ID)

---

### validate_links.py

**Purpose:** Validate bidirectional links

**Usage:**
```bash
# Validate all links
python3 scripts/validate_links.py --all

# Validate specific requirement
python3 scripts/validate_links.py --requirement SW-REQ-086

# Validate specific test
python3 scripts/validate_links.py --test TC-UT-086_component.py

# JSON output (for CI/CD)
python3 scripts/validate_links.py --all --json
```

**Validation Checks:**
1. Requirement has `tested_by:` field
2. Listed test files exist
3. Test file has `Validates:` or `Tests:` docstring
4. Links are bidirectional (both directions exist)

---

## Integration Points

### Upstream: Where Rules Come From

| Source | Action |
|--------|--------|
| Feedback_Tracker | Detects naming violations → suggests naming rule |
| Tree Analyzer | Shows which files fail naming validation |
| Human Review | Approves/rejects naming rules |

### Downstream: Where Enforcement Goes

| Target | Action |
|--------|--------|
| CI/CD | Fails build on violations |
| Tree Analyzer | Uses validated files for chain visualization |
| Developer | Receives immediate feedback |

---

## Examples

### Example 1: Valid Naming

**File:** `tests/unit/TC-UT-086_context_analyzer.py`

```bash
$ python3 scripts/validate_naming.py --file tests/unit/TC-UT-086_context_analyzer.py

✅ PASS: Valid naming format
✅ PASS: Level: UT (Unit Test)
✅ PASS: ID: 086
✅ PASS: Requirement exists: REQ-086_context_analyzer.md
```

**Actions required:** None. File is valid.

---

### Example 2: Invalid Naming

**File:** `tests/unit/test_context.py`

```bash
$ python3 scripts/validate_naming.py --file tests/unit/test_context.py

❌ FAIL: Invalid naming format
❌ Expected: TC-{LEVEL}-{ID}_{name}.py
❌ Found: test_context.py

❌ FAIL: Missing TC- prefix
❌ FAIL: Missing level identifier (UT | IT | ST | AT)
❌ FAIL: Missing numeric ID

RECOMMENDED FIX:
mv tests/unit/test_context.py tests/unit/TC-UT-086_context_analyzer.py
```

**Actions required:** Rename file to match convention.

---

### Example 3: Missing Link

**File:** `requirements/SW-REQ-086.md`

```yaml
---
id: SW-REQ-086
title: Context Analyzer
traced_from: SYS-REQ-002
tested_by: []  # Empty!
---
```

```bash
$ python3 scripts/validate_links.py --requirement SW-REQ-086

❌ FAIL: tested_by field is empty
❌ FAIL: No test files linked

RECOMMENDED FIX:
1. Create test file: tests/unit/TC-UT-086_context_analyzer.py
2. Add to requirement:
   tested_by:
     - TC-UT-086_context_analyzer.py
```

---

## Anti-Patterns

### ❌ NOT About Style

```python
# ❌ WRONG: This is about style, not traceability
def test_component():
    pass

# ✅ CORRECT: This encodes traceability
def test_TC_UT_086_component_functionality():
    pass
```

### ❌ NOT Optional

```python
# ❌ WRONG: Naming is optional
# "We can just remember what tests what"

# ✅ CORRECT: Naming is enforced
# CI/CD fails if naming doesn't match
```

### ❌ NOT One-Way

```python
# ❌ WRONG: One-way link
# Test says: "I test SW-REQ-086"
# But requirement doesn't list the test

# ✅ CORRECT: Bidirectional
# Test says: "I test SW-REQ-086"
# Requirement says: "Tested by TC-UT-086"
```

---

## Troubleshooting

### "Invalid naming format" but I'm following conventions

**Cause:** Different convention detected
**Solution:** Ensure filename matches exactly: `TC-{LEVEL}-{ID}_{name}.py`

### "Requirement file not found"

**Cause:** Requirement file missing or wrong location
**Solution:**
```bash
# Check requirement exists
ls requirements/SW-REQ-086.md

# If missing, create it
touch requirements/SW-REQ-086.md
```

### "tested_by field empty"

**Cause:** Requirement file doesn't list test
**Solution:** Add to requirement YAML:
```yaml
tested_by:
  - TC-UT-086_component.py
```

---

## See Also

- [LOOP_EXPLANATION.md](../LOOP_EXPLANATION.md) - System overview
- [CONTRACTS.md](../CONTRACTS.md) - Component specifications
- [Feedback_Tracker skill](./feedback_tracker/) - Pattern detection primitive
- [Tree Analyzer skill](./gap_visualizer/) - Gap visualization primitive

---

**Version:** 1.0.0
**Last Updated:** 2025-01-08
**Type:** Enforcer (Loop Component)
**Status:** Production-ready
