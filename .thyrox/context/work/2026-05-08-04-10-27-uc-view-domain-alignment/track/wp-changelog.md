```yml
created_at: 2026-05-08 05:00:00
project: IACT-docs
work_package: 2026-05-08-04-10-27-uc-view-domain-alignment
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — UC ↔ Use-Case-View ↔ Domain-Model alignment

## [1.0.0] — 2026-05-08

### Resumen

Auditoría y alineación cross-corpus entre tres
directorios:

- `source/requisitos/casos-uso/` (88 UCs)
- `source/arquitectura-tecnica/use-case-view/` (88 view files)
- `source/arquitectura-tecnica/domain-model/` (109+ classes)

Resultado: 0 gaps en cross-references, 0 case mismatches,
0 missing class members, 88/88 UCs con spec textual
completa Aprobada (ya no hay UCs Reservado), 88/88 view
files con `left to right direction` (uml-07 conformance
profunda).

### Changed (D3a — 14 renames UC en 8 archivos)

| Task | Archivo | Renames |
|---|---|---|
| T-001 | uc-acc-04 diagrama-de-agr | `agr_code` → `agr_id` |
| T-002 | uc-rpt-12 diagrama-de-clases | `list` → `get` |
| T-003 | uc-alr-01 diagrama-de-clases | `id` → `rule_id`, `state` → `status` |
| T-004 | uc-aud-01 diagrama-de-clases | `query` → `find` |
| T-005 | uc-alr-01 diagrama-de-clases | `reload(rule_id)` → `reload_rule(rule_id)` |
| T-006 | uc-pip-02 diagrama-de-clases | `listar` → `query` |
| T-007 | uc-pip-02 diagrama-de-clases | `por_estado` → `find_by_state` |
| T-008 | uc-pip-01 diagrama-de-clases | `ultima_ejecucion` → `last_successful_by_dataset`, `ejecuciones_recientes` → `find_recent` |
| T-009 | uc-rpt-10 diagrama-de-clases | `id` → `view_id`, `filters` → `filters_snapshot`, `owner` → `owner_user_id` |
| T-010 | uc-alr-05 diagrama-de-clases | `id` → `subscription_id`, `user` → `subscriber_user_id`, `rule` → `alert_id` |

Ajuste durante ejecución T-005: el plan decía `reload` →
`reload_all`, pero el UC original tenía `reload(rule_id)` con
parámetro. Semánticamente coincide con DM `reload_rule(rule_id)`,
no `reload_all()`. Aplicado el match correcto.

### Added (D3b — 15 miembros agregados a domain-model en 7 archivos)

| Task | Clase DM | Miembro agregado | Tipo |
|---|---|---|---|
| T-011 | AccessGroup | `id` | UUID PK técnico |
| T-012 | AccessGroup | `is_system` | Boolean |
| T-013 | AccessGroup | `state`, enum AccessGroupState | AccessGroupState |
| T-014 | PipelineExecutionRepo | `find_recent` | List<PipelineExecution> |
| T-015 | RBACRepo | `get_user_segments` | List<Segment> |
| T-016 | RBACRepo | `has_global_capability` | Boolean |
| T-017 | SavedView | `chart_config` | Map<String, Any> |
| T-018 | SavedView | `columns` | List<String> |
| T-019 | SavedView | `report_type` | ReportType |
| T-020 | SegmentResolver | `invalidate_cache` | void |
| T-021 | SegmentResolver | `is_global` | Boolean |
| T-022 | Subscription | `scope` | SubscriptionScope |
| T-023 | Subscription | `channel` | NotificationChannel |
| T-024 | User | `segment_id` | UUID <<BR-012>> |

Follow-up T-033 también agregó `PIIScanner.sanitize(payload)` a
`pii-scanner.rst` canónico (gap detectado al re-correr el
análisis post-EXECUTE).

### Fixed (D3c — case mismatch + alias en 5 archivos)

| Task | Antes | Después |
|---|---|---|
| T-025 | `PiiScanner` (en 5 archivos) | `PIIScanner` (canónico DM) |
| T-026 | `MenuIVRReportService` (en 2 archivos uc-rpt-16) | `IvrNavigationReportService` (canónico DM, PascalCase) |

Follow-up T-033 corrigió un overshoot inicial: T-026 había
aliased a `IVRNavigationReportService` (mayúsculas) pero el
canónico es `IvrNavigationReportService` (PascalCase). Corregido.

### Added (D1 — 3 UCs nuevos × 17 archivos = 51 archivos nuevos)

| Task | UC | Archivos | Funcion RBAC |
|---|---|---|---|
| T-027 | UC_USR_05 Bloquear Usuario | 17 (12 spec + 5 diagrams) | `block_users` |
| T-028 | UC_USR_06 Desbloquear Usuario | 17 (12 spec + 5 diagrams) | `unblock_users` |
| T-029 | UC_USR_07 Editar Perfil Propio | 17 (12 spec + 5 diagrams) | `edit_own_profile` |

Cada UC promovido de `Reservado v0.1.0` → `Aprobado v1.0.0`,
con resolución explícita de las 3 preguntas pendientes en cada
placeholder original (capability RBAC, alcance, relación con
otros UCs).

### Changed (D1 colateral — 3 view files alineados)

| Task | Archivo | Cambio |
|---|---|---|
| T-030 | use-case-view/users/uc-usr-05-bloquear-usuario.rst | Reservado → Aprobado, agrega `left to right direction`, sincroniza con spec |
| T-031 | use-case-view/users/uc-usr-06-desbloquear-usuario.rst | Idem |
| T-032 | use-case-view/users/uc-usr-07-editar-perfil-propio.rst | Idem |

### Verification

#### T-033 build strict + final cross-ref analysis

Build sphinx strict tras follow-ups: ver
`track/build-logs/sphinx-strict-final2-*.log`.

Cross-ref final en `track/cross-ref-gaps-final.txt`:

```
== POST-EXECUTE FINAL VERIFICATION ==
Classes truly missing in DM: 0
Case mismatches: 0
Classes with missing members: 0
Total missing members: 0
```

#### Conformidad uml-07 final

| Métrica | Antes | Después |
|---|---|---|
| view files con `actor` | 88/88 | 88/88 ✅ |
| view files con `usecase` | 88/88 | 88/88 ✅ |
| view files con `rectangle` system boundary | 88/88 | 88/88 ✅ |
| view files con `left to right direction` | 85/88 | 88/88 ✅ |
| UCs con spec textual completa | 85/88 | 88/88 ✅ |
| UCs con `diagramas-uml/` directorio | 85/88 | 88/88 ✅ |

## Commits del WP

1. `1cc5cf8e` — Phase 1 DISCOVER
2. `89bb190c` — Phase 2 MEASURE
3. `136414b1` — Phase 3 ANALYZE D4 classification
4. `440e6fcd` — Phase 8 PLAN EXECUTION (task plan)
5. `629329e0` — D3a renames UC (T-001..T-010)
6. `710cd5fe` — D3b adds DM (T-011..T-024)
7. `984e032f` — D3c case + alias (T-025..T-026)
8. `ccf6ac54` — T-027 UC_USR_05
9. `b1379bff` — T-028 UC_USR_06
10. `567c7f5e` — T-029 UC_USR_07
11. `52efb2b5` — T-030..T-032 view alignment
12. `898d1d82` — T-033 follow-up fixes
13. (este commit) + build strict OK — TRACK cierre

## Total

- 34 tasks atómicos ejecutados (T-001..T-034)
- ~70 archivos afectados (estimado original ~70 ✅)
  - 8 archivos UC editados (D3a)
  - 7 archivos DM editados (D3b)
  - 5 archivos UC editados (D3c)
  - 51 archivos nuevos (D1: 17 × 3 UCs)
  - 3 archivos view alineados (D1 colateral)
  - 1 archivo PIIScanner (T-033 follow-up)

## Roadmap status final

| Iniciativa | Estado |
|---|---|
| Roadmap CLEAN_CODE remediation (8 WPs + 2 TDs) | ✅ Completado |
| WP uc-view-domain-alignment (este) | ✅ Completado |

## Refs

- Phase 1 DISCOVER: `wp-state.md`
- Phase 2 MEASURE: `measure/measure-summary.md`
- Phase 3 ANALYZE D4: `analyze/d4-classification.md`
- Phase 8 PLAN: `plan-execution/task-plan.md`
- Phase 11 TRACK: `track/cross-ref-gaps-final.txt`,
  `track/build-logs/`
