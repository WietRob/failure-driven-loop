# Component Contracts

**Version:** 1.0.0
**Purpose:** Exact specifications for each loop component
**Status:** Required for implementation

---

## Contract Format

Each component contract specifies:

| Section | Purpose |
|---------|---------|
| **MUST satisfy** | Non-negotiable requirements |
| **MUST NOT** | Explicit prohibitions |
| **Input** | What the component accepts |
| **Output** | What the component produces |
| **Failure modes** | What happens when contract is violated |

---

## 1. Feedback_Tracker Contract

### Purpose
Detect recurring error patterns in development and encode them into enforceable rules.

### MUST satisfy

#### P1: Pattern Detection
- [ ] Scan error logs for identical/similar errors across multiple files
- [ ] Threshold: 10+ occurrences of same pattern = candidate for rule
- [ ] Ignore one-off errors (noise filtering)

#### P2: Quantification
- [ ] Report exact count: "127 files with fixture-before-import"
- [ ] Report affected files: list of all violating files
- [ ] Report first occurrence: when did this pattern start?

#### P3: Root Cause Identification
- [ ] Analyze error type and context
- [ ] Identify the ANTECEDENT: what caused the pattern?
- [ ] Identify the CONSEQUENCE: what failed as a result?

#### P4: Rule Generation
- [ ] Convert pattern into actionable rule text
- [ ] Example: "pytest fixtures must be placed AFTER all imports"
- [ ] Associate rule with specific skill (TDD, CodeReview, etc.)

#### P5: Change Tracking
- [ ] Track which rules were added in each cycle
- [ ] Version skill when rule added
- [ ] Record evidence: pattern count → rule addition

### MUST NOT

- ❌ Store data without pattern detection (generic logging is forbidden)
- ❌ Require manual review to find patterns (automation required)
- ❌ Accept human exception without automated detection
- ❌ Delete historical patterns (institutional memory)

### Input

```yaml
Error logs from:
- pytest failures
- linting errors
- type checking failures
- CI/CD pipeline failures

Format:
{
  "error_type": "NameError",
  "error_message": "name 'pytest' is not defined",
  "file": "tests/unit/TC-UT-086_component.py",
  "line": 15,
  "timestamp": "2025-10-28T10:00:00Z"
}
```

### Output

```yaml
Pattern Report:
{
  "pattern_id": "PAT-001",
  "error_type": "NameError",
  "root_cause": "pytest.fixture placed before import pytest",
  "occurrence_count": 127,
  "affected_files": ["tests/unit/TC-UT-001.py", "tests/unit/TC-UT-002.py", ...],
  "suggested_rule": "pytest fixtures must be placed AFTER all imports",
  "target_skill": "TDD",
  "priority": "HIGH"
}
```

### Failure Modes

| Mode | Detection | Result |
|------|-----------|--------|
| Pattern threshold too low | <10 occurrences | Noise treated as signal |
| Pattern threshold too high | >10 occurrences | Real patterns missed |
| No root cause analysis | Error message only | Rules too vague |
| No skill association | Generic rule | Rule can't be enforced |

---

## 2. Traceability + Naming Enforcement Contract

### Purpose
Validate that files follow naming conventions that encode traceability, and enforce bidirectional links.

### MUST satisfy

#### P1: Naming Pattern Validation
- [ ] Validate filename matches pattern: `TC-{LEVEL}-{ID}_{component}.py`
- [ ] Extract LEVEL: UT | IT | ST | AT
- [ ] Extract ID: numeric identifier
- [ ] Extract component: human-readable name

#### P2: ID Extraction
- [ ] Parse requirement ID from filename
- [ ] Support formats: TC-UT-086, TC-IT-023, TC-ST-001, TC-AT-012
- [ ] Reject malformed IDs

#### P3: Requirement Existence Check
- [ ] Look up requirement file using extracted ID
- [ ] Format: `requirements/{LEVEL}/TC-{LEVEL}-{ID}.md`
- [ ] Verify requirement file exists and is valid

#### P4: Bidirectional Link Creation
- [ ] Requirement file MUST contain: `tested_by: [TC-{LEVEL}-{ID}]`
- [ ] Test file MUST contain docstring: `Validates: {requirement}`
- [ ] Verify both directions exist

#### P5: CI/CD Integration
- [ ] Return exit code 0 (pass) or 1 (fail)
- [ ] Output list of violations with file paths
- [ ] Block merge if violations exist

### MUST NOT

- ❌ Accept "close enough" naming (strict matching)
- ❌ Pass if requirement file is missing
- ❌ Allow manual override without documentation
- ❌ Continue on error (fail fast)

### Input

```yaml
Files to validate:
- tests/unit/TC-UT-086_component.py
- src/core/component.py
- requirements/software/SW-REQ-086.md
```

### Output

```yaml
Validation Report:
{
  "status": "FAIL",
  "violations": [
    {
      "file": "tests/unit/TC-UT-086_component.py",
      "violation": "Missing tested_by link to SW-REQ-086",
      "expected": "tested_by: [SW-REQ-086]",
      "found": "tested_by: []"
    }
  ],
  "links_created": 0,
  "links_missing": 1
}
```

### Failure Modes

| Mode | Detection | Result |
|------|-----------|--------|
| Missing requirement file | ID can't be looked up | FAIL |
| Missing tested_by field | Field exists but empty | FAIL |
| Missing Validates docstring | Docstring doesn't match | FAIL |
| Malformed filename | Regex doesn't match | FAIL |

---

## 3. Tree Analyzer Contract

### Purpose
Visualize the complete traceability chain for a requirement and identify gaps.

### MUST satisfy

#### P1: Chain Traversal
- [ ] Accept requirement ID (US-A1, SYS-REQ-001, SW-REQ-086, TC-UT-001)
- [ ] Follow chain: US → SYS-REQ → SW-REQ → CODE → TEST
- [ ] Follow bidirectional links in both directions

#### P2: Status Display
- [ ] Show status for EACH level: ✅ (complete), ❌ (missing), ⚠️ (partial)
- [ ] Display parent-child relationships visually
- [ ] Indicate depth: how many levels deep?

#### P3: Gap Localization
- [ ] Show EXACT file path for each gap
- [ ] Indicate WHICH level has the gap
- [ ] Show WHICH link is missing (parent→child or child→parent)

#### P4: Remediation Suggestions
- [ ] For missing CODE: "Create file: src/component.py"
- [ ] For missing TEST: "Create file: tests/unit/TC-UT-XXX.py"
- [ ] For missing link: "Add 'tested_by: [TC-XXX]' to requirement"

#### P5: Multiple Format Output
- [ ] Console (text-based tree)
- [ ] JSON (machine-readable)
- [ ] Markdown (documentation)

### MUST NOT

- ❌ Return only a percentage score
- ❌ Hide which level has the gap
- ❌ Require human investigation to find gaps
- ❌ Accept partial traversal (must complete entire chain)

### Input

```yaml
Command:
  python3 tree_analyzer.py --us US-A1 --format text

Parameters:
  - requirement_id: US-A1
  - format: text | json | markdown
  - max_depth: 5
```

### Output (Text Format)

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
3. Create: requirements/software/SW-REQ-011.md
```

### Output (JSON Format)

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
                {
                  "id": "src/auth/validator.py",
                  "status": "COMPLETE"
                },
                {
                  "id": "tests/unit/TC-UT-010_validator.py",
                  "status": "COMPLETE"
                },
                {
                  "id": "src/auth/hasher.py",
                  "status": "MISSING"
                }
              ]
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

### Failure Modes

| Mode | Detection | Result |
|------|-----------|--------|
| Invalid requirement ID | ID not found | ERROR with suggestion |
| Circular reference | Infinite loop detected | ERROR with path |
| Missing parent | Parent ID doesn't exist | ERROR with context |

---

## 4. Integration Contract (How Components Connect)

### Data Flow

```
Feedback_Tracker
    │
    ▼ (Pattern → Rule)
Traceability Enforcement ───┐
    │                       │
    ▼ (Violations)          │
Tree Analyzer ◄─────────────┘
    │
    ▼ (Gaps)
Human Fixes
    │
    ▼ (No new failures)
Feedback_Tracker (detects improvement)
```

### Checkpoints

| Checkpoint | Component | When | Result |
|------------|-----------|------|--------|
| C1 | Feedback_Tracker | Weekly | Pattern detected? → Rule added |
| C2 | Traceability | Every commit | Naming valid? → Links exist? |
| C3 | Tree Analyzer | On demand | Gaps visible? → Remediation clear |
| C4 | Feedback_Tracker | After fix | Pattern reduced? → Loop complete |

---

## 5. Quality Gates

Each component MUST pass its own tests:

### Feedback_Tracker Tests
```python
def test_pattern_detection_threshold():
    # 9 occurrences → no pattern (below threshold)
    # 10 occurrences → pattern detected
    pass

def test_no_false_positives():
    # Random errors not grouped
    pass
```

### Traceability Enforcement Tests
```python
def test_valid_filename():
    # TC-UT-086_component.py → PASS
    pass

def test_invalid_filename():
    # test_component.py → FAIL
    pass

def test_missing_link():
    # File exists, requirement missing → FAIL
    pass
```

### Tree Analyzer Tests
```python
def test_complete_chain():
    # US-A1 → all children exist → COMPLETE
    pass

def test_gap_visualization():
    # Missing file shown as ❌ GAP
    pass
```

---

**Contracts defined. Implementation can proceed.**

**Next:** Extract Feedback_Tracker skill + scripts
