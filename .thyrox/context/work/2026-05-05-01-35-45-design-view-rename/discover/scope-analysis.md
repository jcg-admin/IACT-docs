```yml
created_at: 2026-05-05 01:35:45
project: THYROX
work_package: 2026-05-05-01-35-45-design-view-rename
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP design-view-rename — Scope Analysis

## Problema

Los 13 archivos en `source/arquitectura-tecnica/design-view/` se llaman
`mod-*.rst` — prefijo idéntico al de `use-case-view/` y `implementation-view/`.

El prefijo `mod-` es módulo-céntrico y no encode el tipo de diagrama.

**Tipo de diagrama real en design-view:** secuencia (Sequence Diagram)
— participantes interactuando (actor → frontend → service → repository → db).
La Design View en el modelo Kruchten 4+1 muestra los patrones de interacción
y flujo de datos en tiempo de diseño.

**Prefijo correcto:** `seq-` (confirma el anchor RST ya existente: `.. _at_design_*`)

## Por qué `seq-` y no otro prefijo

| Opción | Razón |
|--------|-------|
| `seq-auth.rst` | Directo — "sequence diagram of auth". Consistente con `system-view/secuencia-sistema-iact.rst` |
| `design-auth.rst` | Redundante — el directorio ya dice "design-view" |
| `flow-auth.rst` | Semánticamente correcto pero no estándar en el proyecto |
| `mod-auth.rst` | ACTUAL — no encode tipo de diagrama ❌ |

Precedente en el proyecto: `system-view/secuencia-sistema-iact.rst` usa "secuencia".
Pero para consistencia con `process-view/proc-*` (prefijo corto de 4 letras),
se usa `seq-` en lugar de la forma larga.

## Archivos a renombrar (13 + 1 index)

| Nombre actual | Nombre correcto | Anchor RST (no cambia) |
|--------------|----------------|------------------------|
| `mod-access.rst` | `seq-access.rst` | `at_design_mod_access` |
| `mod-admin.rst` | `seq-admin.rst` | `at_design_mod_admin` |
| `mod-alerts.rst` | `seq-alerts.rst` | `at_design_mod_alerts` |
| `mod-audit.rst` | `seq-audit.rst` | `at_design_mod_audit` |
| `mod-auth.rst` | `seq-auth.rst` | `at_design_mod_auth` |
| `mod-caller.rst` | `seq-caller.rst` | `at_design_mod_caller` |
| `mod-logs.rst` | `seq-logs.rst` | `at_design_mod_sys_logs` |
| `mod-operator.rst` | `seq-operator.rst` | `at_design_mod_operator_calls` |
| `mod-permissions.rst` | `seq-permissions.rst` | `at_design_mod_permissions` |
| `mod-pipeline.rst` | `seq-pipeline.rst` | `at_design_mod_etl_monitoring` |
| `mod-reports.rst` | `seq-reports.rst` | `at_design_mod_vis_reports` |
| `mod-supervision.rst` | `seq-supervision.rst` | `at_design_mod_supervision` |
| `mod-users.rst` | `seq-users.rst` | `at_design_mod_user_identity` |
| `index.rst` | `index.rst` (toctree actualizado) | — |

## Cross-references externas (PROVEN via grep)

**Cross-refs entrantes a `design-view/mod-*.rst` desde fuera del directorio:**
- NINGUNA (grep de `design-view/mod-` en todo source/ → 0 resultados)

**Cross-refs salientes desde archivos design-view (seealso blocks):**
- Apuntan a `domain-model/`, `use-case-view/mod-*`, `process-view/`, `deploy-view/`, `vistas-kruchten`
- Ninguna de estas cambia con este WP (salen, no entran)

## Archivos afectados

- 13 renombres de archivo (git mv)
- 1 actualización de toctree en `design-view/index.rst`
- 0 actualizaciones de cross-refs externas

## Criterios de exit

- `make html` → `build succeeded.` EXIT:0, 0 warnings
- Los 13 archivos tienen nombre `seq-*.rst` en el directorio
- `design-view/index.rst` toctree apunta a `seq-*` correctamente
- Los anchors RST internos (`.. _at_design_*`) se conservan sin cambio
