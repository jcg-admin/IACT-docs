```yml
created_at: 2026-04-23 18:51:00
updated_at: 2026-04-23 18:51:00
project: IACT-docs
work_package: 2026-04-23-18-51-33-plantuml-java-integration-impl
phase: Phase 1 — DISCOVER
status: Activo
```

# Risk Register: PlantUML Java Integration Implementation

---

## R-001: Java Not Installed or Incorrect Version

**Severity:** HIGH  
**Probability:** MEDIUM  
**Impact:** Cannot generate diagrams, build fails  

### Description
System may not have Java installed, or installed version incompatible with PlantUML v1.2025.0.

### Mitigation
1. Check `java -version` on target system
2. Install JDK 8+ if missing
3. Document minimum Java version requirement
4. Create validation script in build process

### Owner: Phase 1 Setup

---

## R-002: PlantUML Version Mismatch

**Severity:** HIGH  
**Probability:** LOW  
**Impact:** Syntax errors, features not available  

### Description
Analysis was done for v1.2025.0 but different version installed, causing compatibility issues.

### Mitigation
1. Pin PlantUML version in configuration
2. Create VERSION file documenting requirement
3. Test with v1.2025.0 explicitly in Phase 2
4. Document upgrade path for future versions

### Owner: Phase 1 Setup

---

## R-003: sphinxcontrib.plantuml Configuration Errors

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Impact:** Diagrams don't render, Sphinx warnings  

### Description
Sphinx configuration syntax error or incompatible plantuml_prepend directive.

### Mitigation
1. Test with 1 sample diagram first (Phase 2)
2. Validate conf.py syntax before expanding
3. Monitor Sphinx warnings closely
4. Incremental validation (5 diagrams before full expansion)

### Owner: Phase 2 Style Configuration

---

## R-004: Build Time Degradation

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Impact:** Slow builds, poor developer experience  

### Description
Running PlantUML on 100+ diagrams increases build time significantly.

### Mitigation
1. Baseline build time before and after
2. Parallel PlantUML processing if available
3. Cache generated images (avoid regeneration if unchanged)
4. Consider conditional rendering (only changed diagrams)

### Owner: Phase 4 Expansion + Phase 5 Optimization

---

## R-005: PlantUML Syntax Errors in Existing Diagrams

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Impact:** Build fails on invalid diagrams  

### Description
Some existing inline PlantUML diagrams may have syntax errors not caught before.

### Mitigation
1. Validate all UC diagrams with PlantUML linter
2. Fix syntax errors before applying styles
3. Create validation script for future diagrams
4. Document common PlantUML mistakes

### Owner: Phase 3 Validation or Phase 2 Pre-validation

---

## R-006: Style Application Breaks UML Compliance

**Severity:** MEDIUM  
**Probability:** LOW  
**Impact:** Diagrams visually incorrect, UML non-compliant  

### Description
Applied styles might accidentally change semantic meaning or break UML rules.

### Mitigation
1. Review skinparam against UML 2.x spec
2. Use `strictuml` mode to enforce compliance
3. Test with validation tools
4. Small incremental changes (avoid big styling refactors)

### Owner: Phase 2 Style Configuration + Phase 3 Validation

---

## R-007: Graphviz Dependency Missing

**Severity:** MEDIUM  
**Probability:** MEDIUM  
**Impact:** SVG generation fails, PNG only alternative  

### Description
Graphviz may not be installed, required for SVG output with better rendering.

### Mitigation
1. Check `dot -V` on system
2. Document as optional dependency
3. Fallback to PNG if Graphviz not available
4. Create installation guide for Graphviz

### Owner: Phase 1 Setup or Phase 2 Configuration

---

## R-008: Incomplete Coverage After Expansion

**Severity:** LOW  
**Probability:** MEDIUM  
**Impact:** Some diagrams still without styles  

### Description
After Phase 4, some UC diagrams may be missed (100+ is a lot to track).

### Mitigation
1. Create automated check: find diagrams without style inclusion
2. Script to verify all UC_*.rst include styles
3. Track coverage percentage
4. Manual audit before WP closure

### Owner: Phase 4 Expansion

---

## R-009: Rollback Required if Critical Issue

**Severity:** LOW  
**Probability:** LOW  
**Impact:** Time loss, revert to previous state  

### Description
If major issue discovered late (e.g., Phase 4), rollback might be needed.

### Mitigation
1. Each phase is self-contained, can rollback independently
2. Git history preserves all commits
3. Incremental approach allows rollback by module
4. Testing before expansion

### Owner: All phases (rollback planning)

---

## R-010: Documentation Becomes Outdated

**Severity:** LOW  
**Probability:** HIGH  
**Impact:** Maintenance burden, confusion for contributors  

### Description
PlantUML styling guidelines become outdated as features change.

### Mitigation
1. Create living documentation in META_XX
2. Document in this WP track/ folder
3. Create examples of correct styling
4. Version control for documentation

### Owner: Phase 5 Documentation + ongoing maintenance

---

## Risk Management Strategy

### Monitoring
- Phase 1: Check Java, PlantUML versions
- Phase 2: Monitor Sphinx warnings
- Phase 3: Track render times per diagram
- Phase 4: Coverage percentage monitoring
- Phase 5: Final validation

### Escalation
- HIGH severity issues → investigate immediately
- MEDIUM probability + HIGH severity → test before proceeding
- LOW probability + LOW severity → monitor but proceed

### Review Schedule
- Weekly during implementation
- After each phase completion
- Final review before WP closure

---

**Risk Register Created:** 2026-04-23 18:51:00  
**Total Risks Identified:** 10  
**HIGH Severity:** 2 (R-001, R-002)  
**MEDIUM Severity:** 6 (R-003, R-004, R-005, R-006, R-007, R-008)  
**LOW Severity:** 2 (R-009, R-010)
