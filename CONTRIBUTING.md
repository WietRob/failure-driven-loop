# Contributing to Failure-Driven Enforcement Loop

We welcome contributions! This guide explains how to participate.

---

## How to Contribute

### Report a Bug

Found an issue? Please use the **Bug Report** issue template.

Include:
- Command you ran
- Output you got (copy-paste)
- Expected behavior
- Python version
- OS type

### Suggest a Feature

Have an idea? Use the **Feature Request** issue template.

Before suggesting:
1. Read [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md)
2. Check [Non-Goals](./README.md#non-goals) in README
3. Ask: Does this preserve the closed-loop identity?

### Report a Misinterpretation

Misunderstood the system? Use the **Misinterpretation/Docs Confusion** issue template.

**This is valuable feedback!** It helps us clarify messaging.

### Submit Code

Want to fix a bug or add a feature? Here's the process:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Write tests first
   - Keep changes small and focused
   - Preserve the closed-loop identity
4. **Run tests**
   ```bash
   pytest tests/ -v
   ```
5. **Submit a pull request**
   - Describe what you changed
   - Link to related issue
   - Include test output

---

## Development Guidelines

### Code Style

We use:
- **Black** for formatting (100 char line length)
- **Ruff** for linting and import ordering
- **MyPy** for type checking

Run checks:
```bash
black failure_loop/
ruff check failure_loop/
mypy failure_loop/
```

### Testing

All contributions must include tests.

Test naming: `TC-UT-XXX_name.py` (see [TRACEABILITY v3.1](./docs/TRACEABILITY_v3.1.md))

Run tests:
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=failure_loop --cov-report=term-missing

# Specific test
pytest tests/TC-UT-001_verification.py -v
```

### Documentation

If you change behavior, update:
- CLI help text (in script docstrings)
- README (if user-facing)
- Examples (if adding new use cases)

---

## What We're Looking For

We prioritize contributions that:

1. **Preserve the closed-loop identity**
   - Feedback → Pattern → Enforcement → Gap → Fewer Failures

2. **Reduce friction**
   - Faster pattern detection
   - Clearer error messages
   - Simpler installation

3. **Keep scope minimal**
   - Don't add "nice-to-have" features
   - Each component has single responsibility
   - Avoid feature creep

4. **Maintain clarity**
   - Unambiguous output
   - Explicit next steps
   - Clear documentation

---

## What We Avoid

We typically decline contributions that:

1. **Violate Non-Goals**
   - Project management features (use Jira)
   - Test framework features (use pytest)
   - Metrics dashboard features (use Datadog)
   - Observability features (use Sentry)

2. **Break the loop**
   - Remove detection phase
   - Remove enforcement phase
   - Add manual steps

3. **Over-expand scope**
   - Add ImpactAnalyzer prematurely
   - Create new primitives without clear need
   - Add configuration options that complicate setup

---

## Community Guidelines

### Be Constructive

- Focus on the code, not the person
- Assume good intentions
- Explain your reasoning clearly

### Ask Questions

- If something is unclear, ask!
- Questions help us improve docs
- No question is "too basic"

### Respect the Loop

- Remember: This is a closed-loop system
- Changes should strengthen, not weaken, the loop
- If in doubt, ask: "Does this help fewer failures occur?"

---

## Getting Help

- **Issues:** GitHub Issues
- **Documentation:** [LOOP_EXPLANATION.md](./LOOP_EXPLANATION.md), [QUICK_START.md](./docs/QUICK_START.md)
- **Examples:** [EXAMPLES.md](./docs/EXAMPLES.md)

---

## License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

---

**Thank you for contributing! The loop appreciates it.**
