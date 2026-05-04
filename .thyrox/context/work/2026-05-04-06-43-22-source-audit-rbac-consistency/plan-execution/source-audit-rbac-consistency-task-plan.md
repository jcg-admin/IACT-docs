```yml
created_at: 2026-05-04 06:47:23
project: IACT-docs
work_package: 2026-05-04-06-43-22-source-audit-rbac-consistency
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — Source Audit RBAC Consistency

Corrección de inconsistencias detectadas en `source/` respecto a
CIA-RBAC-002 + CNST-033 v2.0.0.

Un hallazgo accionable identificado (F-01). Ver
`discover/source-audit-rbac-consistency-analysis.md`.

---

## Bloque A — Corrección F-01

- [x] **T-001** Corregir `HasFunctionPermission` → `FunctionPermission`
  en `source/normativa/restricciones/cnst-010-permission-class-explicita-en-vistas-drf.rst`
  (líneas 74 y 87).
- [x] **T-002** Commit y push

---

---

## Bloque B — Corrección F-02/F-03 (adr-back-006 + adr-back-005)

- [x] **T-003** Corregir `adr-back-006` §6: `GranularPermission` →
  `FunctionPermission`; `user_has_function()` → `FunctionAuthorization`
  backend (CIA-RBAC-002 DEC-003/DEC-005).
- [x] **T-004** Ampliar nota en `adr-back-005`: añadir renames
  `GranularPermission` → `FunctionPermission` y
  `GranularPermissionMixin` → `FunctionPermissionMixin`
  (CIA-RBAC-002 DEC-005) al bloque `.. note::` existente.
- [ ] **T-005** Commit y push

---

## Orden de ejecución

```
T-001 → T-002 → T-003 → T-004 → T-005
```
