```yml
created_at: 2026-05-04 07:25:32
project: IACT-docs
work_package: 2026-05-04-07-25-32-exceptional-permission-naming
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — ExceptionalPermission Naming

Corregir `ExceptionalGrant` → `ExceptionalPermission` en el único
archivo donde aparece el nombre incorrecto.

---

## Bloque A — Corrección

- [x] **T-001** `adr-back-006-rbac-estrategia-implementacion.rst` §2.4:
  cambiar `ExceptionalGrant` → `ExceptionalPermission` en la tabla de
  modelos Django (línea 191).
- [ ] **T-002** Commit y push.

---

## Orden de ejecución

```
T-001 → T-002
```
