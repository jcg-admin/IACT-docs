```yml
created_at: 2026-04-25 23:55:00
project: IACT-docs
work_package: 2026-04-25-22-47-23-github-actions-setup
phase: Phase 7 — DESIGN/SPECIFY
author: Claude
status: Borrador
version: 1.0.0
spec_count: 5
```

# Especificación de Requisitos Técnicos — GitHub Actions Setup Phase 1

## Resumen Ejecutivo

Este documento especifica exactamente los 5 archivos que se crearán en `.github/` para implementar CI/CD automation Phase 1 (Essential) del IACT-docs project.

Los archivos establecen:
1. **Issue templates (3):** Structured bug reports, feature requests, questions
2. **PR template (1):** Contribution checklist
3. **Sphinx build workflow (1):** Automated CI/CD validation

**Objetivo:** Proporcionar especificaciones técnicas detalladas que respeten:
- Phase 6 PLAN: 5 files, clear scope
- Phase 4 CONSTRAINTS: All HC/SC respected (Ubuntu, Python 3.11, <60 min/month, no breaking changes)
- Exit criteria: Zero `[NEEDS CLARIFICATION]` markings

---

## Mapeo Phase 6 PLAN → Especificación

| Archivo (Phase 6) | SPEC ID | Descripción Técnica |
|---|---|---|
| `.github/ISSUE_TEMPLATE/config.yml` | SPEC-001 | Configures template menu (bug, feature, question) |
| `.github/ISSUE_TEMPLATE/bug-report.yml` | SPEC-002 | Structured bug report form (YAML) |
| `.github/ISSUE_TEMPLATE/feature-request.md` | SPEC-003 | Feature request template (Markdown) |
| `.github/PULL_REQUEST_TEMPLATE.md` | SPEC-004 | PR checklist + contribution guidelines |
| `.github/workflows/sphinx-build.yml` | SPEC-005 | Sphinx CI/CD workflow (GitHub Actions) |

---

## SPEC-001: Issue Template Config

**ID:** SPEC-001  
**Archivo:** `.github/ISSUE_TEMPLATE/config.yml`  
**Prioridad:** High (foundational for issue templates)  
**Estado:** Pendiente aprobación  
**Complejidad:** Baja  
**Esfuerzo Estimado:** 15 minutos

### Descripción

Configure GitHub's issue template menu to offer three structured options: bug reports, feature requests, and questions. This file acts as the registry that tells GitHub which templates to show when users create an issue.

### Criterios de Aceptación

```
Given a user navigates to Issues > New Issue on GitHub
When they click the template selector
Then they see three options:
  1. "Bug Report" (bug-report.yml)
  2. "Feature Request" (feature-request.md)
  3. "Question" (default Markdown placeholder)

Given config.yml is properly formatted YAML
When GitHub parses the file
Then no parsing errors occur and templates are accessible
```

### Consideraciones Técnicas

- Format: YAML (GitHub's native config format for issue templates)
- Location: `.github/ISSUE_TEMPLATE/` directory
- Naming: `config.yml` (exact filename required by GitHub)
- References: Must link to bug-report.yml and feature-request.md files

### Implementación

**Contenido esperado:**
```yaml
blank_issues_enabled: false
contact_links:
  - name: Question or Discussion
    url: https://github.com/jcg-admin/IACT-docs/discussions
    about: Ask questions or start discussions
```

**Archivos a Crear:**
- `.github/ISSUE_TEMPLATE/config.yml`

**Respeta Constraints:**
- ✅ HC-005: No breaking changes (new file only, no modifications)
- ✅ SC-004: Backward compatible (optional feature, GitHub ignores if not present)

### Validación

- [ ] File created at correct path: `.github/ISSUE_TEMPLATE/config.yml`
- [ ] YAML syntax valid (no errors when pushed)
- [ ] GitHub renders template selector correctly
- [ ] Commits follow conventional format: `feat(github-actions): add issue template config`

**Notas:** If `blank_issues_enabled: false`, users cannot create blank issues (they must choose a template). This is acceptable for IACT-docs to enforce structure.

---

## SPEC-002: Bug Report Template

**ID:** SPEC-002  
**Archivo:** `.github/ISSUE_TEMPLATE/bug-report.yml`  
**Prioridad:** High (primary issue type)  
**Estado:** Pendiente aprobación  
**Complejidad:** Media  
**Esfuerzo Estimado:** 20 minutos

### Descripción

A structured YAML form template for bug reports. GitHub renders YAML templates as interactive forms with type-specific fields (text, textarea, dropdown, checkboxes). This template guides contributors to provide complete bug information.

### Criterios de Aceptación

```
Given a user selects "Bug Report" from the issue template menu
When the form loads in the GitHub UI
Then they see fields for:
  - Title (required)
  - Description of the bug (textarea)
  - Reproduction steps (numbered list)
  - Expected behavior (textarea)
  - Actual behavior (textarea)
  - Environment (Sphinx version, Python version, OS) — pre-populated hints
  - Screenshots/attachments (optional)

Given user fills in the form and submits
When the issue is created
Then the issue body is properly formatted and readable
```

### Consideraciones Técnicas

- Format: YAML with `name`, `description`, `body` sections
- Body: Array of field objects with type, attributes, validations
- Pre-populated: Sphinx 9.0.4 version hint in environment field
- Required fields: title, description, reproduction steps, expected/actual behavior

### Implementación

**Estructura esperada:**
```yaml
name: Bug Report
description: Report a bug in IACT-docs or Sphinx build

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug!
        Please provide as much detail as possible.

  - type: textarea
    id: description
    attributes:
      label: Description
      placeholder: Describe the bug...
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: How to reproduce
      placeholder: |
        1. ...
        2. ...

  - type: input
    id: environment
    attributes:
      label: Environment
      value: "Sphinx 9.0.4, Python 3.11, PlantUML 1.2025.0"
```

**Archivos a Crear:**
- `.github/ISSUE_TEMPLATE/bug-report.yml`

**Respeta Constraints:**
- ✅ HC-005: No breaking changes (new template only)
- ✅ SC-004: Backward compatible

### Validación

- [ ] File created at correct path: `.github/ISSUE_TEMPLATE/bug-report.yml`
- [ ] YAML syntax valid
- [ ] Form renders correctly in GitHub UI
- [ ] All required fields are marked `required: true`
- [ ] Pre-populated environment field includes Sphinx version

---

## SPEC-003: Feature Request Template

**ID:** SPEC-003  
**Archivo:** `.github/ISSUE_TEMPLATE/feature-request.md`  
**Prioridad:** High (secondary issue type)  
**Estado:** Pendiente aprobación  
**Complejidad:** Baja  
**Esfuerzo Estimado:** 15 minutos

### Descripción

A Markdown template (simpler than YAML forms) for feature requests. Provides guided sections for motivation, proposed solution, and acceptance criteria.

### Criterios de Aceptación

```
Given a user selects "Feature Request" from the menu
When the issue form opens
Then they see a Markdown template with sections:
  - **Motivation:** Why is this feature needed?
  - **Proposed Solution:** How should it work?
  - **Alternatives Considered:** Other options evaluated
  - **Acceptance Criteria:** How to measure success

Given user fills in sections and submits
When the issue is created
Then the structure is readable and traceable
```

### Consideraciones Técnicas

- Format: Markdown (GitHub's simpler template format)
- No type validation (unlike YAML forms) but easier to write
- Clear section headers for guidance
- Optional: Links to GUIDELINES.rst

### Implementación

**Contenido esperado:**
```markdown
# Feature Request

## Motivation
Why do we need this feature?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches could work?

## Acceptance Criteria
How will we know it's done?
- [ ] Criterion 1
- [ ] Criterion 2

## Related Issues
Closes #[issue_number]
```

**Archivos a Crear:**
- `.github/ISSUE_TEMPLATE/feature-request.md`

**Respeta Constraints:**
- ✅ HC-005: No breaking changes
- ✅ SC-004: Backward compatible

### Validación

- [ ] File created at correct path: `.github/ISSUE_TEMPLATE/feature-request.md`
- [ ] Markdown syntax valid
- [ ] All sections present and clear
- [ ] Links to GUIDELINES.rst (if included) are valid

---

## SPEC-004: Pull Request Template

**ID:** SPEC-004  
**Archivo:** `.github/PULL_REQUEST_TEMPLATE.md`  
**Prioridad:** High (contribution guide)  
**Estado:** Pendiente aprobación  
**Complejidad:** Baja  
**Esfuerzo Estimado:** 15 minutos

### Descripción

A Markdown template that appears when users open a pull request. Provides a checklist of pre-merge requirements: local testing, RST conventions, commit messages, documentation updates.

### Criterios de Aceptación

```
Given a user creates a PR to main branch
When the PR description form loads
Then they see a checklist including:
  - [ ] I have tested this change locally
  - [ ] I have followed RST formatting conventions
  - [ ] I have used conventional commit messages
  - [ ] Documentation is updated
  - [ ] No breaking changes introduced

Given user submits the PR
When reviewers see the PR
Then they can verify checklist items and block merge if unchecked
```

### Consideraciones Técnicas

- Format: Markdown with checkbox syntax (`- [ ] item`)
- Not a GitHub-enforced requirement (informational, relies on reviewer discipline)
- Can reference GUIDELINES.rst or contribution standards
- Helps maintain consistency without strict enforcement

### Implementación

**Contenido esperado:**
```markdown
## PR Checklist

- [ ] Changes tested locally (`make html` succeeds)
- [ ] RST title formatting follows conventions (overline/underline match)
- [ ] Commit messages follow conventional format (type(scope): description)
- [ ] Documentation updated if needed
- [ ] No breaking changes to conf.py or dependencies

## Description
[Brief description of changes]

## Related Issues
Closes #[issue_number]

## Screenshots
[If applicable]
```

**Archivos a Crear:**
- `.github/PULL_REQUEST_TEMPLATE.md`

**Respeta Constraints:**
- ✅ HC-005: No breaking changes
- ✅ SC-004: Backward compatible

### Validación

- [ ] File created at correct path: `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Markdown syntax valid
- [ ] Template appears when user creates PR
- [ ] All checklist items are relevant and actionable

---

## SPEC-005: Sphinx Build Workflow

**ID:** SPEC-005  
**Archivo:** `.github/workflows/sphinx-build.yml`  
**Prioridad:** Critical (core CI/CD automation)  
**Estado:** Pendiente aprobación  
**Complejidad:** Alta  
**Esfuerzo Estimado:** 1.5 horas

### Descripción

GitHub Actions workflow (YAML) that automatically validates Sphinx documentation builds on every PR and push to main. This is the core CI/CD feature that prevents broken builds from merging.

### Criterios de Aceptación

```
Given a PR is created to main branch
When the workflow triggers automatically
Then the following steps execute:
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies from pyproject.toml
  4. Run: make clean && make html
  5. Report success or failure

Given Sphinx build succeeds
When workflow completes
Then PR shows green checkmark (✓) and can be merged

Given Sphinx build fails
When workflow completes  
Then PR shows red X (✗), error log visible, merge blocked
```

### Consideraciones Técnicas

**Respeta ALL HC/SC from Phase 4 CONSTRAINTS:**
- ✅ HC-001: Triggers only on PR+main (not every commit) → cost ~50 min/month
- ✅ HC-002: `runs-on: ubuntu-latest` (Linux runner)
- ✅ HC-003: `python-version: '3.11'` (from pyproject.toml requires-python)
- ✅ HC-004: PlantUML must be available (apt-get install or preinstalled)
- ✅ HC-005: Exit code validation (make html must succeed)
- ✅ SC-001: Cost minimization (trigger strategy limits usage)
- ✅ SC-002: Build speed (15-20 min timeout accommodates compilation)
- ✅ SC-003: PlantUML support (sufficient timeout for diagram compilation)
- ✅ SC-004: No breaking changes (new file, no modifications to source)

### Implementación

**Estructura esperada:**
```yaml
name: Sphinx Build Validation

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e .
      
      - name: Build Sphinx documentation
        run: |
          cd source
          make clean
          make html
      
      - name: Upload build artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: sphinx-build
          path: source/_build/html/
```

**Archivos a Crear:**
- `.github/workflows/sphinx-build.yml`

**Archivos implícitos (NO crear, ya existen):**
- `source/conf.py` (PlantUML config already present)
- `pyproject.toml` (dependencies already defined)
- `Makefile` or `source/Makefile` (build system already set up)

### Validación

- [ ] File created at correct path: `.github/workflows/sphinx-build.yml`
- [ ] YAML syntax valid (no parsing errors)
- [ ] Workflow triggers on PR to main (test with feature branch)
- [ ] Python 3.11 environment loads successfully
- [ ] Dependencies install without conflicts
- [ ] `make html` command executes
- [ ] Workflow reports pass/fail clearly
- [ ] Build completes within 15-minute timeout
- [ ] PlantUML diagrams compile without errors
- [ ] Timeout estimate validated: actual time < 15 min

**Notas:** 
- First run may be slower (pip install cache miss), subsequent runs faster
- PlantUML compilation adds 1-3 minutes (acceptable)
- If workflow times out, reduce diagram complexity or optimize in Phase 2

---

## Dependencias Entre Specs

```
SPEC-001 (config.yml)
    ↓
SPEC-002 (bug-report.yml) — referenced by SPEC-001
SPEC-003 (feature-request.md) — referenced by SPEC-001
    ↓
SPEC-004 (PULL_REQUEST_TEMPLATE.md) — independent, complements issue templates
    ↓
SPEC-005 (sphinx-build.yml) — independent, validates that PRs can build
```

**Nota:** SPEC-001 must be created first (it configures templates). SPEC-002/003/004 can be created in parallel. SPEC-005 can be created anytime but must work with existing Sphinx configuration.

---

## Plan de Implementación (Phase 8 PLAN EXECUTION)

### Tarea 1: Create Issue Template Config
- SPEC-001 (config.yml)
- Dependency: None
- Estimated: 15 min

### Tarea 2: Create Bug Report Template
- SPEC-002 (bug-report.yml)
- Dependency: SPEC-001 (config references this)
- Estimated: 20 min

### Tarea 3: Create Feature Request Template
- SPEC-003 (feature-request.md)
- Dependency: SPEC-001 (config references this)
- Estimated: 15 min

### Tarea 4: Create PR Template
- SPEC-004 (PULL_REQUEST_TEMPLATE.md)
- Dependency: None (independent)
- Estimated: 15 min

### Tarea 5: Create Sphinx Build Workflow
- SPEC-005 (sphinx-build.yml)
- Dependency: None (standalone workflow)
- Estimated: 1.5 hours (includes local testing)

---

## Riesgos Técnicos y Mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación | Phase Owner |
|--------|---------|-------------|-----------|-------------|
| **YAML syntax error in workflow** | Workflow won't run | MEDIA | Use GitHub's visual editor to validate; test locally with `act` | Phase 10 |
| **PlantUML timeout on runner** | Build times out; workflow fails | BAJA | Set timeout to 15-20 min (generous); PlantUML usually fast on modern runners | Phase 10 |
| **Python version mismatch** | Dependencies won't install | BAJA | Explicitly specify `python-version: 3.11` matching pyproject.toml | Phase 7 ✅ |
| **Missing PlantUML binary** | Diagrams don't compile | BAJA | Ubuntu runners include Java by default; may need `apt-get install plantuml` | Phase 8 |
| **Cost exceeds free tier** | Project incurs charges | BAJA | Trigger only on PR+main, not every commit; estimate 50 min/month max | Phase 4 ✅ |

---

## Aprobaciones

| Rol | Nombre | Estado |
|-----|--------|--------|
| Tech Spec | Claude | ⏳ Pendiente aprobación |
| User/Project Owner | [Usuario] | ⏳ Pendiente aprobación |

---

**Versión:** 1.0.0  
**Creado:** 2026-04-25 23:55:00  
**Status:** Borrador — Listo para Phase 8 PLAN EXECUTION cuando se apruebe  
**Next Step:** User confirms all 5 specs are clear and implementable, then proceed to Phase 8 PLAN EXECUTION (task breakdown T-001..T-005)
