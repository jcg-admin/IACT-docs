```yml
created_at: 2026-05-04 07:53:00
project: IACT-docs
work_package: 2026-05-04-07-53-00-function-naming-legacy-ids
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Discover — Migración de IDs Legacy (AUTH-NNN, USR-NNN...) a Codenames

## Problema

Las funciones RBAC tienen dos formas de identificación:
1. **ID interno de catálogo** (legacy): `AUTH-001`, `USR-003`, `ACC-005`, etc.
2. **Codename semántico** (canónico): `view_own_sessions`, `deactivate_users`, `view_separation_rules`

El codename es el identificador canónico en Django (`has_perm(codename)`,
`calculate_effective_functions()`, UC specs). Los IDs numéricos son
artefactos del proceso de construcción del catálogo — no identidades
de autorización.

`cia-rbac-002 §14.1` lo confirma (PROVEN): "El campo `function_id`
(`AUTH-001`) es un identificador de catálogo, no un identificador de
autorización. El campo `name` (`manage_sessions`) es el identificador
semántico que opera en el plano del código."

## Hallazgos (PROVEN — grep ejecutado)

**214 ocurrencias brutas** en 55 archivos.
**151 ocurrencias activas** (excluyendo changelog, rename notes,
`BRQ-` prefix) en 23 archivos.

## Mapa completo ID → Codename (verificado en catalogo-funciones.rst)

### MOD_Auth
| ID | Codename |
|----|----------|
| AUTH-001 | `view_own_sessions` |
| AUTH-002 | `close_user_session` |
| AUTH-003 | `reset_password` |
| AUTH-004 | `view_all_active_sessions` |

### MOD_Users
| ID | Codename |
|----|----------|
| USR-001 | `create_users` |
| USR-002 | `update_users` |
| USR-003 | `deactivate_users` |
| USR-004 | `list_users` |
| USR-005 | `search_users` |
| USR-006 | `block_users` |
| USR-007 | `unblock_users` |
| USR-008 | `reactivate_users` |
| USR-009 | `view_users` |
| USR-010 | ELIMINADA v5.2.0 |

### MOD_Access
| ID | Codename |
|----|----------|
| ACC-001 | `assign_functions` |
| ACC-002 | `revoke_functions` |
| ACC-003 | `view_assignments` |
| ACC-004 | `assign_function_groups` |
| ACC-005 | `view_separation_rules` (RENAME desde `manage_separation_rules`) |
| ACC-006 | ELIMINADA v5.2.0 (era `create_function_group` — migrado a PERM) |
| ACC-007 | `assign_functions_to_group` (migrado a PERM) |
| ACC-008 | `revoke_function_group` (migrado a PERM) |
| ACC-009 | `grant_exceptional_permission` |
| ACC-010 | `revoke_exceptional_permission` |
| ACC-011 | `update_separation_rule` (NUEVA v5.4.0) |
| ACC-012 | `disable_separation_rule` (NUEVA v5.4.0) |

### MOD_Alerts (ALR)
| ID | Codename |
|----|----------|
| ALR-001 | `view_alerts` |
| ALR-002 | `configure_alerts` |
| ALR-003 | `configure_team_alerts` |
| ALR-004 | `pause_alerts` |
| ALR-005 | `disable_alerts` (RENAME desde `delete_alerts`) |
| ALR-006 | `view_alert_history` |
| ALR-007 | `acknowledge_alert` (NUEVA) |
| ALR-008 | `subscribe_to_alert` |
| ALR-009 | `unsubscribe_from_alert` |
| ALR-010 | `configure_subscription_severity` |

### MOD_Audit (AUD)
| ID | Codename |
|----|----------|
| AUD-001 | `view_audit_log` |
| AUD-002 | `search_audit_log` |
| AUD-003 | `export_audit_log` |
| AUD-004 | `generate_compliance_report` |

### MOD_Logs (LOG)
| ID | Codename |
|----|----------|
| LOG-001 | `view_application_logs` (RENAME desde `view_technical_logs`) |
| LOG-002 | `export_logs` |
| LOG-003 | `search_logs` |
| LOG-004 | `view_etl_logs` (NUEVA) |
| LOG-005 | `view_infrastructure_logs` (NUEVA) |
| LOG-006 | `view_system_health` (NUEVA) |
| LOG-007 | `view_technical_metrics` (NUEVA) |

### MOD_Supervision (SUP)
| ID | Codename |
|----|----------|
| SUP-001 | `monitor_live_calls` |
| SUP-002 | `barge_in_calls` |
| SUP-003 | `broadcast_team_messages` |

## Archivos a modificar (23 archivos, 151 ocurrencias activas)

### Prioridad ALTA — arquitectura activa referenciada
1. `bounded-context-rbac.rst` — UML `<<ACC-NNN>>` en class methods
2. `bounded-context-audit.rst` — UML `<<AUD-NNN>>`
3. `bounded-context-auth.rst` — UML `<<AUTH-NNN>>`
4. `bounded-context-alerts.rst` — UML `<<ALR-NNN>>`
5. `bounded-context-logs.rst` — UML `<<LOG-NNN>>`
6. `matriz-dependencias-uc-iact.rst` — lista `ACC-NNN codename` → solo codename

### Prioridad MEDIA — catálogo y grupos
7. `catalogo-funciones.rst` — changelog notes (mantener historia, no son IDs activos)
8. `grupos-funciones.rst` — referencias en tabla de grupos
9. `sod.rst` — referencias SoD
10. `convenciones.rst` (raci-rbac) — referencias en tabla de convenciones
11. `modulos/supervision/index.rst` — `SUP-001 codename` → solo codename

### Prioridad BAJA — documentos históricos/normativos
12. `fnd-00-contexto-y-jerarquia.rst` — referencias en contexto conceptual
13. `modelo-dominio-iact.rst` — notas de pendientes
14. `cia-rbac-002-arquitectura-permisos-drf.rst` — uso como ejemplo negativo (NO cambiar §14)
15. `analisis-errores-modelo-rbac-v5-2-0.rst` — historia (NO cambiar)
16. `formalizacion-modelo-rbac.rst` — historia (NO cambiar)
17. `deep-review-rbac-coherencia-artefactos-canonicos.rst` — análisis (verificar contexto)
18. `tpl-br-decision-tipo.rst` — template
19. `tpl-fr-documentacion-10-componentes.rst` — template
20. `adr-gob-009-rbac-modelo-conceptual.rst` — normativa
21. `guia-completa-desarrollo-features.rst` — procedimiento
22. `proc-qa-002-estrategia-qa.rst` — procedimiento
23. `cnst-030-reglas-de-separacion-de-funciones-sod.rst` — restricción

## Regla de qué cambiar y qué preservar

**CAMBIAR** (ID usado como identificador activo de función):
```
<<ACC-001>> → <<assign_functions>>
- ACC-001 ``assign_functions`` → ``assign_functions``
SUP-001 ``monitor_live_calls`` → ``monitor_live_calls``
```

**PRESERVAR** (contexto histórico / evidencia / cia):
```
- ACC-005 RENAME ``manage_separation_rules`` → ``view_separation_rules``
- AUTH-001 (ejemplo negativo en cia-rbac-002 §14)
- BRQ-AUTH-001..005 (son IDs de business requirements, no functions)
- analisis-errores-modelo-rbac-v5-2-0.rst (registro histórico)
```

## Notas especiales

### ACC-006 eliminada
`bounded-context-rbac.rst` tiene `<<ACC-006>>` en `create_function_group()`.
ACC-006 fue eliminada en v5.2.0. `create_function_group` migró a PERM
(es `UC_PERM_05`). La notación correcta: `<<create_function_group>>`.

### ACC-005 ambiguo (view vs. CRUD)
El bounded-context muestra:
- `+ create()  <<ACC-005>>` — INCORRECTO: create_separation_rule es ACC-ADM-001 ahora
- `+ view()    <<ACC-005 view_separation_rules>>` — el rename está anotado

La corrección será:
- `+ create()   <<create_separation_rule>>` (ADM)
- `+ view()     <<view_separation_rules>>`
- `+ update_separation_rule()  <<update_separation_rule>>`
- `+ disable_separation_rule() <<disable_separation_rule>>`
```
