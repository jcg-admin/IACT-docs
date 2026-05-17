```yml
created_at: 2026-05-04 07:53:00
project: IACT-docs
work_package: 2026-05-04-07-53-00-function-naming-legacy-ids
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — Migración IDs Legacy (AUTH-NNN, USR-NNN...) a Codenames

Reemplazar identificadores numéricos de función (AUTH-001, USR-003,
ACC-005, ALR-NNN, AUD-NNN, LOG-NNN, SUP-NNN) por sus codenames
semánticos canónicos en todos los documentos donde funcionan como
referencias activas (no en contexto histórico/changelog).

Mapa de sustitución: ver discover/function-naming-legacy-ids-analysis.md.

---

## Bloque A — Bounded contexts (UML class diagrams)

- [x] **T-001** `bounded-context-rbac.rst`: reemplazar `<<ACC-004>>`→
  `<<assign_function_groups>>`, `<<ACC-006>>`→`<<create_function_group>>`,
  `<<ACC-007>>`→`<<assign_functions_to_group>>`, `<<ACC-008>>`→
  `<<revoke_function_group>>`, `<<ACC-009>>`→`<<grant_exceptional_permission>>`,
  `<<ACC-010>>`→`<<revoke_exceptional_permission>>`,
  `<<ACC-005>>`→`<<view_separation_rules>>` (en `+ create()`),
  `<<ACC-011>>`→`<<update_separation_rule>>`,
  `<<ACC-012>>`→`<<disable_separation_rule>>`.
  Nota especial: `+ create() <<ACC-005>>` corrección → `<<create_separation_rule>>`.
- [x] **T-002** `bounded-context-audit.rst`: `<<AUD-001>>`→`<<view_audit_log>>`,
  `<<AUD-002>>`→`<<search_audit_log>>`, `<<AUD-003>>`→`<<export_audit_log>>`,
  `<<AUD-004>>`→`<<generate_compliance_report>>`.
- [x] **T-003** `bounded-context-auth.rst`: `<<AUTH-004>>`→
  `<<view_all_active_sessions>>`, `<<AUTH-001>>`→`<<view_own_sessions>>`.
- [x] **T-004** `bounded-context-alerts.rst`: ALR-NNN → codenames
  (view_alerts, configure_alerts, etc.).
- [x] **T-005** `bounded-context-logs.rst`: LOG-NNN → codenames
  (view_application_logs, export_logs, etc.).

## Bloque B — Matriz de dependencias

- [x] **T-006** `matriz-dependencias-uc-iact.rst`: reemplazar `ACC-NNN codename`
  → solo codename; `AUTH-NNN codename` → codename; `USR-NNN codename`→
  codename; `AUD-NNN codename` → codename; `ALR-NNN codename` → codename.
  Regla: `ACC-001 \`\`assign_functions\`\`` → `\`\`assign_functions\`\``.

## Bloque C — Grupos, SoD, RACI, supervisión

- [x] **T-007** `grupos-funciones.rst`: reemplazar IDs en tablas de grupos.
- [x] **T-008** `sod.rst`: reemplazar IDs en definición de reglas SoD.
- [x] **T-009** `raci-rbac-iact/convenciones.rst`: reemplazar `SUP-001..003`
  con codenames.
- [x] **T-010** `modulos/supervision/index.rst`: `SUP-NNN codename` → codename.

## Bloque D — Base cognitiva y modelo de dominio

- [x] **T-011** `fnd-00-contexto-y-jerarquia.rst`: `AUD-003` → `export_audit_log`,
  `LOG-002` → `export_logs`.
- [x] **T-012** `modelo-dominio-iact.rst`: `ALR-007` → `acknowledge_alert`.

## Bloque E — Normativos y procedimientos (verificar contexto)

- [x] **T-013** `adr-gob-009-rbac-modelo-conceptual.rst`: verificado — IDs son
  changelog de renames históricos (PRESERVAR per regla de preservación).
- [x] **T-014** `guia-completa-desarrollo-features.rst`: verificado — RF-AUTH-NNN
  son IDs de requisito funcional (RF- prefix), no function IDs (PRESERVAR).
- [x] **T-015** `proc-qa-002-estrategia-qa.rst`: verificado — TC-USR-NNN son
  test case IDs (TC- prefix), no function IDs (PRESERVAR).
- [x] **T-016** `cnst-030-reglas-de-separacion-de-funciones-sod.rst`:
  AUD-001..004 parenthetical → '4 funciones' (codenames ya presentes).
- [x] **T-017** `tpl-br-decision-tipo.rst`: verificado — SUP-001 es entity ID
  en SQL ejemplo (supervisor_id = 'SUP-001'), no function ID (PRESERVAR).
- [x] **T-018** `tpl-fr-documentacion-10-componentes.rst`: verificado — USR-001
  es user_id en JSON ejemplo, no function ID (PRESERVAR).

## Bloque F — Cierre

- [x] **T-019** Commit y push.

---

## Regla de preservación (NO CAMBIAR)

Los siguientes contextos NO se modifican:
- Changelog notes del catálogo: `ACC-005 RENAME manage_separation_rules →...`
- `BRQ-AUTH-NNN`, `BRQ-USR-NNN`: son IDs de Business Requirements, no funciones
- `cia-rbac-002 §14.1`: usa AUTH-001 como ejemplo negativo (argumento del texto)
- `analisis-errores-modelo-rbac-v5-2-0.rst`: registro histórico
- `formalizacion-modelo-rbac.rst`: registro histórico

## Orden de ejecución

```
T-001..T-005 (paralelo, bounded contexts) →
T-006 (matriz) →
T-007..T-010 (paralelo, catálogo/raci) →
T-011..T-012 (paralelo, base cognitiva) →
T-013..T-018 (paralelo, normativos) →
T-019
```
