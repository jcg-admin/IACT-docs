```yml
created_at: 2026-05-07 23:25:00
project: IACT-docs
work_package: 2026-05-07-23-15-00-endpoint-sod-rules-rename
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Task Plan
```

# Task Plan — endpoint sod-rules rename

> 10 tareas atomicas, 1 archivo = 1 commit.

## Reglas

1. Renombrar `sod-rules` -> `separation-rules` en TODO match
   del archivo (pueden ser multiples ocurrencias por archivo).
2. Renombrar `Createsodruleview` -> `CreateSeparationRuleView`
   (T-006).
3. NO tocar `catalogo-funciones.rst` (tokens opacos).
4. NO tocar STD-013 (ejemplo educativo en §82 preservar).
5. Sin builds intermedios. Build serial final en TR-01.

## Bloque EXECUTE (10 tareas)

### Cluster admin (3)

- [ ] **T-001** — Rename en `source/requisitos/casos-uso/admin/uc-adm-01/actores-precondiciones.rst` (3 refs).
- [ ] **T-002** — Rename en `source/requisitos/casos-uso/admin/uc-adm-01/flujo-principal.rst` (1 ref).
- [ ] **T-003** — Rename en `source/requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst` (1 ref).

### Cluster access (7)

- [ ] **T-004** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/actores-precondiciones.rst` (1 ref).
- [ ] **T-005** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/criterios-aceptacion.rst` (1 ref).
- [ ] **T-006** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/datos-involucrados.rst` (5 refs).
- [ ] **T-007** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-secuencia-crear-regla.rst` (1 ref + alias UML).
- [ ] **T-008** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/flujo-principal.rst` (4 refs).
- [ ] **T-009** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/implementacion-tecnica.rst` (1 ref).
- [ ] **T-010** — Rename en `source/requisitos/casos-uso/access/uc-acc-05/testing.rst` (1 ref).

## Bloque TRACK (3 tareas)

- [ ] **TR-01** — Build clean serial deterministic (-j 1).
- [ ] **TR-02** — Verificar EXIT=0 + 0 warnings + 0 cross-refs rotos + grep validation (1 sola ref restante en STD-013 §82).
- [ ] **TR-03** — Cierre WP: changelog + lessons + wp-state.

## Convenciones de commit

`Rename sod-rules to separation-rules in {archivo}`

Body referencia T-NNN + backend A-003.
