# Quick Start Guide

**Version:** 1.0.0
**Purpose:** Get up and running with the Failure-Driven Enforcement Loop

---

## What You Need

- Python 3.10+
- Git

## Installation

```bash
# Clone or copy the opencode-port directory
cp -r /path/to/opencode-port ~/my-project/

cd ~/my-project
```

## Directory Structure

```
opencode-port/
├── LOOP_EXPLANATION.md      # ← Read this first
├── CONTRACTS.md             # ← Component specifications
├── skills/
│   ├── feedback_tracker/    # ← Detect patterns
│   ├── traceability_enforcer/  # ← Enforce rules
│   └── gap_visualizer/      # ← Find gaps
├── docs/
│   └── EXAMPLES.md          # ← More examples
└── README.md                # ← This file
```

---

## 5-Minute Demo

Let's walk through a complete failure → fix cycle.

### Step 1: Create a Test File (with intentional violation)

```bash
# Create test directory
mkdir -p tests/unit

# Create a test file with naming violation
cat > tests/unit/test_auth.py << 'EOF'
@pytest.fixture
def mode():
    return 'SIMULATION'

"""Test for authentication module."""

import pytest

class TestAuth:
    def test_login(self):
        assert True
EOF
```

### Step 2: Run Naming Validation

```bash
# Check naming convention
python3 skills/traceability_enforcer/scripts/validate_naming.py --all
```

**Output:**
```
============================================================
NAMING VALIDATION RESULTS
============================================================
Total files: 1
✅ Valid: 0
❌ Invalid: 1

❌ INVALID FILES:
------------------------------------------------------------

File: tests/unit/test_auth.py
  - Invalid naming format
  - Expected: TC-{LEVEL}-{ID}_{component}.py
  - Found: test_auth.py
  💡 Rename to match TC-LEVEL-ID_component.py pattern

RECOMMENDED FIX:
mv tests/unit/test_auth.py tests/unit/TC-UT-001_auth.py
```

### Step 3: Fix the Naming

```bash
# Rename the file
mv tests/unit/test_auth.py tests/unit/TC-UT-001_auth.py
```

### Step 4: Run Validation Again

```bash
python3 skills/traceability_enforcer/scripts/validate_naming.py --all
```

**Output:**
```
============================================================
NAMING VALIDATION RESULTS
============================================================
Total files: 1
✅ Valid: 1
❌ Invalid: 0

✅ VALID FILES (1 shown as summary):
  TC-UT-001_auth.py
```

### Step 5: Log the Failure

```bash
# Log what happened
python3 skills/feedback_tracker/scripts/log_feedback.py \
  --type mistake \
  --context "Wrong test filename - missing TC-UT prefix" \
  --feedback "Renamed to TC-UT-001_auth.py" \
  --category Naming \
  --severity medium
```

**Output:**
```
✅ Feedback logged!
   Category: Naming
   Severity: medium
   Type: mistake
   Log: skills/feedback_tracker/logs/feedback.jsonl
```

### Step 6: Analyze Patterns

```bash
# Check for patterns
python3 skills/feedback_tracker/scripts/analyze_patterns.py
```

**Output:**
```
============================================================
PATTERN ANALYSIS COMPLETE
============================================================
Total entries analyzed: 1
Report saved to: skill_update_suggestions.md

Review skill_update_suggestions.md for detailed suggestions
```

### Step 7: Visualize the Gap

```bash
# Create a requirement file
mkdir -p requirements
cat > requirements/SW-REQ-001.md << 'EOF'
---
id: SW-REQ-001
title: Authentication Module
traced_from: SYS-REQ-001
refined_in: []
tested_by: []
---

This requirement covers authentication functionality.
EOF

# Visualize the chain
python3 skills/gap_visualizer/scripts/tree_analyzer.py --sw SW-REQ-001
```

**Output:**
```
============================================================
TRACEABILITY CHAIN: SW-REQ-001
============================================================
❌ SW-REQ-001: Authentication Module
  GAP: No refined_in or tested_by links
REMEDIATION:
1. Add code files to refined_in
2. Add test files to tested_by
```

---

## Complete Workflow

### Daily: Before Committing

```bash
# 1. Check naming
python3 skills/traceability_enforcer/scripts/validate_naming.py --all

# 2. Check links
python3 skills/traceability_enforcer/scripts/validate_links.py --all

# 3. If failures, fix them
#    Then commit
```

### Weekly: Pattern Analysis

```bash
# 1. Analyze feedback
python3 skills/feedback_tracker/scripts/analyze_patterns.py --weekly

# 2. Review suggestions
cat skill_update_suggestions.md

# 3. Update skills if needed
```

### On-Demand: Find Gaps

```bash
# Visualize a requirement
python3 skills/gap_visualizer/scripts/tree_analyzer.py --us US-A1

# JSON output for automation
python3 skills/gap_visualizer/scripts/tree_analyzer.py --us US-A1 --json
```

---

## Common Commands

### Validation

```bash
# Validate all naming
python3 skills/traceability_enforcer/scripts/validate_naming.py --all

# Validate specific file
python3 skills/traceability_enforcer/scripts/validate_naming.py --file tests/unit/TC-UT-001.py

# Validate by level
python3 skills/traceability_enforcer/scripts/validate_naming.py --level UT
```

### Feedback

```bash
# Log feedback (interactive)
python3 skills/feedback_tracker/scripts/log_feedback.py --interactive

# Log feedback (non-interactive)
python3 skills/feedback_tracker/scripts/log_feedback.py \
  --type mistake \
  --context "pytest fixture before import" \
  --feedback "All imports must come before fixtures" \
  --category Testing \
  --severity high

# Analyze patterns
python3 skills/feedback_tracker/scripts/analyze_patterns.py
```

### Gap Analysis

```bash
# Visualize user story
python3 skills/gap_visualizer/scripts/tree_analyzer.py --us US-A1

# Visualize requirement (JSON)
python3 skills/gap_visualizer/scripts/tree_analyzer.py --sw SW-REQ-001 --json
```

---

## Next Steps

1. **Read:** [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md) - Understand the system
2. **Read:** [CONTRACTS.md](./CONTRACTS.md) - See component specifications
3. **Try:** The demo above
4. **Explore:** [EXAMPLES.md](./EXAMPLES.md) - More scenarios

---

**Version:** 1.0.0
**Last Updated:** 2025-01-08
