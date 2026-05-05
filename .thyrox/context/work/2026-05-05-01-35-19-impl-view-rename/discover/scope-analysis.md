```yml
created_at: 2026-05-05 01:35:19
project: THYROX
work_package: 2026-05-05-01-35-19-impl-view-rename
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP impl-view-rename — Scope Analysis

## Problema

Los 13 archivos en `source/arquitectura-tecnica/implementation-view/` se llaman
`mod-*.rst` — prefijo idéntico al de `use-case-view/` y `design-view/`.

El prefijo `mod-` es módulo-céntrico: describe QUÉ MÓDULO cubre el archivo, pero
no QUÉ VISTA ni QUÉ TIPO DE DIAGRAMA. Esto viola el principio de que los nombres
de archivo deben ser auto-descriptivos cuando se ven fuera de su directorio.

**Evidencia del problema:**
- `process-view/proc-etl-pipeline.rst` → correcto: `proc-` codifica la vista
- `system-view/componentes-sistema-iact.rst` → correcto: tipo de diagrama en el nombre
- `implementation-view/mod-auth.rst` → incorrecto: mismo nombre que en design-view y use-case-view

**Tipo de diagrama real en implementation-view:** componentes (Component Diagram)
— capas `<<api>>`, `<<serializer>>`, `<<service>>`, `<<repository>>`, `<<orm>>`

**Prefijo correcto:** `impl-` (confirma el anchor RST ya existente: `.. _at_impl_mod_auth:`)

## Archivos a renombrar (13 + 1 index)

| Nombre actual | Nombre correcto | Anchor RST (no cambia) |
|--------------|----------------|------------------------|
| `mod-access.rst` | `impl-access.rst` | `at_impl_mod_access` |
| `mod-admin.rst` | `impl-admin.rst` | `at_impl_mod_admin` |
| `mod-alerts.rst` | `impl-alerts.rst` | `at_impl_mod_alerts` |
| `mod-audit.rst` | `impl-audit.rst` | `at_impl_mod_audit` |
| `mod-auth.rst` | `impl-auth.rst` | `at_impl_mod_auth` |
| `mod-caller.rst` | `impl-caller.rst` | `at_impl_mod_caller` |
| `mod-logs.rst` | `impl-logs.rst` | `at_impl_mod_sys_logs` |
| `mod-operator.rst` | `impl-operator.rst` | `at_impl_mod_operator_calls` |
| `mod-permissions.rst` | `impl-permissions.rst` | `at_impl_mod_permissions` |
| `mod-pipeline.rst` | `impl-pipeline.rst` | `at_impl_mod_etl_monitoring` |
| `mod-reports.rst` | `impl-reports.rst` | `at_impl_mod_vis_reports` |
| `mod-supervision.rst` | `impl-supervision.rst` | `at_impl_mod_supervision` |
| `mod-users.rst` | `impl-users.rst` | `at_impl_mod_users` |
| `index.rst` | `index.rst` (toctree actualizado) | — |

## Cross-references externas (PROVEN via grep)

**Cross-refs entrantes a `implementation-view/mod-*.rst` desde fuera del directorio:**
- NINGUNA (grep de `implementation-view/mod-` en todo source/ → 0 resultados)

**Cross-refs salientes desde archivos impl-view (seealso blocks):**
- Solo apuntan a `domain-model/`, `use-case-view/`, `process-view/`, `vistas-kruchten`
- Ninguna de estas cambia con este WP

## Archivos afectados

- 13 renombres de archivo (git mv)
- 1 actualización de toctree en `implementation-view/index.rst`
- 0 actualizaciones de cross-refs externas

## Criterios de exit

- `make html` → `build succeeded.` EXIT:0, 0 warnings
- Los 13 archivos tienen nombre `impl-*.rst` en el directorio
- `implementation-view/index.rst` toctree apunta a `impl-*` correctamente
- Los anchors RST internos (`.. _at_impl_*`) se conservan sin cambio
