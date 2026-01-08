# Minimal Demo

**Purpose:** Copy/paste demo showing the failure-driven loop in action.

---

## File Structure

```
examples/minimal/
├── TC-UT-001_naming_violation.py  # Test for naming validation
├── tests/unit/test_auth.py           # File with naming violation
├── requirements/SW-REQ-001.md      # Requirement file
└── README.md                      # This file
```

---

## Quick Demo

**Step 1: Detect violation**
```bash
cd /path/to/failure-driven-loop
python examples/minimal/TC-UT-001_naming_violation.py
```

**Expected output:**
```
✅ Naming violation detected correctly
```

**Step 2: See what went wrong**
```bash
fdl-validate-naming --file examples/minimal/tests/unit/test_auth.py
```

**Expected output:**
```
❌ INVALID FILES:
------------------------------------------------------------
File: examples/minimal/tests/unit/test_auth.py
  - Invalid naming format
  - Expected: TC-{LEVEL}-{ID}_{component}.py
  - Found: test_auth.py
```

**Step 3: Fix the violation**
```bash
mv examples/minimal/tests/unit/test_auth.py \
   examples/minimal/tests/unit/TC-UT-001_auth.py
```

**Step 4: Verify fix**
```bash
fdl-validate-naming --file examples/minimal/tests/unit/TC-UT-001_auth.py
```

**Expected output:**
```
✅ VALID FILES (1 shown as summary):
------------------------------------------------------------
  TC-UT-001_auth.py
✅ All files pass naming validation
```

---

## What This Demonstrates

| Phase | Action | Expected Outcome |
|--------|---------|-----------------|
| 1 | Run validation test | ✅ Violation detected |
| 2 | Check wrong file | ❌ Naming validation fails |
| 3 | Fix filename | File renamed to correct format |
| 4 | Verify fix | ✅ Naming validation passes |

**Result:** The loop closed — failure detected → feedback → pattern → enforcement → fix → fewer failures.
