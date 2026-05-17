```yml
created_at: 2026-05-06 10:08:00
project: IACT-docs
work_package: 2026-05-06-10-03-46-mapeo-uc-completion
phase: Phase 10 — EXECUTE (B-1..B-5 done)
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — Mapeo-UC Completion

## B-1 — Reescritura completa de tabla 10.1

**Bugs detectados durante DISCOVER (diff catálogo vs mapeo):**

| # | Bug | Severidad | Resolución |
|---|---|---|---|
| F-01 | 3 entradas miscategorizadas Access→Admin | CRITICO | Movidas a Access (categoría correcta) |
| F-02 | 3 funciones reales de MOD_Admin ausentes | CRITICO | Agregadas: `create_separation_rule`, `manage_function_catalog`, `assign_functions_to_group` |
| F-03 | 8 funciones de MOD_Access faltantes | ALTO | Agregadas (PERM-related: assign_functions_to_group, grant/revoke_exceptional_permission, revoke_function_group, create_function_group + las 3 de F-01) |
| F-04 | 3 funciones de MOD_Reports faltantes | MEDIO | Agregadas: `schedule_report`, `save_view`, `share_report` |
| F-05 | `read_own_mailbox` (OPR) viola scope nota | BAJO | Eliminada (OPR/SUP son reservadas open-closed) |

**Resultado:** tabla 10.1 ahora declara exactamente las **64 funciones
in-scope** distribuidas en 9 módulos:

- Auth: 4
- Users: 9
- Access: 12 (antes 4)
- Pipeline: 4
- Reports: 11 (antes 8)
- Alerts: 10
- Audit: 4
- Logs: 7
- Admin: 3 (antes miscategorizado)
- **Total: 64** ✅

UC IDs preservados de la tabla anterior donde existían (curated por
el autor); nuevos del catálogo donde no.

Strict build (sphinx -W): EXIT=0.

## B-2 — Domain-model post-bump v5.6.0

- `arquitectura-tecnica/domain-model/overview.rst:41-42`: residuo del
  bump automático del WP-1 (`74 funciones RBAC v5.6.0 activas`).
  Corregido a `64 funciones activas (77 declaradas, 13 reservadas
  open-closed para MOD_Operator y MOD_Supervision)`.
- `arquitectura-tecnica/domain-model/strategy-pattern.rst`: agregada
  `.. note::` declarando que las strategies `DispatchModeStrategy`,
  `HoldMessageStrategy` y `DispositionPromptStrategy` (UC_OPR_03/04/06)
  son extension points open-closed (out-of-scope para v5.6.0).

## B-3 — Tabla de módulos en `fnd-00-contexto-y-jerarquia.rst`

§1.3.2 Módulos Funcionales tenía 3 bugs:

1. Header decía "8 Módulos Funcionales" pero la tabla listaba 11 →
   corregido a "Los Módulos Funcionales" sin número en header.
2. Texto decía "12 módulos" pero la tabla tenía 11 (faltaba ADM y
   Caller no estaba clasificado) → expandido a 13 módulos UC con
   columna `Status v5.6.0`.
3. Faltaba MOD_Admin (NUEVO v5.6.0) → agregado con status
   "Activo (NUEVO v5.6.0)".

Adicionalmente §4 "Próximos Pasos" actualizado: "12 módulos" →
"13 módulos UC".

## B-4 — Refs "12 modulos" en backend, normativa y arquitectura

Casos detectados (8 archivos):

| Archivo | Antes | Después |
|---|---|---|
| `requisitos/_metodologia-aplicacion/plan-documentacion-uc.rst:608` | "12 módulos UC (AUTH..CLI)" sin ADM | "13 módulos UC ... ADM (NUEVO v5.6.0), OPR (reservado), SUP (reservado), CLI" |
| `base-cognitiva/.../txm-02-taxonomia-artefactos.rst:319` | "12 módulos, catálogo v5.5.0" | "13 módulos UC ... catálogo v5.6.0" |
| `backend/conventions.rst:63`, `backend/overview.rst:31,50` | "12 modulos" | "13 modulos UC ... 9 RBAC activos + ADM nuevo + 2 reservados + Caller" |
| `arquitectura-tecnica/modulos/index.rst:17` | "12 modulos funcionales" | "13 modulos UC ... 9 RBAC activos + ADM nuevo v5.6.0 + 2 reservados + Caller" |
| `arquitectura-tecnica/context-view/{context-diagram,stakeholders}.rst` | "12 modulos" | "10 RBAC activos in-scope" / "13 modulos UC" según contexto |
| `normativa/procedimientos/proc-doc-{004,014}.rst` | "12 modulos IACT" | "13 modulos UC v5.6.0" |
| `normativa/gobernanza/adr-gob-008.rst:99` | "(12 modulos)" | "(13 modulos UC: 10 RBAC activos in-scope v5.6.0 + 2 reservados + Caller)" |

Distinción documentada:

- **Módulos UC en filesystem:** 13 (auth, users, access, permissions,
  pipeline, reports, alerts, audit, logs, admin, operator,
  supervision, caller).
- **Módulos RBAC en catálogo:** 11 (Auth, Users, Access, Pipeline,
  Reports, Alerts, Audit, Logs, Operator, Supervision, Admin —
  Permissions coexiste con Access vía ADR-008).
- **Módulos RBAC activos in-scope v5.6.0:** 9 (sin OPR/SUP).

Strict builds (sphinx -W) tras B-2, B-3 y B-4: EXIT=0 cada uno.

## B-5 — Fix sistemático AGR-009/admin_sistema en `fnd-03-casos-de-uso.rst`

`fnd-03-casos-de-uso.rst` mezclaba "AGR-009 admin_sistema" tanto
para UCs del modelo RBAC (UC_ADM) como para UCs de Pipeline
(UC-050..053, UC-070..072) — eso es semánticamente
inconsistente: AGR-009 es `pipeline_admin_group` (sysadmin del
ETL), AGR-010 es `system_admin_group` (admin del modelo RBAC).

Fixes:

- §3.4 tabla "AGRUPADOR FUNCIONES UC TIPICOS":
  - "AGR-009: admin_sistema (...) UC_ADM_01..03" →
    "AGR-010: system_admin (NUEVO v5.6.0 — admin del modelo
    RBAC) UC_ADM_01..03"
  - "AGR-009: admin_sistema (view_pipeline_status, ...)
    UC-050-053, UC-070-072" → "AGR-009: pipeline_admin
    (view_pipeline_status, ...) UC-050-053, UC-070-072"
- §UC_ADM_01: "Actor Primario: AGR-009 (admin_sistema)" →
  "AGR-010 (system_admin)".
- §UC_ACC_09: clarificación dual "AGR-008 para ACC; **AGR-010
  (system_admin)** para ADM".
- Tabla §3.6 R015/R016 MODULES_ADMIN/SYSTEM_ADMIN: AGR-009 →
  AGR-010.

NO tocados (fuera de scope WP):

- `br-001`, `br-002` (operacional ETL — uso de
  `admin_sistema` puede ser legacy, contexto operacional).
- `requisitos-funcionales/users/uc-008-baja, uc-009-listar`
  (refs a "rol admin_sistema" en abstracto — review caso por
  caso requiere WP separado).
- `fnd-04-trazabilidad`, `fnd-03:680, 750` (UCs ETL/logs
  donde el contexto es ambiguo).

## UC_PERM_08 verificado

Existe completo (12 partes) con `:estado: Vigente :version: 5.0.0`.
Función RBAC: implícita `view_own_navigation` (no es función del
catálogo — es UX, accesible para cualquier user autenticado;
seguridad real está en UC_PERM_07). NO requiere agregar al mapeo
porque su función es implícita.
