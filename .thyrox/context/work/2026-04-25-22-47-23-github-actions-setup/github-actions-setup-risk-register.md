```yml
created_at: 2026-04-25 22:47:23
updated_at: 2026-04-25 22:47:23
project: IACT-docs
work_package: 2026-04-25-22-47-23-github-actions-setup
phase: Phase 1 — DISCOVER
status: Activo
```

# Risk Register — GitHub Actions Setup WP

---

## R-001: Workflow Configuration Error

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Current State:** POTENTIAL

### Description
sphinx-build.yml workflow may fail due to incorrect environment setup, Python version mismatch, or Sphinx extension conflicts.

### Impact
- Build fails on PR, blocking merges
- CI/CD pipeline becomes unreliable
- Reduces confidence in automation

### Mitigation
1. Test workflow locally with act (GitHub Actions emulator)
2. Start with minimal dependencies, add incrementally
3. Use Python 3.11 (matches pyproject.toml requires-python)
4. Document environment dependencies in workflow

### Owner: Phase 10 (EXECUTE)

---

## R-002: Workflow Syntax Errors

**Severity:** LOW  
**Probability:** MEDIUM  
**Current State:** POTENTIAL

### Description
YAML syntax errors in workflow files prevent workflow from running at all.

### Impact
- Workflow fails to run
- GitHub shows syntax error notification
- Minimal impact (workflow just won't execute)

### Mitigation
1. Use GitHub's workflow editor for validation (visual)
2. Test YAML syntax before committing
3. Reference official GitHub Actions docs for correct syntax

### Owner: Phase 8 (PLAN EXECUTION)

---

## R-003: Template Coverage Gaps

**Severity:** LOW  
**Probability:** LOW  
**Current State:** POTENTIAL

### Description
Issue/PR templates may not cover all contribution scenarios, leaving edge cases unaddressed.

### Impact
- Some contributors still provide unstructured information
- Not critical (templates are guidance, not hard requirements)

### Mitigation
1. Create templates for 90% use cases (bug, feature, question)
2. Plan Phase 2 for additional templates if needed
3. Iterate based on real usage

### Owner: Phase 6 (PLAN)

---

## R-004: Cost Overrun Risk

**Severity:** LOW  
**Probability:** LOW  
**Current State:** UNLIKELY

### Description
GitHub Actions usage exceeds free tier estimates, incurring costs.

### Impact
- Unexpected AWS/GitHub charges
- Project budget impact (minimal for docs project)

### Mitigation
1. Monitor usage dashboard monthly
2. Set spending limits in GitHub settings
3. Estimated 50 min/month is <3% of free tier
4. Plan includes cost-conscious workflow design

### Owner: Ongoing (TRACK)

---

## R-005: Branch Protection Issues

**Severity:** MEDIUM  
**Probability:** LOW  
**Current State:** POTENTIAL

### Description
Branch protection rules conflict with workflow, preventing valid PRs from merging.

### Impact
- Valid PRs blocked from merging
- Developers frustrated with CI/CD process
- May bypass protection rules unsafely

### Mitigation
1. Test branch protection rules during Phase 10
2. Start permissive (allow merge without checks), tighten later
3. Document required status checks clearly
4. Provide override process for admins

### Owner: Phase 10 (EXECUTE)

---

## R-006: Sphinx Build Environment Mismatch

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Current State:** POTENTIAL

### Description
Sphinx build on GitHub Actions runner differs from local (missing PlantUML, different Python paths, etc.).

### Impact
- Builds pass locally but fail on CI
- Difficult to debug (environment differences)
- Reduces CI/CD reliability

### Mitigation
1. Use Ubuntu runner (standard, well-documented)
2. Install PlantUML explicitly in workflow
3. Use Ubuntu's standard Python (avoid pyenv complexity)
4. Document exact environment in workflow comments
5. Validate PlantUML + Java availability in workflow

### Owner: Phase 8 (PLAN EXECUTION)

---

## R-007: PlantUML Diagram Compilation Timeout

**Severity:** LOW  
**Probability:** LOW  
**Current State:** UNLIKELY

### Description
Building many PlantUML diagrams on CI runner times out due to slow Java startup.

### Impact
- Workflow times out (>10 min default timeout)
- Build fails on CI despite working locally
- May require rerunning workflow multiple times

### Mitigation
1. Set generous timeout (15-20 min for Sphinx build)
2. Cache Java/PlantUML if possible
3. Optimize PlantUML diagrams for speed
4. Phase 2: Consider splitting large diagram builds

### Owner: Phase 10 (EXECUTE)

---

## R-008: Dependency Conflict in Workflow

**Severity:** MEDIUM  
**Probability:** LOW  
**Current State:** POTENTIAL

### Description
Installing workflow dependencies (pip packages) conflicts with existing environment or breaks build.

### Impact
- Build fails on CI
- Dependency resolution errors
- May require manual package version pinning

### Mitigation
1. Use pyproject.toml (single source of truth)
2. Install with: `pip install -e . --no-deps` for simple setup
3. Test locally first
4. Use dependency caching to speed up subsequent runs

### Owner: Phase 8 (PLAN EXECUTION)

---

## Risk Summary by Phase

| Risk | Phase 1 | Phase 6 | Phase 8 | Phase 10 | Ongoing |
|------|---------|---------|---------|----------|---------|
| R-001 (Config error) | Identify | Plan mitigation | Document | Monitor | Track |
| R-002 (Syntax error) | Identify | Validate YAML | Create/validate | Test | Monitor |
| R-003 (Template gaps) | Identify | Cover 90% | Review coverage | Validate | Iterate |
| R-004 (Cost overrun) | Identify | Budget | Design | Monitor | Track |
| R-005 (Branch protection) | Identify | Plan rules | Avoid conflict | Test | Monitor |
| R-006 (Env mismatch) | Identify | Plan Ubuntu setup | Configure env | Validate | Maintain |
| R-007 (Timeout) | Identify | Budget time | Set timeout | Validate | Monitor |
| R-008 (Dep conflict) | Identify | Design install | Test locally | Validate | Monitor |

---

## Risk Owner & Escalation

**Primary Owner:** Claude (Phase 10 EXECUTE)  
**Escalation Path:** If any risk materializes → Document in error-log → Adjust workflow → Retest

---

**Risk Register Status:** COMPLETE  
**Total Risks Identified:** 8  
**High-risk items:** 0  
**Mitigation coverage:** 100%  
**Date:** 2026-04-25 22:47:23
