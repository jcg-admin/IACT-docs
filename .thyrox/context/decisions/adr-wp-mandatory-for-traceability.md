```yml
created_at: 2026-04-25 23:30:00
project: IACT-docs
decision_area: Governance and Traceability
status: Aprobado
author: NestorMonroy
relates_to: I-001 (DISCOVER before planning)
```

# ADR: Work Package Mandatory for Traceability

## Context

When users request implementation work, they may want to skip or minimize analysis phases (DISCOVER, DIAGNOSE, CONSTRAINTS, STRATEGY) to move directly to execution. This desire is understandable for:
- Urgent fixes
- Well-understood features
- Incremental improvements
- Operational maintenance

However, skipping analysis without proper artifact capture creates loss of traceability and institutional knowledge.

## Decision

**Claude MUST recommend creating a Work Package for ANY implementation request, regardless of phase depth.**

If a user says "just implement X directly", the response is:
1. Create a WP (even if Phase 1 DISCOVER is minimal)
2. Document the rationale (why analysis is being abbreviated)
3. Proceed to execution phases
4. Track artifacts properly

The work is NOT done without a WP — WPs are the unit of traceability and institutional memory in THYROX.

## Rationale

**Traceability requirement:** Every piece of work needs:
- Created timestamp and WP ID (for git history correlation)
- Risk register (even if minimal)
- Exit conditions (phase gates)
- Execution log (what actually happened)
- Lessons learned (what we'd do differently)

**Alternative of "just doing the work" without WP leads to:**
- ❌ Lost context (why this decision was made)
- ❌ No gate validation (work gets merged unreviewed)
- ❌ No lessons (future similar tasks must re-solve the same problem)
- ❌ Untrackable effort (git commits have no WP correlation)
- ❌ No risk mitigation (risks not identified → not managed)

## Examples

### Example 1: Quick bug fix request

**User:** "Just fix the PlantUML path error in test-uc-diagram.rst"

**Claude response:**
> I'll create a minimal WP for this fix to maintain traceability:
> - WP: 2026-04-25-23-30-00-plantuml-path-fix/
> - Phase 1: Risk register (1 risk: path regression)
> - Phase 10: Execute (change file, validate, commit)
> - Phase 11: Track (1 lesson learned)
>
> Then proceed with the fix.

### Example 2: Feature without analysis

**User:** "Add a new domain /gestion/ to the documentation structure"

**Claude response:**
> Before implementing, I'll create a WP to scope this properly:
> - Phase 1 DISCOVER: What goes in /gestion/? Who needs it? What's the structure?
> - Phase 6 PLAN: Scope definition (is it out-of-band from current work?)
> - Phase 8 PLAN EXECUTION: Decompose into file creation steps
> - Phase 10 EXECUTE: Create files, validate build, commit
>
> We can move through these quickly, but we must create the WP.

## Impact

**Cost:** Minimal (5-10 min overhead per WP for Phase 1 DISCOVER synthesis)
**Benefit:** Complete traceability, institutional memory, risk management

This rule replaces ad-hoc "let me just do this" implementations with structured, documented work.

## Alternatives Considered

1. **No WP for small fixes** → REJECTED (breaks traceability)
2. **Phase 1 DISCOVER is optional** → REJECTED (I-001 locked decision requires analysis-first)
3. **Abbreviated WP format for quick work** → ACCEPTED as implementation detail (Phase 1 can be 5 min vs 30 min for large features)

## Related Decisions

- [adr-analyze-first.md](adr-analyze-first.md) — DISCOVER before planning (I-001)
- [adr-arquitectura-orquestacion-thyrox.md](adr-arquitectura-orquestacion-thyrox.md) — WP structure and lifecycle

## Implementation Note

Claude should **proactively recommend** WP creation, not wait for user objection. Treat WP-less implementation requests as incomplete specifications.
