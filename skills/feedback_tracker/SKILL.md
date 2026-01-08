---
name: "failure_tracker"
description: "Detect recurring error patterns and encode them into enforceable rules. Use this for Learning from Feedback, Mistake Pattern Detection, Skill Update Suggestions, Avoiding Repeated Mistakes, Continual Learning, Self-Improving Skills, or Adaptive Agent Optimization. Core primitive of the Failure-Driven Enforcement Loop."
version: 1.0.0
created: 2025-01-08
updated: 2025-01-08
allowed-tools: [read, write, bash, grep, glob, python3]
---

# Skill: Failure-Driven Feedback Tracker

**Type:** Primitive (Core Loop Component)
**Status:** Production-ready

## Purpose

The **Feedback_Tracker** is the first primitive in the Failure-Driven Enforcement Loop.

**It does ONE thing:**
1. Detects when the SAME error happens MULTIPLE times
2. Quantifies the frequency (e.g., "127 files")
3. Generates a rule change suggestion

This is **not**:
- ❌ A generic logger
- ❌ A retrospective notes system
- ❌ A metrics dashboard

This is **pattern detection for enforcement**.

## The Loop Position

```
FAILURE OBSERVED (somewhere in the system)
         │
         ▼
┌─────────────────────┐
│  Feedback_Tracker   │ ← You are here
│  • Detects pattern  │   Detects recurring errors
│  • Quantifies count │   Quantifies frequency
│  • Suggests rule    │   Generates rule change
└─────────┬───────────┘
          │
          ▼
RULE ENFORCED (by Traceability Enforcer)
          │
          ▼
GAPS VISUALIZED (by Tree Analyzer)
          │
          ▼
FEWER FAILURES → Loop continues
```

## Workflow

### Phase 1: Log a Failure

**Trigger:** You notice an error that should not happen again.

```bash
# Interactive mode (recommended)
python3 scripts/log_feedback.py --interactive

# Non-interactive mode
python3 scripts/log_feedback.py \
  --type mistake \
  --context "pytest fixture placed before import pytest" \
  --feedback "All imports must come before @pytest.fixture decorators" \
  --category Testing \
  --severity high
```

**Log Format (JSONL - append-only):**
```jsonl
{"timestamp": "2025-01-08T10:30:00", "type": "mistake", "context": "...", "feedback": "...", "category": "Testing", "severity": "high"}
```

**Required Fields:**
- `timestamp`: ISO8601
- `type`: mistake | repetition | clarification
- `context`: What went wrong
- `feedback`: The correction
- `category`: Testing | Architecture | Security | Performance | API | Naming | Documentation
- `severity`: low | medium | high

---

### Phase 2: Detect Patterns

**Trigger:** Weekly or after 10+ feedback entries.

```bash
# Analyze all feedback
python3 scripts/analyze_patterns.py

# Analyze specific category
python3 scripts/analyze_patterns.py --category Testing

# Weekly report
python3 scripts/analyze_patterns.py --weekly
```

**Pattern Detection Criteria:**
- **Frequency:** ≥3 similar corrections
- **Consistency:** Same pattern across multiple entries
- **Severity:** High severity = higher priority

---

### Phase 3: Generate Rule Suggestion

**Output:** `skill_update_suggestions.md`

```markdown
# Skill Update Suggestions

**Generated:** 2025-01-08T10:00:00
**Based on:** 12 feedback entries

## Testing Category - HIGH Priority

**Pattern detected:** 5 corrections related to "pytest fixture before import"
**Frequency:** 5/10 sessions (50%)
**Severity:** HIGH (causes NameError)

**Examples:**
- "pytest fixture placed before import - NameError"
- "All decorators must have imports defined first"
- "@pytest.fixture at line 1 but pytest not imported"

**Suggested Update:**
Add to TDD skill:

```markdown
## ⚠️ CRITICAL: Fixture Placement

pytest fixtures MUST be placed AFTER all imports.

# ❌ WRONG
@pytest.fixture
def mode():
    return 'SIMULATION'

import pytest

# ✅ CORRECT
import pytest

@pytest.fixture
def mode():
    return 'SIMULATION'
```

**Confidence:** HIGH (consistent pattern, 50% frequency)
**Status:** NEEDS_REVIEW
```

---

### Phase 4: Human Review & Update

**CRITICAL:** NEVER automatic overwrites!

**Process:**
1. Review: Read `skill_update_suggestions.md`
2. Approve/Reject: For each suggestion, decide
3. Update: Edit the relevant skill
4. Commit: Git commit with evidence
5. Track: Log in update history

**Safety Rules:**
- ⚠️ NEVER automatic overwrites
- ⚠️ Confidence threshold: ≥3 occurrences
- ⚠️ Version control: Git commit after each update
- ⚠️ Rollback capability: Keep history

---

## Categories

The Feedback_Tracker supports 7 categories:

| Category | Examples |
|----------|----------|
| **Testing** | Fixture placement, private method access, missing validates |
| **Architecture** | Dependency violation, god class, DDD violation |
| **Security** | Plain password, SQL injection, GDPR violation |
| **Performance** | N+1 query, cache invalidation |
| **API** | REST violation, missing versioning |
| **Naming** | Wrong test prefix, missing requirement ID |
| **Documentation** | Missing docstring, unclear comment |

---

## Scripts

### log_feedback.py

**Purpose:** CLI tool for structured feedback logging

**Usage:**
```bash
# Interactive mode (easiest)
python3 scripts/log_feedback.py --interactive

# Non-interactive
python3 scripts/log_feedback.py \
  --type mistake \
  --context "TC-UT test used ._private" \
  --feedback "Use public API, not private methods" \
  --category Testing \
  --severity high

# Help
python3 scripts/log_feedback.py --help
```

**Features:**
- Append-only (never overwrite logs)
- Auto-generate session ID
- Validate required fields
- ISO8601 timestamp

---

### analyze_patterns.py

**Purpose:** Pattern detection and suggestion generation

**Usage:**
```bash
# Analyze all feedback
python3 scripts/analyze_patterns.py

# Analyze specific category
python3 scripts/analyze_patterns.py --category Testing

# Custom threshold
python3 scripts/analyze_patterns.py --min-frequency 5

# Weekly report
python3 scripts/analyze_patterns.py --weekly
```

**Algorithm:**
1. Parse `logs/feedback.jsonl`
2. Group by category
3. Find patterns via regex matching
4. Calculate frequency and severity
5. Generate suggestions (≥3 occurrences = pattern)
6. Write `skill_update_suggestions.md`

**Output:** Markdown file with suggestions (sorted by priority)

---

## Integration Points

### Upstream: Where Failures Come From

| Source | Trigger | Command |
|--------|---------|---------|
| CI/CD failure | Test fails | `pytest && python3 log_feedback.py --type mistake ...` |
| Code review | Human correction | `python3 log_feedback.py --interactive` |
| Manual check | Pattern noticed | `python3 log_feedback.py --type repetition ...` |

### Downstream: Where Rules Go

| Target | Action |
|--------|--------|
| Traceability Enforcer | Validates naming patterns |
| Tree Analyzer | Shows gaps in enforcement |
| Skills | Updated with new rules |

---

## Metrics

Track effectiveness over time:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pattern Detection Rate | 100% | All repeated errors detected |
| False Positive Rate | <10% | Patterns that aren't real |
| Recurrence Rate | <10% | Patterns that return after fix |
| Improvement | 50% reduction | Corrections per week |

---

## Anti-Patterns (What This Is NOT)

### ❌ NOT a Generic Logger

```python
# ❌ WRONG: Just storing data
def log(message):
    file.write(message)

# ✅ CORRECT: Pattern detection built-in
def analyze():
    patterns = detect_recurring_errors()
    if len(patterns) >= 3:
        generate_rule_suggestion()
```

### ❌ NOT a Retrospective Tool

```python
# ❌ WRONG: Weekly meeting notes
def retrospective():
    team_discusses_mistakes()
    writes_notes_in_wiki()

# ✅ CORRECT: Automated pattern detection
def detect_patterns():
    errors = load_all_errors()
    recurring = find_recurring(errors)
    suggest_rules(recurring)
```

### ❌ NOT a Metrics Dashboard

```python
# ❌ WRONG: Just showing numbers
def dashboard():
    show("127 errors this week")

# ✅ CORRECT: Actionable suggestions
def suggest_rules():
    patterns = find_patterns()
    if patterns:
        return generate_rule_suggestions(patterns)
```

---

## Example: End-to-End Flow

### Day 1-3: Mistake Detection

```
Developer writes test with fixture before import.
Error: NameError: name 'pytest' is not defined

Developer runs:
python3 scripts/log_feedback.py \
  --type mistake \
  --context "pytest fixture before import" \
  --feedback "All imports must come before fixtures" \
  --category Testing \
  --severity high
```

### Day 4-7: More of the Same

```
Same error happens again.
Developer logs feedback again.

After 5 similar logs...
```

### Friday: Pattern Analysis

```bash
python3 scripts/analyze_patterns.py
```

**Output: skill_update_suggestions.md**
```
- Testing category: Add fixture placement warning
- Priority: HIGH
- Occurrences: 5
```

### Week 2: Human Review

```
Developer reviews suggestion:
  "Add fixture warning: ✅ APPROVED"

Developer edits TDD skill, adds warning section.

Git commit:
  "feat(TDD): Add pytest fixture placement warning based on feedback (5x)"
```

### Week 3+: Behavior Changed

```
New tests follow pattern.
No more fixture placement errors.
Feedback_Tracker detects: 0 new occurrences.
Loop complete!
```

---

## Troubleshooting

### No patterns detected
**Cause:** Less than 3 similar feedback entries
**Solution:** Continue logging, or lower threshold:
```bash
python3 analyze_patterns.py --min-frequency 2
```

### Too many false positives
**Cause:** Pattern matching too broad
**Solution:** Refine context in feedback logs, be more specific

### Suggestions not implemented
**Cause:** Human review bottleneck
**Solution:** Schedule weekly review time

---

## See Also

- [LOOP_EXPLANATION.md](../LOOP_EXPLANATION.md) - System overview
- [CONTRACTS.md](../CONTRACTS.md) - Component specifications
- [Tree Analyzer skill](./gap_visualizer/) - Gap visualization primitive
- [Traceability Enforcer skill](./traceability_enforcer/) - Rule enforcement primitive

---

**Version:** 1.0.0
**Last Updated:** 2025-01-08
**Type:** Primitive (Core Loop Component)
**Status:** Production-ready
