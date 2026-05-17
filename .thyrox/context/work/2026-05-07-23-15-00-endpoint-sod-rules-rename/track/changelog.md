```yml
created_at: 2026-05-07 23:25:00
project: IACT-docs
work_package: 2026-05-07-23-15-00-endpoint-sod-rules-rename
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — endpoint sod-rules rename

## [1.0.0] — 2026-05-07

### Changed (10 archivos)

**Cluster admin (3):**

- ``uc-adm-01/actores-precondiciones.rst`` — 3 endpoint refs
  (``POST``, ``PATCH``, ``disable``).
- ``uc-adm-01/flujo-principal.rst`` — 1 endpoint ref.
- ``uc-adm-01/diagramas-uml/diagrama-de-actividad.rst`` — 1
  endpoint ref en plantuml block.

**Cluster access (7):**

- ``uc-acc-05/actores-precondiciones.rst`` — 1 ref.
- ``uc-acc-05/criterios-aceptacion.rst`` — 1 ref.
- ``uc-acc-05/datos-involucrados.rst`` — 5 refs en tabla API.
- ``uc-acc-05/diagramas-uml/diagrama-de-secuencia-crear-regla.rst``
  — rename comprehensive: 1 endpoint + 6 identificadores
  (CreateSoDRuleView, SoDRuleRepo, SoDRuleCache, SoDRuleDuplicate,
  create_sod_rule, SOD_RULE_CREATED).
- ``uc-acc-05/flujo-principal.rst`` — 4 refs (GET, POST,
  PATCH, DELETE).
- ``uc-acc-05/implementacion-tecnica.rst`` — 1 ref.
- ``uc-acc-05/testing.rst`` — 1 ref.

### Verification

- ``grep -rn "sod-rules" source/``: solo **1 resultado**
  (preservado intencionalmente — STD-013 §82 ejemplo
  negativo).
- ``grep -rn "separation-rules" source/``: 24 refs canonicas.
- Build clean serial deterministic (-j 1) — ver TR-01.

### Excluded (preservado)

- ``catalogo-funciones.rst:192,216`` — tokens opacos
  ``access:view_sod``, ``access:update_sod``. Son contrato
  RBAC del backend.
- ``std-013-rest-api-conventions.rst:82`` — ``❌ /access/sod-rules``
  ejemplo educativo de bad practice.
- ``mtm-03-metamodelo-rbac.rst`` — ``role_id`` en sintaxis
  RBAC clasica (out-of-scope, posible deuda futura).

## Commits del WP

13 commits totales:

1. WP setup (Phase 1 + Phase 8) — ``d8bfa8ae``.
2. T-001 ``c3a0fb46`` — uc-adm-01 actores-precondiciones.
3. T-002 ``1d7b2284`` — uc-adm-01 flujo-principal.
4. T-003 ``e6ad2fb9`` — uc-adm-01 diagrama-de-actividad.
5. T-004 ``7cf6b9a6`` — uc-acc-05 actores-precondiciones.
6. T-005 ``bb6c00f7`` — uc-acc-05 criterios-aceptacion.
7. T-006 ``2deebf28`` — uc-acc-05 datos-involucrados.
8. T-007 ``5e54b405`` — uc-acc-05 secuencia-crear-regla.
9. T-008 ``1a2a255d`` — uc-acc-05 flujo-principal.
10. T-009 ``05738f8b`` — uc-acc-05 implementacion-tecnica.
11. T-010 ``91ed9620`` — uc-acc-05 testing.
12. (este commit) — TRACK: changelog + cierre.

## Refs

- WP previo: ``2026-05-07-14-49-04-uml-diagrams-deep-audit``
  (cerrado).
- Backend A-001..A-005 — rename SodRule -> SeparationRule.
- STD-013 — norma canonica de separation-rules.
