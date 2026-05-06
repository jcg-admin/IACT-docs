```yml
created_at: 2026-05-06 10:08:00
project: IACT-docs
work_package: 2026-05-06-10-03-46-mapeo-uc-completion
phase: Phase 10 — EXECUTE (B-1 done)
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

## Pendiente detectado durante DISCOVER

- Frontend menu visibility per RBAC: existe UC_PERM_08 ("Menú
  dinámico") según el ejecutor. Verificar que:
  - Está documentado consistentemente
  - Aparece en el mapeo-uc (puede requerir entrada adicional)
  - Está mapeado a las funciones de MOD_Permissions
  - WP separado pendiente de bootstrap.
