```yml
created_at: 2026-04-23 18:51:00
project: IACT-docs
work_package: 2026-04-23-18-51-33-plantuml-java-integration-impl
phase: Phase 1 — DISCOVER
author: Claude Code Agent
status: Aprobado
```

# Phase 1 DISCOVER: PlantUML Java Integration Implementation

**WP:** 2026-04-23-18-51-33-plantuml-java-integration-impl  
**Project:** IACT-docs  
**Objective:** Integrate PlantUML with Java execution, styles, and automated image generation  
**Date:** 2026-04-23  

---

## 1. Problem Statement

### Current State
- 100+ PlantUML diagrams in IACT-docs UC documentation
- Diagrams currently inline in RST with minimal styling
- No centralized style configuration
- Manual handling of diagram rendering
- No guarantee images update when `make html` runs

### Target State
- PlantUML diagrams automatically rendered on `make html`
- Centralized style configuration (source/_static/plantuml-styles.puml)
- Java-based PlantUML processor integrated with Sphinx
- Consistent visual style across all 100+ diagrams
- UML compliance verified

### Success Criteria
**WP is CLOSED when:**
1. ✅ `make html` generates diagrams → PNG/SVG images automatically
2. ✅ Styles from centralized config applied to all diagrams
3. ✅ 0 new warnings in Sphinx build
4. ✅ Java PlantUML processor correctly installed and configured
5. ✅ All 100+ UC diagrams render correctly with new styles
6. ✅ Documentation updated with styling guidelines
7. ✅ Build process is reproducible (CI/CD ready)

---

## 2. Scope Definition

### In Scope
- Install and configure Java PlantUML v1.2025.0
- Create centralized style configuration file
- Configure sphinxcontrib.plantuml to use styles
- Test with sample diagrams (5 critical UC modules)
- Expand to all UC diagrams (100+)
- Validate `make html` workflow end-to-end
- Document for maintenance

### Out of Scope
- Creating new diagrams (only styling existing)
- Custom PlantUML extensions/plugins
- Alternative diagram tools (only PlantUML)
- CI/CD pipeline setup (only local make html)
- Performance optimization beyond baseline

---

## 3. Stakeholders & Success Metrics

### Stakeholders
- **IACT Documentation Team:** Need consistent, professional diagrams
- **Maintenance Team:** Need reproducible build process
- **New Contributors:** Need clear guidelines for new diagrams

### Success Metrics
| Metric | Target | Verification |
|--------|--------|---|
| Build warnings | 0 | `make clean && make html` output |
| Diagrams rendered | 100% | Visual inspection of generated HTML |
| Style application | 100% | All diagrams use corporate colors |
| Build time | <5 min | Time tracking in CI logs |
| Reproducibility | 100% | Different machines, same output |

---

## 4. Technical Context from Previous WP

### PlantUML Analysis Completed ✅
- 626-line integration analysis
- UML compliance verified
- 4-phase implementation strategy
- Corporate palette defined

### Color Palette Defined
```
PRIMARY: #1976D2     (Blue - IACT brand)
SECONDARY: #388E3C   (Green - Access Control)
ACCENT: #F57C00      (Orange - Alerts)
BG: #FFFFFF          (White)
TEXT: #000000        (Black)
```

### Risks Identified
1. Java not installed → Mitigation: Verify `java -version`
2. PlantUML version mismatch → Mitigation: Pin to 1.2025.0
3. Sphinx configuration errors → Mitigation: Incremental testing
4. Build warnings on inclusion → Mitigation: Test 5 samples first

---

## 5. Implementation Strategy (4 Phases)

### Phase 1: Environment Setup
**Duration:** 2-3 hours
- Verify Java installation
- Download PlantUML v1.2025.0
- Install sphinxcontrib.plantuml
- Configure in Sphinx conf.py

### Phase 2: Style Configuration
**Duration:** 2-3 hours
- Create `source/_static/plantuml-styles.puml`
- Define corporate palette (variables)
- Create skinparam groups
- Test with 1 sample diagram

### Phase 3: Validation (5 Critical Modules)
**Duration:** 4-6 hours
- Apply styles to UC_AUTH_01
- Apply styles to UC_ACCESS_010
- Apply styles to UC_USERS_001
- Apply styles to UC_REPORTS_001
- Apply styles to UC_ALERTS_001
- Run `make clean && make html` after each
- Verify 0 warnings, images rendered correctly

### Phase 4: Expansion & Documentation
**Duration:** 6-10 hours
- Apply styles to all remaining UC diagrams (95+)
- Validate by module (8 modules)
- Update README.md with guidelines
- Create META_XX_Estilos_PlantUML.rst
- Final validation: full build

### Phase 5: Closure
**Duration:** 1-2 hours
- Verify all 100+ diagrams render
- Document build process
- Create maintenance guidelines
- Close WP when `make html` fully working

---

## 6. Dependencies & Assumptions

### Dependencies
- Java Runtime Environment (8+)
- Python 3.8+ (for Sphinx)
- sphinxcontrib.plantuml package
- PlantUML v1.2025.0
- Graphviz (optional, for better rendering)

### Assumptions
- Java is available in PATH
- Sphinx is running correctly (verified by 0 warnings in previous WP)
- All UC diagrams are valid PlantUML syntax
- sphinxcontrib.plantuml supports style configuration

---

## 7. Risks & Mitigation

| Risk | Probability | Severity | Mitigation |
|------|---|---|---|
| Java not installed | Medium | High | Check `java -version` first |
| PlantUML version incompatible | Low | High | Pin to v1.2025.0 |
| Warnings from style syntax | Low | Medium | Test 5 diagrams before expanding |
| Build time increases | Medium | Low | Monitor build time, optimize if needed |
| Images not generating | Low | High | Validate PlantUML proc. after each phase |

---

## 8. Definition of Done

### WP Closure Criteria
- [ ] Phase 1: Environment Setup complete
- [ ] Phase 2: Style configuration working
- [ ] Phase 3: 5 critical diagrams validated (0 warnings)
- [ ] Phase 4: All 100+ diagrams with styles
- [ ] Phase 5: Full build successful, documentation updated
- [ ] `make clean && make html` produces images automatically
- [ ] All deliverables documented and committed

### Quality Gates
- [ ] 0 new Sphinx warnings
- [ ] 100% diagram coverage (all UC diagrams styled)
- [ ] Corporate palette applied consistently
- [ ] Reproducible on different machines
- [ ] Documentation up-to-date

---

## 9. Constraints

### Technical Constraints
- Must use PlantUML (not alternative tools)
- Java-based processor (requirement)
- Sphinx integration via sphinxcontrib.plantuml
- Must maintain 0-warning build baseline

### Time Constraints
- Target completion: 4-5 weeks
- Must not impact current documentation

### Resource Constraints
- Single developer (Claude)
- Incremental validation required (can't batch-process all 100+ at once)

---

## 10. Next Steps

### Immediate (Next Session)
1. **Phase 1 DISCOVER:** ✅ Completed (this document)
2. **Phase 3 DIAGNOSE:** Detailed technical analysis
3. **Phase 5 STRATEGY:** Select implementation approach
4. **Phase 6 PLAN:** Define scope + roadmap
5. **Phase 8 PLAN EXECUTION:** Create task breakdown

### Upon Approval
1. Begin Phase 1 Setup (Java, PlantUML, dependencies)
2. Create styles.puml in source/_static/
3. Test with sample diagrams
4. Proceed to expansion phase

---

## 11. Estimated Timeline

```
Week 1: Environment Setup + Style Configuration
├── Day 1-2: Java, PlantUML install, Sphinx config
├── Day 3-4: Create plantuml-styles.puml
└── Day 5: Test with 1 sample diagram

Week 2: Validation (5 Critical Modules)
├── Days 1-2: AUTH, ACCESS modules
├── Days 3-4: USERS, REPORTS modules
└── Day 5: ALERTS module + full validation

Weeks 3-4: Expansion (95+ remaining diagrams)
├── By module (8 modules total)
├── Incremental validation
└── Monitor build time/warnings

Week 5: Documentation & Closure
├── Update README.md, META_XX
├── Create guidelines for new diagrams
└── Final validation, WP closure
```

---

## 12. Success Definition

**WP is CLOSED and SUCCESS when:**

```
$ make clean && make html
# Build succeeds
# 0 warnings
# 100+ diagrams generated as PNG/SVG
# All diagrams display corporate colors
# HTML output shows styled diagrams
```

---

**Analysis Created:** 2026-04-23 18:51:00  
**Status:** Phase 1 DISCOVER COMPLETE  
**Next Phase:** Phase 3 DIAGNOSE (detailed technical analysis)  
**Ready for approval:** YES
