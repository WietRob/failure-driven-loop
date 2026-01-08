# Internal Trial Guide

**Duration:** 5 minutes setup + 15 minutes demo
**Participants:** 2-3 developers
**Goal:** Validate loop adoption and identify friction points

---

## Before the Trial

### Prerequisites

- Python 3.10+
- 2-3 developers willing to try new tools

### Setup (Do Once)

```bash
cd opencode-port
bash TRIAL_SETUP.sh
```

---

## Trial Agenda

### Phase 1: Introduction (2 minutes)

**Say this:**

> "This is the Failure-Driven Enforcement Loop — a system that learns from our mistakes and prevents recurrence."
>
> "We're testing if it actually works in practice. Your honest feedback is essential."
>
> "The loop starts with failures, not planning. Let's see it in action."

---

### Phase 2: Demo Execution (10 minutes)

**Step 1: Show the problem**

```bash
# Create a naming violation
echo '@pytest.fixture
def mode():
    return "SIMULATION"

"""Test file."""

import pytest

class TestAuth:
    def test_login(self):
        assert True' > tests/unit/test_auth.py

# Run validation
fdl-validate-naming --file tests/unit/test_auth.py
```

**Ask:** "What just happened?"

**Expected answer:** "It caught the wrong filename."

---

**Step 2: Show the loop**

```bash
# Log the failure
fdl-log-feedback \
  --type mistake \
  --context "Wrong test filename" \
  --feedback "Use TC-UT-XXX_name.py pattern" \
  --category Naming \
  --severity medium

# Repeat twice more to trigger pattern detection
fdl-log-feedback --type repetition --context "Another naming violation" --feedback "Files should be TC-UT-XXX" --category Naming --severity medium
fdl-log-feedback --type mistake --context "Third naming violation" --feedback "Must follow pattern" --category Naming --severity medium

# Detect pattern
fdl-analyze-patterns
```

**Ask:** "What just happened?"

**Expected answer:** "It detected a pattern and suggested a rule."

---

**Step 3: Show the fix**

```bash
# Rename the file
mv tests/unit/test_auth.py tests/unit/TC-UT-001_auth.py

# Verify
fdl-validate-naming --file tests/unit/TC-UT-001_auth.py
```

**Ask:** "What just happened?"

**Expected answer:** "The violation is gone. Loop closed."

---

### Phase 3: Quick Questions (3 minutes)

**Ask each participant:**

| Question | Note |
|----------|------|
| 1. "Did you understand the loop?" | ✅ / ❌ |
| 2. "What was the most unclear step?" | Open response |
| 3. "Would you use this daily?" | ✅ / ❌ / 🤔 |
| 4. "What's one thing that could be simpler?" | Open response |

---

## Feedback Collection

### Immediate Feedback Form

```markdown
## Trial Feedback - [DATE]

### Understanding
- [ ] I understood the loop immediately
- [ ] I understood after explanation
- [ ] I still don't understand

### Clarity (1-5)
How clear was each step?
| Step | Clarity (1-5) |
|------|---------------|
| Naming validation | |
| Feedback logging | |
| Pattern detection | |
| Fix application | |

### Adoption
- [ ] I would use this daily
- [ ] I would use it occasionally
- [ ] I would not use this

### Friction Points
What was confusing or difficult?
1. _______________________
2. _______________________
3. _______________________

### Suggestions
How can we improve?
1. _______________________
2. _______________________
```

---

## Success Metrics

### Quantitative

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Understanding rate | ≥80% | "I understood the loop" |
| Adoption willingness | ≥60% | "Would use daily" |
| Time to close loop | ≤2 min | Timer during demo |

### Qualitative

- Documentation gaps identified
- Friction points documented
- Unclear commands flagged

---

## Post-Trial Actions

### Day 1: Consolidate Feedback

1. Collect all forms
2. Identify top 3 friction points
3. Prioritize fixes

### Week 1: Address Issues

1. Update documentation
2. Simplify unclear commands
3. Add examples if needed

### Week 2: Measure Results

1. Re-run demo with same questions
2. Compare understanding rate
3. Decide: Ready for public release?

---

## Troubleshooting

### "Command not found"

```bash
# Ensure package is installed
pip install -e .

# Verify CLI is available
which fdl-validate-naming
```

### "No feedback entries found"

```bash
# Check log directory
ls -la failure_loop/logs/

# Re-run feedback logging
fdl-log-feedback --interactive
```

### "Pattern not detected"

```bash
# Need 3+ similar entries
fdl-log-feedback --type mistake --context "Test 1" ...
fdl-log-feedback --type mistake --context "Test 2" ...
fdl-log-feedback --type mistake --context "Test 3" ...

# Then analyze
fdl-analyze-patterns
```

---

## Trial Output Template

After completing the trial, record:

```markdown
## Trial Results - [DATE]

### Participants
1. [Name] - [Role]
2. [Name] - [Role]
3. [Name] - [Role]

### Understanding
- ✅ Understood immediately: X/3
- ✅ Understood after explanation: Y/3
- ❌ Still confused: Z/3

### Top Friction Points
1. [Issue] - [How many mentioned it]
2. [Issue] - [How many mentioned it]
3. [Issue] - [How many mentioned it]

### Suggested Improvements
1. [Improvement]
2. [Improvement]
3. [Improvement]

### Decision
- [ ] Ready for public release
- [ ] Needs refinements, retry trial
- [ ] Requires major changes

### Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

---

## Contact

Questions? See:
- [README.md](./README.md) - Full documentation
- [QUICK_START.md](./docs/QUICK_START.md) - 5-minute guide
- [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md) - System overview

---

**Good luck! The loop works — now let's prove it.**
