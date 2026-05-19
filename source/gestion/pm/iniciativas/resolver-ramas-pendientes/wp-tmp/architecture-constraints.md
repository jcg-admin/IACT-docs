```yml
created_at: 2026-04-23 10:40:00
project: IACT-docs
work_package: 2026-04-23-07-04-55-config-review-iact-docs
phase: Phase 4 — CONSTRAINTS
author: claude
status: Borrador
version: 1.0.0
```

# Architecture Constraints — Phase 4 Documentation

## Executive Summary

Phase 3 DIAGNOSE identified 711 Sphinx warnings stemming from **fundamental architectural decoupling** between documentation specification (index.rst toctrees) and implementation (actual source files). This constraint analysis documents the technical, organizational, and strategic boundaries within which Phase 5 STRATEGY must operate.

---

## 1. Technical Constraints

### 1.1 Sphinx Configuration Constraint

**Constraint:** MyST parser enabled but source files overwhelmingly RST-only

```yml
File Distribution:
  .rst files: 345+ (89% of sources)
  .md files:  95+ (11% of sources)
  
conf.py declares:
  extensions: [..., 'myst_parser']
  source_suffix: {'.rst': 'restructuredtext'}
  
Problem:
  .md files processed by myst_parser BUT
  .rst files do NOT cross-link to .md files correctly
  Result: 225 "myst.xref_missing" warnings
```

**Implication:**
- Cannot easily remove MyST without auditing all 95 .md files
- Cannot fully enable MyST without converting .rst→.md comprehensively
- Current state: **Unstable hybrid mode**

**Decision Point for Phase 5:**
- **OPTION A:** Remove MyST, .md files become static assets → 5 min fix, loses Markdown capability
- **OPTION B:** Migrate all docs to single format (prefer RST for code docs, .md for procedural) → 12-14 hour refactor

---

### 1.2 Document Catalog Constraint

**Constraint:** 216 source files exist but are not registered in any toctree

```
Directory Structure Actual:
  source/base_cognitiva/       32 files
  source/requisitos/           78 files
  source/arquitectura_tecnica/ 85 files
  source/normativa/            145 files
  source/gestion/              42 files
  Total: 382 source files

Toctree-Registered Files:
  base_cognitiva/index.rst      ~25 files (78% coverage)
  requisitos/index.rst          ~52 files (67% coverage)
  arquitectura_tecnica/index.rst ~45 files (53% coverage)
  normativa/index.rst           ~95 files (66% coverage)
  gestion/index.rst             ~20 files (48% coverage)
  Total: ~237 files (~62% coverage)

Orphaned: 145+ files (38% of codebase)
```

**Root Cause:** Project structure evolved (new files added) without corresponding index updates

**Implication:**
- **Buildable:** Orphaned files don't break the build (Sphinx warning-only)
- **Not navigable:** Users cannot discover 38% of documentation
- **Search impact:** Orphaned files may not appear in search results
- **Maintenance burden:** Toctree fragmentation grows with each new file

**Decision Point for Phase 5:**
- **OPTION A (Quick):** Create minimal toctrees for orphaned files → 1-2 hours, 90% warning reduction
- **OPTION B (Complete):** Audit each orphaned file, categorize, place strategically → 4-5 hours, 100% coverage + organization improvements

---

### 1.3 Reference Target Constraint

**Constraint:** 46 ambiguous cross-reference targets (UC_RPT vs UC_RPT_*)

```
Example:
  index.rst has:   UC_RPT_01_Consultar_Reporte_Trimestral
  source/ has:     UC_RPT_01 (no trimestral in filename)
  Warning:         Unknown document: 'UC_RPT_01_Consultar_Reporte_Trimestral'
  
Pattern observed:
  - 14 UC_RPT_* references don't exist in source/requisitos/
  - 5 UC_ALR_* references incomplete
  - 4 UC_LOG_* references missing
  - 8 UC_AUD_* references partial
```

**Root Cause:** Specification (UC catalog) pre-dates implementation (actual .rst files)

**Implication:**
- **Quick fix:** Remove/update 46 broken references
- **Better fix:** Either create missing UC files OR remove aspirational references
- **Constraint:** UC catalog is not in scope for this WP (maintained by Business Analyst team)

**Decision Point for Phase 5:**
- Option: Remove aspirational UC references from index.rst → 15 min fix, 46 warnings eliminated

---

## 2. Organizational Constraints

### 2.1 Ownership and Authority

**Constraint:** 95 Markdown files in requisitos_no_funcionales/ owned by RNF-Process team

```
/source/requisitos/requisitos_no_funcionales/
  ├── RNF-PROC-001_PROCESO_SDLC.md
  ├── RNF-PROC-002_METRICAS_PROCESO.md
  └── [other RNF process docs]
  
Status:
  Created by: PMO/RNF team
  Format: Markdown (not RST)
  Ownership: Not this WP's team
  Dependencies: Other projects reference these
```

**Implication:**
- Cannot unilaterally convert .md→.rst (affects other projects)
- Cannot delete (other projects depend)
- Must coordinate with RNF team for any changes

**Decision Point for Phase 5:**
- Configuration option: Treat RNF procedimiento .md files as external assets (solve via MyST or separate build step)

---

### 2.2 Timeline and Resource Constraint

**Constraint:** Two remediation options with different scope/effort

| Aspect | Quick Win (A) | Complete (B) |
|--------|----------|-----------|
| Effort | 2.5 hours | 12-14 hours |
| Warning reduction | ~60% (280 remaining) | ~95% (<50 remaining) |
| Architecture improvement | Minimal | Comprehensive |
| Risk of regressions | Low | Medium |
| Requires coordination | Minimal | High (RNF team) |

**Implication:**
- Phase 5 STRATEGY must choose based on project priorities
- If quick release needed: Option A (2.5h turnaround)
- If quality-first: Option B (multi-day effort)

---

## 3. Strategic Constraints

### 3.1 Project Quality Gate

**Constraint:** Documentation is public-facing (end-user documentation)

**Current State:**
- Build succeeds (functional)
- 711 warnings visible in build log (perception issue)
- 38% of documentation unreachable (user experience issue)
- Hybrid RST/MD (maintainability issue)

**Implication:**
- Warnings visible to developers building docs (psychological impact: "something is broken")
- Users cannot discover 216 files (incomplete product perception)
- Maintainers inherit technical debt (cost of future changes higher)

**Decision Point for Phase 5:**
- Low threshold quality gate: If warnings <100 → Ship with Option A
- High threshold: If <50 warnings needed → Commit to Option B

---

### 3.2 Technology Debt Constraint

**Constraint:** Fixing warnings now prevents larger refactor later

```
Technology Debt Accumulation:
  
Year 1: 711 warnings
  → 50% effort cost on every doc change
  → Maintainers learn to ignore warnings
  → Debt compounds

Year 2: 1000+ warnings
  → Discoverability crisis (new users find wrong docs)
  → Search broken (orphaned files not indexed)
  → Refactor becomes unavoidable but costlier

Cost of delay:
  Fix now:   2.5 - 14 hours (one-time)
  Fix later: 40+ hours (distributed, compound interest)
```

**Implication:**
- Option A now << Option B later
- Option B now << Complete rewrite in 2 years

---

## 4. Constraint Summary for Phase 5

### Hard Constraints (Non-Negotiable)

1. **Cannot convert RNF .md files** without RNF team approval
2. **Cannot remove MyST** without understanding .md file usage
3. **Cannot ignore 216 orphaned files** (user experience impact)

### Soft Constraints (Negotiable with Trade-offs)

1. **UC catalog mismatches** (Quick fix: remove broken references)
2. **Toctree coverage** (Quick fix: add orphaned files; Complete fix: reorganize structure)
3. **Format consistency** (Quick fix: tolerate hybrid; Complete fix: single format)

### Decision Factors for Phase 5

| Factor | Favors A (Quick) | Favors B (Complete) |
|--------|-----------------|-------------------|
| Time budget | <3 hours available | 2+ days available |
| Quality tolerance | 280 warnings acceptable | <50 warnings required |
| Refactor appetite | Minimal changes preferred | Comprehensive ok |
| User impact | Can wait for better UX | Need improved discoverability now |

---

## Next Phase: Phase 5 STRATEGY

**Input:** These 4 constraints + 2 remediation options

**Decision:** 
- Which remediation option (A vs B)?
- Resource allocation?
- Timeline?
- Coordination requirements?

**Output:**
- Strategy statement choosing A or B
- Justification based on constraints
- Risk assessment for chosen path
- Resource/timeline plan

---

**Trazabilidad:** Constraints inform the strategy choice in Phase 5.
Violation of hard constraints will require re-negotiation with stakeholders.
