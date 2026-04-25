```yml
created_at: 2026-04-25 22:13:43
updated_at: 2026-04-25 22:13:43
project: IACT-docs
work_package: 2026-04-25-22-13-43-iact-project-state-assessment
phase: Phase 1 — DISCOVER
status: Activo
```

# Risk Register — IACT Project State Assessment WP

---

## R-001: Placeholder Text in Production Documentation

**Severity:** MEDIUM  
**Probability:** HIGH  
**Current State:** MATERIALIZED (confirmed in readme.rst)

### Description
Organization name field still contains template text: "[Nombre de tu Empresa]" (readme.rst:18). Indicates documentation was published without final customization.

### Impact
- External readers perceive documentation as incomplete/unprofessional
- May indicate other customizations missing
- Reduces credibility

### Mitigation
1. Audit all documentation for remaining placeholder text
2. Collect actual organization name from stakeholder
3. Replace all instances globally
4. Implement documentation review gate before publication

### Owner: Phase B (Documentation Completeness)

---

## R-002: Uneven Documentation Coverage

**Severity:** MEDIUM  
**Probability:** HIGH  
**Current State:** CONFIRMED (gestion/ domain sparse)

### Description
Documentation completeness varies by domain:
- requisitos/ ✅ Robust
- arquitectura_tecnica/ ✅ Good
- normativa/ ✅ Complete
- base_cognitiva/ ⚠️ Partial
- gestion/ 🔴 Sparse

Operational documentation (gestion/) significantly less developed than others.

### Impact
- Operators lack complete guidance
- Knowledge transfer difficult
- Process documentation incomplete

### Mitigation
1. Expand gestion/ domain with operational procedures
2. Document process workflows
3. Create operational playbooks
4. Define maintenance procedures

### Owner: Phase B (Documentation Completeness)

---

## R-003: Technical Debt from config-review-iact-docs

**Severity:** MEDIUM  
**Probability:** HIGH  
**Current State:** CONFIRMED (analysis complete, remediation pending)

### Description
config-review-iact-docs WP identified but did not implement:
- 8 risks in risk-register
- Configuration gaps and inconsistencies
- Extension compatibility issues

Analysis complete; implementation deferred to separate WP.

### Impact
- Configuration issues unresolved
- Technical debt accumulating
- Build pipeline potentially fragile

### Mitigation
1. Implement one of: Config Standardization (Phase A), Security Hardening (Phase C), or RBAC (Phase D)
2. Resolve identified configuration gaps
3. Normalize Sphinx settings
4. Validate extension compatibility

### Owner: Phase A or C or D (depending on choice)

---

## R-004: PlantUML Hook Instability (Technical Debt)

**Severity:** LOW  
**Probability:** MEDIUM  
**Current State:** MATERIALIZED (disabled in conf.py)

### Description
PlantUML sphinxcontrib hook throws FileNotFoundError on image path resolution. Temporarily disabled in conf.py line 37 during plantuml-java-integration-impl WP.

### Impact
- PlantUML diagrams not currently rendered
- Diagram generation blocked until hook fixed
- Build output missing diagram visualizations

### Mitigation
1. Fix image path handling in sphinxcontrib.plantuml hook
2. Re-enable hook after validation
3. Test diagram rendering with sample diagrams
4. Document any path configuration requirements

### Owner: Phase A (Configuration Standardization)

---

## R-005: RBAC Model Not Enforced

**Severity:** MEDIUM  
**Probability:** HIGH  
**Current State:** CONFIRMED (documented but not implemented)

### Description
Governance model (RBAC 5.1.1) is documented in normativa/ but not actually implemented in code. Documentation describes the structure, but access control enforcement is missing.

### Impact
- Security model not enforced
- Production deployment incomplete
- Compliance gap (documented model ≠ actual enforcement)

### Mitigation
1. Review RBAC documentation (normativa/)
2. Design access control implementation
3. Implement role-based access enforcement
4. Validate against documented model
5. Test with production scenarios

### Owner: Phase D (RBAC Implementation)

---

## R-006: Outdated Project Timeline Information

**Severity:** LOW  
**Probability:** MEDIUM  
**Current State:** CONFIRMED (readme mentions Oct 2025 as start date)

### Description
readme.rst lists "Fecha de Inicio: Octubre 2025" which appears to be future or inconsistent with current date (April 2026 per system clock).

### Impact
- Confusion about actual project timeline
- Incorrect historical context for stakeholders
- Documentation credibility reduced

### Mitigation
1. Verify actual project start date
2. Update readme.rst with accurate date
3. Review other timeline-related documentation
4. Establish documentation update frequency

### Owner: Phase B (Documentation Completeness)

---

## R-007: Integration Points Underdocumented

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Current State:** CONFIRMED (readme mentions integrations but details sparse)

### Description
readme.rst mentions PBX/IVR, CRM, and compliance integrations but provides minimal detail. Integration architecture, data flows, and API contracts not well documented.

### Impact
- Integration developers lack guidance
- Third-party integration risk
- Data consistency concerns

### Mitigation
1. Document integration architecture
2. Specify data flow models
3. Define API contracts for each integration
4. Create integration testing guide
5. Document error handling for integration failures

### Owner: Phase A or C (depending on priority)

---

## R-008: Configuration Knowledge Concentration

**Severity:** LOW  
**Probability:** MEDIUM  
**Current State:** POTENTIAL (if maintainer turnover occurs)

### Description
Configuration decisions, extension selections, and setup procedures may be concentrated in limited personnel knowledge. If key people leave, project continuity at risk.

### Impact
- Knowledge transfer difficult
- Configuration changes risky
- Onboarding new team members challenging

### Mitigation
1. Document all configuration decisions
2. Create runbooks for common procedures
3. Establish configuration version control
4. Cross-train team on deployment procedures
5. Create architecture decision records (ADRs)

### Owner: Phase A (Configuration Standardization)

---

## Risk Management Strategy

### Monitoring by Phase

**Phase A (Config Standardization):**
- R-003, R-004, R-008
- Track: config resolution progress, extension compatibility

**Phase B (Documentation Completeness):**
- R-001, R-002, R-006, R-007
- Track: domain coverage percentage, placeholder text count

**Phase C (Security Hardening):**
- R-003, R-007
- Track: compliance checklist completion, vulnerability remediation

**Phase D (RBAC Implementation):**
- R-005
- Track: enforcement coverage, access control test coverage

### Escalation Path
- **Materialize:** Move from CONFIRMED to ACTIVE intervention
- **Assign Owner:** Phase (A/B/C/D) responsible for mitigation
- **Review:** Weekly during implementation phase
- **Resolution:** Close risk when mitigation complete + verified

---

## Summary

| Risk ID | Severity | Status | Owner |
|---------|----------|--------|-------|
| R-001 | MEDIUM | Confirmed | Phase B |
| R-002 | MEDIUM | Confirmed | Phase B |
| R-003 | MEDIUM | Confirmed | Phase A/C/D |
| R-004 | LOW | Materialized | Phase A |
| R-005 | MEDIUM | Confirmed | Phase D |
| R-006 | LOW | Confirmed | Phase B |
| R-007 | MEDIUM | Confirmed | Phase A/C |
| R-008 | LOW | Potential | Phase A |

**Total Risks:** 8  
**Active:** 8 (all require attention)  
**Blocking:** None (project can proceed with chosen phase)

---

**Risk Register Created:** 2026-04-25 22:13:43  
**Status:** Ready for Phase 2 MEASURE or Phase 5 STRATEGY (depends on user choice of A/B/C/D)
