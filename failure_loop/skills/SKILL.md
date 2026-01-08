---
name: "gap_visualizer"
description: "Visualize traceability chain gaps and recommend remediation. Use this for Traceability Gaps, Chain Visualization, Missing Links, Requirement Completeness, or Where-Exactly broken. Core primitive of the Failure-Driven Enforcement Loop."
version: 1.0.0
created: 2025-01-08
updated: 2025-01-08
allowed-tools: [read, write, bash, grep, glob, python3]
---

# Skill: Gap Visualizer (Tree Analyzer)

**Type:** Primitive (Core Loop Component)
**Status:** Production-ready

## Purpose

The **Gap Visualizer** (Tree Analyzer) is the third primitive in the Failure-Driven Enforcement Loop.

**It does ONE thing:**
1. Visualizes the complete traceability chain for a requirement
2. Shows WHERE exactly the chain is broken
3. Recommends SPECIFIC remediation actions

This is **not**:
- ❌ A requirements dashboard (shows only percentages)
- ❌ A documentation tool (shows gaps, not just status)
- ❌ Optional (it's how you find what to fix)

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
│  Traceability       │ ← Enforces naming + links
│  Enforcer           │
│  • Validates naming │
│  • Checks links     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gap Visualizer     │ ← You are here
│  (Tree Analyzer)    │   Shows WHERE gaps are
│  • Visualizes chain │   Recommends fixes
│  • Shows gaps       │
└─────────┬───────────┘
          │
          ▼
FEWER FAILURES → Loop continues
```

## How It Works

### The Traceability Chain

```
US-A1: User Login
├── SYS-REQ-001: Authentication Required ✅
│   ├── SW-REQ-010: Password Validation ✅
│   │   ├── src/auth/validator.py ✅
│   │   │   └── TC-UT-010_validator.py ✅
│   └── SW-REQ-011: Session Management ❌ GAP!
│       └── (missing code file)
└── SYS-REQ-002: GDPR Compliance ✅
    └── SW-REQ-020: Data Protection ✅
        └── (all files present)
```

### What It Shows

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete (all children present) |
| ❌ GAP | Missing (child file/directory not found) |
| ⚠️ PARTIAL | Some children present, some missing |
| ❌ MISSING | Parent requirement doesn't exist |

### Why This Matters

**Most systems show:**
- "Traceability: 85%" (What? Where?)
- "3 missing links" (Which ones?)
- "Gap detected" (Where? How to fix?)

**This system shows:**
- "SW-REQ-011 at line 3 has no code file"
- "TC-IT-023.py missing Validates: clause"
- "Create: src/auth/session.py to complete the chain"

---

## Workflow

### Phase 1: Visualize Chain

```bash
# Visualize a user story
python3 scripts/tree_analyzer.py --us US-A1

# Visualize a system requirement
python3 scripts/tree_analyzer.py --sys SYS-REQ-001

# Visualize a software requirement
python3 scripts/tree_analyzer.py --sw SW-REQ-010
```

**Output (Text Format):**
```
US-A1: User Login Feature
├── SYS-REQ-001: Authentication Required ✅
│   ├── SW-REQ-010: Password Validation ✅
│   │   ├── src/auth/validator.py ✅
│   │   │   └── tests/unit/TC-UT-010_validator.py ✅
│   │   └── src/auth/hasher.py ❌ GAP!
│   │       └── tests/unit/TC-UT-011_hasher.py ⚠️ PARTIAL
│   └── SW-REQ-011: Session Management ❌ MISSING!
└── SYS-REQ-002: GDPR Compliance ✅
    └── ...

REMEDIATION:
1. Create: src/auth/hasher.py (implements SW-REQ-010)
2. Create: tests/unit/TC-UT-011_hasher.py (validates SW-REQ-011)
3. Create: requirements/SW-REQ-011.md
```

---

### Phase 2: Machine-Readable Output

```bash
# JSON output for automation
python3 scripts/tree_analyzer.py --us US-A1 --json

# Markdown output for documentation
python3 scripts/tree_analyzer.py --us US-A1 --markdown
```

**Output (JSON Format):**
```json
{
  "requirement_id": "US-A1",
  "status": "PARTIAL",
  "chain": [
    {
      "id": "US-A1",
      "status": "COMPLETE",
      "children": [
        {
          "id": "SYS-REQ-001",
          "status": "COMPLETE",
          "children": [
            {
              "id": "SW-REQ-010",
              "status": "COMPLETE",
              "children": [
                {"id": "src/auth/validator.py", "status": "COMPLETE"},
                {"id": "tests/unit/TC-UT-010_validator.py", "status": "COMPLETE"}
              ]
            },
            {
              "id": "SW-REQ-011",
              "status": "MISSING"
            }
          ]
        }
      ]
    }
  ],
  "gaps": [
    {
      "level": "CODE",
      "file": "src/auth/hasher.py",
      "parent": "SW-REQ-010"
    }
  ],
  "remediation": [
    "Create: src/auth/hasher.py",
    "Add to requirement: traces_to: [SYS-REQ-001]"
  ]
}
```

---

### Phase 3: CI/CD Integration

Add to your PR checks:

```yaml
# .github/workflows/gap-analysis.yml
name: Gap Analysis

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Gap Analysis
        run: |
          python3 scripts/tree_analyzer.py --all --json > gap_analysis.json
          # Fail if critical gaps found
          if grep -q '"status": "MISSING"' gap_analysis.json; then
            echo "❌ Critical gaps found"
            cat gap_analysis.json
            exit 1
          fi
```

---

## Scripts

### tree_analyzer.py

**Purpose:** Visualize traceability chains and find gaps

**Usage:**
```bash
# Visualize user story
python3 scripts/tree_analyzer.py --us US-A1

# Visualize system requirement
python3 scripts/tree_analyzer.py --sys SYS-REQ-001

# Visualize software requirement
python3 scripts/tree_analyzer.py --sw SW-REQ-010

# Output formats
python3 scripts/tree_analyzer.py --us US-A1 --json        # Machine-readable
python3 scripts/tree_analyzer.py --us US-A1 --markdown    # Documentation

# Analyze all requirements
python3 scripts/tree_analyzer.py --all

# Filter by level
python3 scripts/tree_analyzer.py --level US    # Only user stories
python3 scripts/tree_analyzer.py --level SYS   # Only system reqs
python3 scripts/tree_analyzer.py --level SW    # Only software reqs
```

**Output Formats:**

| Format | Use Case |
|--------|----------|
| text | Terminal output, quick checks |
| json | CI/CD, automation |
| markdown | Documentation, reports |

---

## Chain Traversal

The analyzer follows this chain:

```
User Story (US-A1)
    ↓ traces_to
System Requirement (SYS-REQ-001)
    ↓ architected_by (optional)
Software Requirement (SW-REQ-010)
    ↓ refined_in
Code (src/auth/validator.py)
    ↓ validated_by
Test (tests/unit/TC-UT-010_validator.py)
```

### Required Links

| Link | Required | Description |
|------|----------|-------------|
| US → SYS-REQ | ✅ Required | Every user story must trace to system requirements |
| SYS-REQ → SW-REQ | ✅ Required | System requirements decompose to software requirements |
| SW-REQ → CODE | ✅ Required | Software requirements must be implemented in code |
| CODE → TEST | ✅ Required | Code must be validated by tests |

### Optional Links

| Link | Required | Description |
|------|----------|-------------|
| SYS-REQ → SW-ARCH | ❌ Optional | Only for architectural patterns |

---

## Integration Points

### Upstream: Where Rules Come From

| Source | Action |
|--------|--------|
| Traceability Enforcer | Validates that files exist |
| Feedback_Tracker | Detects missing link patterns |

### Downstream: Where Visualization Goes

| Target | Action |
|--------|--------|
| Developer | Sees exactly what to fix |
| CI/CD | Fails if critical gaps exist |
| Documentation | Generates gap reports |

---

## Examples

### Example 1: Complete Chain

**File:** `tests/unit/TC-UT-010_validator.py`

```python
"""
TC-UT-010: Password Validator

Validates: SW-REQ-010 (Password Validation)
Level: Unit Test (TC-UT)

Traceability: SW-REQ-010 → SYS-REQ-001 → US-A1
"""
```

**Command:**
```bash
$ python3 scripts/tree_analyzer.py --sw SW-REQ-010
```

**Output:**
```
SW-REQ-010: Password Validation
├── src/auth/validator.py ✅
│   └── tests/unit/TC-UT-010_validator.py ✅
└── REMEDIATION: None required (chain complete)
```

---

### Example 2: Missing Code File

**File:** `requirements/SW-REQ-011.md`

```yaml
---
id: SW-REQ-011
title: Session Management
traced_from: SYS-REQ-001
---
```

**Command:**
```bash
$ python3 scripts/tree_analyzer.py --sw SW-REQ-011
```

**Output:**
```
SW-REQ-011: Session Management
├── src/auth/session.py ❌ GAP!
└── tests/unit/TC-UT-011_session.py ❌ GAP!

REMEDIATION:
1. Create: src/auth/session.py
   Add to requirement: refined_in: [src/auth/session.py]
2. Create: tests/unit/TC-UT-011_session.py
   Add to requirement: tested_by: [TC-UT-011_session.py]
```

---

### Example 3: Missing Test

**File:** `src/auth/hasher.py`

```python
"""
Password hasher for authentication.

Implements: SW-REQ-010 (Password Validation)
"""
```

**File:** `requirements/SW-REQ-010.md`

```yaml
---
id: SW-REQ-010
title: Password Validation
traced_from: SYS-REQ-001
refined_in:
  - src/auth/hasher.py
tested_by: []
---
```

**Command:**
```bash
$ python3 scripts/tree_analyzer.py --sw SW-REQ-010
```

**Output:**
```
SW-REQ-010: Password Validation
├── src/auth/hasher.py ✅
│   └── tests/unit/TC-UT-010_hasher.py ❌ GAP!
└── REMEDIATION:
1. Create: tests/unit/TC-UT-010_hasher.py
   Add to requirement: tested_by: [TC-UT-010_hasher.py]
```

---

## Anti-Patterns

### ❌ NOT a Percentage Score

```python
# ❌ WRONG: Just showing 85%
def dashboard():
    return "Traceability: 85%"

# ✅ CORRECT: Shows exactly what's missing
def analyze():
    return {
        "missing": ["src/auth/session.py", "tests/unit/TC-UT-011.py"],
        "remediation": ["Create src/auth/session.py", "..."]
    }
```

### ❌ NOT a One-Way View

```python
# ❌ WRONG: Only shows parent → child
def show_chain():
    print("US-A1 → SYS-REQ-001 → SW-REQ-010")

# ✅ CORRECT: Shows bidirectional and gaps
def show_chain():
    print("US-A1 ✅")
    print("  → SYS-REQ-001 ✅")
    print("    → SW-REQ-011 ❌ GAP!")
```

### ❌ NOT Manual Investigation

```python
# ❌ WRONG: Human must figure out what's missing
def find_gaps():
    human_investigates()

# ✅ CORRECT: Automated gap detection
def find_gaps():
    automated_scan()
    return {"gaps": [...], "remediation": [...]}
```

---

## Troubleshooting

### "Requirement not found"

**Cause:** Requirement file doesn't exist
**Solution:** Create the requirement file with proper frontmatter

### "No code files found"

**Cause:** Code files not in expected locations
**Solution:** Ensure files are in standard locations or configure paths

### "Chain is incomplete but I don't know why"

**Cause:** Missing links between levels
**Solution:** Check frontmatter for:
- `traces_to:` (US → SYS-REQ)
- `refined_in:` (SW-REQ → CODE)
- `tested_by:` (CODE → TEST)

---

## See Also

- [LOOP_EXPLANATION.md](../LOOP_EXPLANATION.md) - System overview
- [CONTRACTS.md](../CONTRACTS.md) - Component specifications
- [Feedback_Tracker skill](./feedback_tracker/) - Pattern detection primitive
- [Traceability Enforcer skill](./traceability_enforcer/) - Rule enforcement primitive

---

**Version:** 1.0.0
**Last Updated:** 2025-01-08
**Type:** Primitive (Core Loop Component)
**Status:** Production-ready
