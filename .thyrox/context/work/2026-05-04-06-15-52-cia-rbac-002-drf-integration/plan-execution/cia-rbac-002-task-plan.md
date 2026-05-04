```yml
created_at: 2026-05-04 06:15:52
project: IACT-docs
work_package: 2026-05-04-06-15-52-cia-rbac-002-drf-integration
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Pendiente
```

# Task Plan — CIA-RBAC-002 + ADR-GOB-010 DRF Integration

Crear documentos CIA-RBAC-002 y ADR-GOB-010, corregir notación
incorrecta de `@require_function` en 3 archivos, actualizar índices.

---

## Bloque A — Estructura y documentos nuevos

- [ ] **T-001** Crear `source/gestion/evidencia/rbac-arquitectura/index.rst`
- [ ] **T-002** Crear `source/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf.rst`
- [ ] **T-003** Crear `source/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend.rst`
- [ ] **T-004** Actualizar `source/gestion/evidencia/index.rst` — agregar `rbac-arquitectura/index`
- [ ] **T-005** Actualizar `source/normativa/gobernanza/index.rst` — agregar `adr-gob-010`

---

## Bloque B — Corrección de notación incorrecta

- [ ] **T-006** Corregir `@require_function('RPT-001')` en `analisis-errores-modelo-rbac-v5-2-0.rst`
- [ ] **T-007** Corregir `@require_function('FUNC-NNN')` en `matriz-dependencias-uc-iact.rst`
- [ ] **T-008** Corregir `@require_function('F_CODE')` en `uc-perm-07/informacion-general.rst`

---

## Bloque C — Commit y push

- [ ] **T-009** Commit: "Add CIA-RBAC-002 and ADR-GOB-010 DRF integration docs"
- [ ] **T-010** Push branch

---

## Orden de ejecución

```
A (T-001..T-005) → B (T-006..T-008) → C (T-009..T-010)
```
