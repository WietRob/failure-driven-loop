# Roadmap

A breakdown of what's included now and what's planned for future phases.

---

## Current Status: Phase 1 (Complete)

**Phase 1: Minimal Closed-Loop System — Production Ready**

### What's Included (v1.0.0)

| Component | Type | Status |
|-----------|------|--------|
| **Feedback_Tracker** | Primitive | ✅ Complete |
| **Traceability Enforcer** | Enforcer | ✅ Complete |
| **Gap Visualizer** | Primitive | ✅ Complete |

**Total:** 3 primitives + 1 enforcer

### What This Means

The system can now:
1. **Detect recurring failures** — Log them, analyze patterns
2. **Enforce rules automatically** — Naming + link validation
3. **Visualize gaps** — Show exactly what's missing
4. **Close the loop** — Each cycle produces fewer failures

### What's NOT Included (Yet)

| Component | Reason |
|-----------|----------|
| **TDD/ATDD/BDD Skills** | Methodology (not loop engine) |
| **CodeReview Skills** | Review process (not loop engine) |
| **Refactoring Skills** | Refactoring patterns (not loop engine) |
| **ImpactAnalyzer** | Planned for Phase 2 |
| **Framework Skills** | CuraOps-specific (not part of this product) |

---

## Phase 2: Planned (Optional)

**Phase 2: Impact Analysis — When Needed**

### What It Would Add

| Component | Purpose |
|-----------|----------|
| **ImpactAnalyzer** | Analyze change impact before implementation |
| **Safety Rules** | Pre-implementation safety checks |
| **Refactoring Guidance** | When to refactor safely |

### Trigger for Phase 2

Phase 2 starts **only** if users ask:
- "How do I know if this change is safe?"
- "What files will this break?"
- "How do I minimize risk?"

### Not a Priority

Phase 1 is **complete and self-sufficient**. Phase 2 will be added **only if demand exists**.

---

## Phase 3: Planned (Future Enhancement)

**Phase 3: Advanced Integration — Later**

### Potential Enhancements

| Enhancement | Status |
|-------------|----------|
| **OpenCode Plugin** | When demand exists |
| **IDE Integration** | When demand exists |
| **Advanced Metrics** | When demand exists |

### No Timeline

These are **ideas, not commitments**. They'll be considered **only after Phase 1 + 2 are validated by real-world use.

---

## What's NOT Planned (Clarification)

### Not Part of This Product

| Item | Reason |
|-------|----------|
| **CuraOps Framework Skills** | This is a separate product |
| **TDD/ATDD/BDD Methodologies** | Development practices (not loop engine) |
| **Code Review Processes** | Team workflows (not loop engine) |
| **General Refactoring Patterns** | Too broad for this scope |
| **Agent Coordination** | CuraOps-specific feature |
| **Foundation Pattern Enforcement** | CuraOps-specific architecture |

### Why Not Included

This product is a **minimal closed-loop system**. Adding anything that doesn't strengthen the loop would dilute the identity.

---

## Summary

| Phase | Status | What's Included |
|-------|----------|-----------------|
| **Phase 1** | ✅ Complete | Feedback + Enforce + Visualize (3 primitives) |
| **Phase 2** | ⏸ Pending | ImpactAnalyzer (when needed) |
| **Phase 3** | ⏸ Idea | OpenCode/IDE integration (future) |

---

## What This Roadmap Clarifies

1. **Phase 1 is complete** — The loop works end-to-end
2. **Scope is minimal** — 3 primitives + 1 enforcer, nothing more
3. **Future phases are optional** — Will only add if real users need them
4. **Not a skill dump** — This is a focused product, not a collection of 22 skills

---

**The loop is closed. Phase 1 is done. Future phases depend on real-world demand.**
