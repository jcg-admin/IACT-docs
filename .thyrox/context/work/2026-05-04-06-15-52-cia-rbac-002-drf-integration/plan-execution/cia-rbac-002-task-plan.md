```yml
created_at: 2026-05-04 06:15:52
project: IACT-docs
work_package: 2026-05-04-06-15-52-cia-rbac-002-drf-integration
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — CIA-RBAC-002 + ADR-GOB-010 DRF Integration

Crear documentos CIA-RBAC-002 y ADR-GOB-010, corregir notación
incorrecta de `@require_function` en 3 archivos, actualizar índices.

---

## Bloque A — Estructura y documentos nuevos

- [x] **T-001** Crear `source/gestion/evidencia/rbac-arquitectura/index.rst`
- [x] **T-002** Crear `source/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf.rst`
- [x] **T-003** Crear `source/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend.rst`
- [x] **T-004** Actualizar `source/gestion/evidencia/index.rst` — agregar `rbac-arquitectura/index`
- [x] **T-005** Actualizar `source/normativa/gobernanza/index.rst` — agregar `adr-gob-010`

---

## Bloque B — Corrección de notación incorrecta

- [x] **T-006** Corregir `@require_function('RPT-001')` en `analisis-errores-modelo-rbac-v5-2-0.rst`
- [x] **T-007** Corregir `@require_function('FUNC-NNN')` en `matriz-dependencias-uc-iact.rst`
- [x] **T-008** Corregir `@require_function('F_CODE')` en `uc-perm-07/informacion-general.rst`

---

## Bloque C — Correcciones post-review (6 problemas detectados)

- [x] **T-009** Fix `has_perm` sin filtro `app_label` en DEC-003
- [x] **T-010** Fix `APP_LABEL` fuera de scope en DEC-005
- [x] **T-011** Fix string literal en `FunctionPermission` — usar `FunctionCatalog`
- [x] **T-012** Fix `constants.py` → `catalog.py` en DEC-004
- [x] **T-013** Fix argumento "fuente única de verdad" → separación de dominios
- [x] **T-014** Renombrar `Perm` → `FunctionCatalog` en CIA-RBAC-002 y ADR-GOB-010

---

## Bloque D — Reemplazo completo CIA-RBAC-002 v2.0.0

- [ ] **T-015** Reemplazar CIA-RBAC-002 con versión completa (16 secciones):
  catálogo completo por módulo, tabla de comportamiento backends,
  registro de riesgos, DAG de dependencias, lecciones del análisis,
  mapa de archivos afectados. Corregir referencias ADR (→ adr-gob-010),
  paths RST correctos, sin markdown links en código.
- [ ] **T-016** Commit y push

---

## Orden de ejecución

```
A (T-001..T-005) → B (T-006..T-008) → C (T-009..T-014) → D (T-015..T-016)
```
