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

Ver análisis completo: `analyze/deep-audit-rbac-consistency.md`.

---

## Bloque A — Corrección F-01 (primera pasada)

- [x] **T-001** Corregir `HasFunctionPermission` → `FunctionPermission`
  en `source/normativa/restricciones/cnst-010-permission-class-explicita-en-vistas-drf.rst`
  (líneas 74 y 87).
- [x] **T-002** Commit y push

---

## Bloque B — Corrección F-02/F-03 (adr-back-006 + adr-back-005)

- [x] **T-003** Corregir `adr-back-006` §6: `GranularPermission` →
  `FunctionPermission`; `user_has_function()` → `FunctionAuthorization`
  backend (CIA-RBAC-002 DEC-003/DEC-005).
- [x] **T-004** Ampliar nota en `adr-back-005`: añadir renames
  `GranularPermission` → `FunctionPermission` y
  `GranularPermissionMixin` → `FunctionPermissionMixin`
  (CIA-RBAC-002 DEC-005) al bloque `.. note::` existente.
- [x] **T-005** Commit y push

---

## Bloque C — Corrección MODULE-NNN (29 archivos)

- [x] **T-006** Reemplazar MODULE-NNN function IDs con codenames en 29
  archivos `source/` (ver commit 4242a7f).

---

## Bloque D — Segunda pasada (hallazgos F-01..F-06 del deep audit)

- [x] **T-007** Corregir `br-006` §5.1: `:ref:\`cnst-012\`` →
  `:ref:\`cnst-029\`` (cnst-012 es Serializer Validation, no RBAC).
- [x] **T-008** Corregir `br-006` §4.2: `AGR-001 a AGR-010` →
  `AGR-001 a AGR-012` (el modelo v5.5.0 tiene 12 AGRs).
- [x] **T-009** Corregir `br-007` §7: reemplazar los 3 ejemplos SoD
  erróneos con las parejas correctas per cnst-030:
  - SOD_001: `view_pipeline_status vs view_audit_log`
  - SOD_002: `create_users vs view_audit_log`
  - SOD_003: `assign_functions vs view_audit_log`
- [x] **T-010** Corregir `glosario.rst`: `usuario_tiene_permiso` →
  `user_has_function`; `verificar_permiso_y_auditar` →
  `check_function_and_audit`.
- [x] **T-011** Corregir `analisis-dominio.rst:561`: `usuario_tiene_permiso()`
  → `user_has_function()`.
- [x] **T-012** Commit y push

---

## Orden de ejecución

```
T-001 → T-002 → T-003 → T-004 → T-005
T-006 (ya completo)
T-007 → T-008 → T-009 → T-010 → T-011 → T-012
```
