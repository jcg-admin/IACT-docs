```yml
project: IACT-docs
work_package: 2026-05-06-10-03-46-mapeo-uc-completion
created_at: 2026-05-06 10:03:46
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño (Stages 1, 3, 10, 11)
target: Completar y corregir mapeo-uc.rst — 8 funciones de MOD_Access faltan, 3 de MOD_Reports faltan, los 3 funciones reales de MOD_Admin estan ausentes, y 3 entradas estan miscategorizadas como Admin cuando son Access. Quitar entrada read_own_mailbox (Operator es reservado).
predecessor_wp: 2026-05-06-09-17-55-uc-opr-sup-reserved-open-closed (cerrado funcionalmente, B-1..B-8)
trigger: Diff automatico catalogo vs mapeo detecto gaps al verificar coherencia v5.6.0.
```

# WP — Mapeo-UC Completion

## Trigger

El WP predecesor introdujo nota de scope `:64 funciones in-scope:`
en mapeo-uc.rst. Verificacion automatica (diff entre catalogo
fuente-de-verdad y mapeo) detecto:

1. **MOD_Access incompleto:** mapeo tiene 4 entradas, catalogo
   declara 12 → faltan 8.
2. **MOD_Reports incompleto:** mapeo tiene 8, catalogo declara 11
   → faltan 3 (`schedule_report`, `save_view`, `share_report`).
3. **MOD_Admin miscategorizado:** mapeo tiene 3 entradas etiquetadas
   "Admin" pero son funciones de MOD_Access (`view_separation_rules`,
   `update_separation_rule`, `disable_separation_rule`). Las 3
   funciones reales de MOD_Admin (`create_separation_rule`,
   `manage_function_catalog`, `assign_functions_to_group`)
   estan ausentes.
4. **MOD_Operator viola scope nota:** la nota declara que las
   funciones reservadas estan fuera del mapeo, pero
   `read_own_mailbox` aparece. Quitar.

## Bugs detectados (severidad)

| # | Bug | Severidad |
|---|---|---|
| F-01 | 3 entradas miscategorizadas Access→Admin | CRITICO (UCs apuntan al modulo equivocado) |
| F-02 | 3 funciones reales de MOD_Admin ausentes | CRITICO (modulo activo sin mapeo) |
| F-03 | 8 funciones de MOD_Access faltan | ALTO (modulo core RBAC incompleto) |
| F-04 | 3 funciones de MOD_Reports faltan | MEDIO (incompleto pero el resto cubre el dominio) |
| F-05 | `read_own_mailbox` viola scope nota | BAJO (entrada reservada filtrada) |

## Plan de batch único

1. **B-1**: Reescribir tabla 10.1 con 64 entradas correctas
   (todas las activas in-scope), agrupadas por módulo en orden
   del catálogo. Quitar OPR/SUP. Strict build.

## Restricciones

- NO inventar UCs — usar UCs declarados en `informacion-general.rst`
  de cada función del catálogo (columna UC).
- Si un UC no esta declarado en el catalogo, marcar como `(pendiente)`.
- Strict build (`-W`) tras edición.
- Tim Pope commit.

## Riesgos

| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | UC ID en catalogo no coincide con UC ID en mapeo (ej: `UC-005` vs `uc-auth-05`) | Preservar IDs originales del mapeo donde existen; usar IDs del catálogo para nuevas entradas |
| R-02 | Entradas existentes "view_separation_rules" miscategorizadas pueden estar referidas en otros docs | Mover (no eliminar) la categoría, preservar UC ID |

## Stopping points

- **SP-01** (gate humano): el ejecutor declaró "ya no necesitas el gate humano".
- **SP-02** (gate técnico): build strict 0 warnings.
