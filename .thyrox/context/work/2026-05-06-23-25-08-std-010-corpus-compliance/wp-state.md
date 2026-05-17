```yml
project: IACT-docs
work_package: 2026-05-06-23-25-08-std-010-corpus-compliance
created_at: 2026-05-06 23:25:08
current_phase: Phase 1 — DISCOVER
author: NestorMonroy
parent_wp: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
trigger: discover/std-010-vocabulario-abstracto-audit.md (V-1..V-3 detected) + executor request to fix all violations corpus-wide
branch: feature/cnst-033-uml-conformance
```

# WP State — STD-010 Corpus Compliance

## Objetivo

Auditar y corregir todas las violaciones de STD-010
(Vocabulario Abstracto) en el corpus IACT-docs. Aplica
exclusivamente a archivos bajo el ámbito declarado en
STD-010 §2:

- `source/requisitos/casos-uso/**/*.rst` (excepto
  `implementacion-tecnica.rst`)
- `source/requisitos/casos-uso/**/diagramas-uml.rst`
  (participantes)

NO aplica a (libre):

- `source/arquitectura-tecnica/**`
- `source/backend/**`
- `source/normativa/**`
- `implementacion-tecnica.rst` por UC
- `.thyrox/context/work/**` (artefactos internos)

## Scope

**In-scope:**

1. Auditoría exhaustiva: catalogar todas las menciones de
   términos prohibidos en archivos bajo ámbito.
2. Corrección de violaciones detectadas: sustituir por
   términos canónicos según STD-010 §3.
3. Reformulación de la decisión "Celery beat" en el WP
   padre `2026-05-06-21-42-06-menu-rbac-user-scope-docs`
   antes de Phase 7 (en el artefacto
   `final-decisions-p1-p4-and-pending-items.md`).
4. Verificación final con grep de STD-010 §6.

**Out-of-scope:**

1. Modificar STD-010 mismo.
2. Auditar/corregir clases de modelo de dominio (idioma)
   — si se detecta mezcla, abrir WP separado.
3. Corregir `source/arquitectura-tecnica/**` (libre por
   STD-010 §2).
4. Phase 5 STRATEGY del WP padre menu-rbac-user-scope —
   **pendiente, se retoma al cerrar este WP**.

## Pending after this WP

- **Retomar WP padre `2026-05-06-21-42-06-menu-rbac-user-scope-docs`**
  en Phase 5 STRATEGY produciendo
  `strategy/menu-rbac-user-scope-solution-strategy.md`
  con:
  - Key Ideas (lifecycle managed wrapper UX,
    defense-in-depth, eventual consistency).
  - Fundamental Decisions (P1-P4 confirmadas).
  - Technology Stack.
  - Architecture Patterns.
  - Adherence to Constraints (BR-012, CNST-029, CNST-032,
    ADR-BACK-001/007).
  - Traceability + evidence classification.

## Stages

- [x] Phase 1 DISCOVER (audit + correction plan)
- [ ] Phase 10 EXECUTE (apply corrections)
- [ ] Phase 11 TRACK (verify with grep, changelog)

Tamaño: pequeño (audit + sustituciones mecánicas).
Saltar Phase 2-9 (no requiere strategy/design adicional —
STD-010 ya define el mapeo canónico).
