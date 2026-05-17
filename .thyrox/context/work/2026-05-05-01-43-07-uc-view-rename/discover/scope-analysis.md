```yml
created_at: 2026-05-05 01:43:07
project: THYROX
work_package: 2026-05-05-01-43-07-uc-view-rename
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP uc-view-rename — Scope Analysis

## Problema

Los 13 archivos en `source/arquitectura-tecnica/use-case-view/` se llaman
`mod-*.rst`. El prefijo `mod-` es módulo-céntrico y no encoda el tipo de
diagrama — igual que el problema ya corregido en `design-view/` y
`implementation-view/`.

La convención correcta (establecida por los WPs anteriores):

| Vista | Diagrama | Prefijo |
|-------|---------|---------|
| `design-view/` | Secuencia | `seq-` ✓ (ya corregido) |
| `implementation-view/` | Componentes | `impl-` ✓ (ya corregido) |
| `use-case-view/` | Casos de uso | `uc-` ← este WP |
| `process-view/` | Proceso concurrente | `proc-` ✓ (siempre correcto) |

**Prefijo correcto:** `uc-` → `uc-auth.rst`, `uc-users.rst`, etc.

## Archivos a renombrar (13 + 1 index)

| Nombre actual | Nombre correcto | Anchor RST (no cambia) |
|--------------|----------------|------------------------|
| `mod-access.rst` | `uc-access.rst` | `at_uc_mod_access` |
| `mod-admin.rst` | `uc-admin.rst` | `at_uc_mod_admin` |
| `mod-alerts.rst` | `uc-alerts.rst` | `at_uc_mod_alerts` |
| `mod-audit.rst` | `uc-audit.rst` | `at_uc_mod_audit` |
| `mod-auth.rst` | `uc-auth.rst` | `at_uc_mod_auth` |
| `mod-caller.rst` | `uc-caller.rst` | `at_uc_mod_caller` |
| `mod-logs.rst` | `uc-logs.rst` | `at_uc_mod_logs` |
| `mod-operator.rst` | `uc-operator.rst` | `at_uc_mod_operator` |
| `mod-permissions.rst` | `uc-permissions.rst` | `at_uc_mod_permissions` |
| `mod-pipeline.rst` | `uc-pipeline.rst` | `at_uc_mod_pipeline` |
| `mod-reports.rst` | `uc-reports.rst` | `at_uc_mod_reports` |
| `mod-supervision.rst` | `uc-supervision.rst` | `at_uc_mod_supervision` |
| `mod-users.rst` | `uc-users.rst` | `at_uc_mod_users` |
| `index.rst` | `index.rst` (toctree actualizado) | — |

## Cross-references externas (PROVEN via grep — 19 referencias en 6 archivos)

A diferencia de `design-view/` e `implementation-view/`, esta vista SÍ tiene
referencias externas que deben actualizarse:

### 1. `diagramas-uc-por-modulo.rst` (13 entradas en toctree)

```
use-case-view/mod-auth         → use-case-view/uc-auth
use-case-view/mod-users        → use-case-view/uc-users
use-case-view/mod-access       → use-case-view/uc-access
use-case-view/mod-permissions  → use-case-view/uc-permissions
use-case-view/mod-reports      → use-case-view/uc-reports
use-case-view/mod-alerts       → use-case-view/uc-alerts
use-case-view/mod-pipeline     → use-case-view/uc-pipeline
use-case-view/mod-audit        → use-case-view/uc-audit
use-case-view/mod-logs         → use-case-view/uc-logs
use-case-view/mod-operator     → use-case-view/uc-operator
use-case-view/mod-supervision  → use-case-view/uc-supervision
use-case-view/mod-caller       → use-case-view/uc-caller
use-case-view/mod-admin        → use-case-view/uc-admin
```

### 2. `requisitos/casos-uso/admin/index.rst` (1 ref `:doc:`)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-admin`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-admin`
```

### 3. `requisitos/casos-uso/admin/uc-adm-01/informacion-general.rst` (1 ref)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-admin`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-admin`
```

### 4. `requisitos/casos-uso/admin/uc-adm-02/informacion-general.rst` (1 ref)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-admin`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-admin`
```

### 5. `requisitos/casos-uso/admin/uc-adm-03/informacion-general.rst` (1 ref)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-admin`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-admin`
```

### 6. `implementation-view/impl-caller.rst` (1 ref `:doc:`)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-caller`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-caller`
```

### 7. `design-view/seq-caller.rst` (1 ref `:doc:`)

```
:doc:`/arquitectura-tecnica/use-case-view/mod-caller`
→ :doc:`/arquitectura-tecnica/use-case-view/uc-caller`
```

## Resumen de archivos afectados

| Archivo | Operación |
|---------|-----------|
| `use-case-view/mod-*.rst` × 13 | `git mv` → `uc-*.rst` |
| `use-case-view/index.rst` | toctree: `mod-*` → `uc-*` (13 entradas) |
| `arquitectura-tecnica/diagramas-uc-por-modulo.rst` | toctree: `use-case-view/mod-*` → `use-case-view/uc-*` (13 entradas) |
| `requisitos/casos-uso/admin/index.rst` | `:doc:` ref: `mod-admin` → `uc-admin` |
| `requisitos/casos-uso/admin/uc-adm-01/informacion-general.rst` | `:doc:` ref |
| `requisitos/casos-uso/admin/uc-adm-02/informacion-general.rst` | `:doc:` ref |
| `requisitos/casos-uso/admin/uc-adm-03/informacion-general.rst` | `:doc:` ref |
| `implementation-view/impl-caller.rst` | seealso `:doc:` ref |
| `design-view/seq-caller.rst` | seealso `:doc:` ref |

**Total: 13 renames + 9 actualizaciones de referencias**

## Criterios de exit

- `make html` → `build succeeded.` EXIT:0, 0 warnings
- Los 13 archivos tienen nombre `uc-*.rst` en `use-case-view/`
- Todos los toctrees y `:doc:` refs apuntan a `uc-*` correctamente
- Los anchors RST internos (`.. _at_uc_mod_*`) se conservan sin cambio
- El warning "document referenced in multiple toctrees" eliminado
