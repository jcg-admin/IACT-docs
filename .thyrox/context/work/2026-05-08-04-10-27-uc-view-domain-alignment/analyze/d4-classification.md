```yml
created_at: 2026-05-08 04:35:00
project: IACT-docs
work_package: 2026-05-08-04-10-27-uc-view-domain-alignment
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# D4 Clasificación caso por caso — 29 miembros

Aplicando criterio D4: si el miembro UC describe el mismo
concepto del dominio bajo nombre distinto a uno ya presente
en DM, es RENAME (corregir UC). Si describe concepto sin
equivalente en DM, es ADD (agregar a DM).

## Tabla de clasificación

| # | Clase | Miembro UC | UC origen | Equivalente DM | Acción |
|---|---|---|---|---|---|
| 1 | AccessGroup | `agr_code : String` | uc-acc-04 | `agr_id : String <<AGR-001..012>>` | **RENAME UC** → `agr_id` |
| 2 | AccessGroup | `id : UUID` | uc-acc-04 | (ninguno — DM solo tiene `agr_id` business code) | **ADD a DM** |
| 3 | AccessGroup | `is_system : Boolean` | uc-acc-04 | (ninguno) | **ADD a DM** |
| 4 | AccessGroup | `state : AccessGroupState` | uc-acc-04 | (ninguno — DM no modela lifecycle) | **ADD a DM** |
| 5 | AgentReportService | `list()` | uc-rpt-12 | `get(invoker, period, filters)` | **RENAME UC** → `get` |
| 6 | AlertRule | `id` | uc-alr-01 | `rule_id : UUID` | **RENAME UC** → `rule_id` |
| 7 | AlertRule | `state` | uc-alr-01 | `status : RuleState` | **RENAME UC** → `status` |
| 8 | AuditRepo | `query()` | uc-aud-01 | `find(filters, cursor, limit)` | **RENAME UC** → `find` |
| 9 | ErroresETLService | `listar()` | uc-pip-02 | `query(filters, ...)` | **RENAME UC** → `query` |
| 10 | EvaluatorReloader | `reload()` | uc-alr-01 | `reload_all()` / `reload_rule(rule_id)` | **RENAME UC** → `reload_all` |
| 11 | PipelineExecutionRepo | `ejecuciones_recientes()` | uc-pip-01 | (ninguno — DM no tiene "find recientes" generico) | **ADD a DM** |
| 12 | PipelineExecutionRepo | `por_estado()` | uc-pip-02 | `find_by_state(state)` | **RENAME UC** → `find_by_state` |
| 13 | PipelineExecutionRepo | `ultima_ejecucion()` | uc-pip-01 | `last_successful_by_dataset(dataset)` | **RENAME UC** → `last_successful_by_dataset` |
| 14 | RBACRepo | `get_user_segments()` | uc-inc-rpt-01 | (ninguno — DM no expone segments) | **ADD a DM** |
| 15 | RBACRepo | `has_global_capability()` | uc-inc-rpt-01 | (ninguno — DM tiene `is_global_admin`, distinto concepto) | **ADD a DM** |
| 16 | SavedView | `id : UUID` | uc-rpt-10 | `view_id : UUID` | **RENAME UC** → `view_id` |
| 17 | SavedView | `chart_config` | uc-rpt-10 | (ninguno — DM solo modela filters/state/owner) | **ADD a DM** |
| 18 | SavedView | `columns` | uc-rpt-10 | (ninguno) | **ADD a DM** |
| 19 | SavedView | `filters` | uc-rpt-10 | `filters_snapshot : List<Filter>` | **RENAME UC** → `filters_snapshot` |
| 20 | SavedView | `owner` | uc-rpt-10 | `owner_user_id : UUID` | **RENAME UC** → `owner_user_id` |
| 21 | SavedView | `report_type` | uc-rpt-10 | (DM tiene `report_id`, no `report_type`) | **ADD a DM** |
| 22 | SegmentResolver | `invalidate_cache()` | uc-inc-rpt-01 | (ninguno — DM tiene `cache` privado pero sin invalidate publico) | **ADD a DM** |
| 23 | SegmentResolver | `is_global()` | uc-inc-rpt-01 | (ninguno) | **ADD a DM** |
| 24 | Subscription | `id : UUID` | uc-alr-05 | `subscription_id : UUID` | **RENAME UC** → `subscription_id` |
| 25 | Subscription | `user` | uc-alr-05 | `subscriber_user_id : UUID` | **RENAME UC** → `subscriber_user_id` |
| 26 | Subscription | `rule` | uc-alr-05 | `alert_id : UUID` | **RENAME UC** → `alert_id` |
| 27 | Subscription | `scope` | uc-alr-05 | (ninguno — DM no modela scope de subscription) | **ADD a DM** |
| 28 | Subscription | `channel` | uc-alr-05 | (ninguno — DM no modela channel — email/SMS/push) | **ADD a DM** |
| 29 | User | `segment_id` | uc-acc-04 | (ninguno en `user.rst` canonico) | **ADD a DM** |

## Conteo final D4

| Acción | Cuenta | Archivos a tocar |
|---|---|---|
| **RENAME UC** (corregir UC al nombre canonico DM) | **14** | ~6 archivos UC en `casos-uso/*/uc-*/diagramas-uml/` |
| **ADD a DM** (agregar miembro a clase DM) | **15** | ~9 archivos DM en `arquitectura-tecnica/domain-model/` |
| **Total** | **29** | **~15 archivos** |

## Distribución por clase y acción

| Clase | RENAMEs UC | ADDs DM | Total |
|---|---|---|---|
| AccessGroup | 1 | 3 | 4 |
| AgentReportService | 1 | 0 | 1 |
| AlertRule | 2 | 0 | 2 |
| AuditRepo | 1 | 0 | 1 |
| ErroresETLService | 1 | 0 | 1 |
| EvaluatorReloader | 1 | 0 | 1 |
| PipelineExecutionRepo | 2 | 1 | 3 |
| RBACRepo | 0 | 2 | 2 |
| SavedView | 3 | 3 | 6 |
| SegmentResolver | 0 | 2 | 2 |
| Subscription | 3 | 2 | 5 |
| User | 0 | 1 | 1 |
| **Total** | **14** | **15** | **29** |

## Observaciones del análisis

### Patrones detectados

1. **Acrónimo en plural simplificado en UCs:**
   `id` (UC) frecuentemente debería ser el nombre canonico
   prefijado: `view_id`, `rule_id`, `subscription_id`. UCs
   tienden a usar `id` genérico por brevedad.

2. **Spanglish en UCs:**
   `listar`, `por_estado`, `ejecuciones_recientes`,
   `ultima_ejecucion` (UC en español) vs `query`,
   `find_by_state`, `find_*`, `last_*` (DM en inglés). DM
   establece la convención canónica en inglés.

3. **Conceptos faltantes en DM legítimos:**
   `chart_config`, `columns`, `channel`, `scope`, `is_system`,
   `is_global`, `invalidate_cache`, `get_user_segments` —
   son funcionalidades modeladas en UC pero ausentes en DM
   canónico. Son trabajo legítimo de enriquecimiento de DM.

### Riesgos confirmados

- **R-01 atenuado:** la mayoría de los 29 son renombrados (14)
  no adiciones reales (15). El esfuerzo en DM es ~50% del
  estimado original.
- **R-02 cerrado:** `MenuIVRReportService` se aliasa a
  `IVRNavigationReportService` (D5).

## Estimación ajustada Phase 10

| Bloque | Archivos | Trabajo |
|---|---|---|
| D3a — Renames UC (14 miembros) | ~6 archivos UC editar | sed-replaceable, bajo riesgo |
| D3b — Adds DM (15 miembros) | ~9 archivos DM editar | edición caso por caso de class blocks PlantUML |
| D3c — Case mismatch PiiScanner (5 refs UC) | ~5 archivos UC | sed bulk |
| D3d — `MenuIVRReportService` → `IVRNavigationReportService` | refs UC | sed bulk |
| D1 — 48 archivos nuevos uc-usr-05/06/07 | nuevos | trabajo de mayor volumen |
| D1 colateral — 3 view files alineados | 3 archivos | edits puntuales |
| **Total** | **~70 archivos** (3 nuevos compuestos + ~24 edits + 48 specs nuevos) | — |

## Refs

- DISCOVER analysis (`wp-state.md`).
- MEASURE summary (`measure/measure-summary.md`).
- DM bodies dump (`analyze/dm-canonical-bodies.txt`).
