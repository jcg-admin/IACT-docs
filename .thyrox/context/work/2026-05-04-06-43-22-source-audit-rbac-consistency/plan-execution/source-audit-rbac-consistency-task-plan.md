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

## Orden de ejecución

```
T-001 → T-002
```
