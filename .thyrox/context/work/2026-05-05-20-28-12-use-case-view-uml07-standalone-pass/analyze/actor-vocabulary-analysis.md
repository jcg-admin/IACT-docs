```yml
created_at: 2026-05-05 20:55:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis de vocabulario de actores — uml-07 standalone

## 1. Propósito

Identificar el vocabulario canónico de **actores** que se usará en los 83 archivos
uml-07 standalone. El target del WP especifica:

- **Funciones RBAC** como actores iniciador y beneficiario (P-15 granular).
- **Entidades del domain-model** como actores `<<sistema>>` con nombre canónico.
- **`Caller`** como actor `<<externo>>` para Module caller.

Este documento extrae sistemáticamente el vocabulario actual de los 83 uml-06 existentes
en `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` y lo valida contra
el domain-model canónico (67 archivos en `source/arquitectura-tecnica/domain-model/`).

## 2. Metodología

Script Python (`uc-vocabulary-extraction.json`) con regex sobre los 83 archivos uml-06
extrae:

1. Líneas `actor "label" as alias <<stereotype>>` agrupadas por stereotype.
2. Cross-refs `:doc:` a domain-model.
3. Match de actor `<<sistema>>` contra archivos `domain-model/<entity>.rst`.

Output: `analyze/uc-vocabulary-extraction.json` (machine-readable).

## 3. Hallazgos cuantitativos

### 3.1 Cobertura

| Métrica | Valor |
|---|---|
| UCs procesados | 83 / 83 |
| UCs con diagrama uml-06 existente | 83 / 83 ✓ |
| Funciones RBAC distintas usadas como actor (incluye beneficiarios) | 93 |
| Sistemas distintos como actor `<<sistema>>` | 48 |
| Cross-refs `:doc:` a domain-model | 57 entidades |
| Domain-model files canónicos | 67 |

### 3.2 Funciones RBAC más usadas (top 15)

| Función RBAC | UCs que la usan |
|---|---|
| `view_audit_log` | 37 (beneficiario en cualquier UC con audit emit) |
| `view_reports` | 9 |
| `User destino` (genérico) | 9 |
| `view_separation_rules` | 3 |
| `assign_function_groups` | 2 |
| `grant_exceptional_permission` | 2 |
| `assign_functions_to_group` | 2 |
| `Operator` (rol genérico) | 2 |
| `view_assignments` | 2 |
| `Frontend`, `User`, `Sistema`, etc. | 1-2 cada uno |

**Hallazgos:**

- **Función dominante**: `view_audit_log` aparece en 37 UCs como beneficiario (toda UC
  que emite AuditEvent). Coherente con CNST-025 inmutabilidad y P-44 audit del audit.
- **Inconsistencia detectada**: 9 UCs usan `User destino` (rol genérico, no función)
  como actor. En uml-07 esto debe ser una **función específica** o estar marcado con
  `<<beneficiario>>` sin función — clarificar caso por caso en Phase 7 DESIGN.
- **Pre-existentes mezclan**: los 30 UCs pre-existentes (auth, users, access parcial,
  perm 04-10, rpt 01-09) usan inconsistencias menores como `User`, `Frontend`, `Operator`
  sin función específica.

### 3.3 Sistemas como actores — match contra domain-model

| Sistema (label) | UCs | Match domain-model | Status |
|---|---|---|---|
| `AuditService` | 20 | `audit-service.rst` | ✓ canonical |
| `Call` | 16 | `call.rst` | ✓ canonical |
| `Sistema` | 10 | (placeholder genérico) | ⚠ no es entidad |
| `InternalMailbox` | 7 | `internal-mailbox.rst` | ✓ canonical |
| `EvaluatorReloader` | 6 | `evaluator-reloader.rst` | ✓ canonical |
| `Session` | 6 | `session.rst` | ✓ canonical |
| `KpiCalculator` | 6 | `kpi-calculator.rst` | ✓ canonical |
| `RuleValidator` | 5 | `rule-validator.rst` | ✓ canonical |
| `TimingCalculator` | 5 | `timing-calculator.rst` | ✓ canonical |
| `Sanitizer` | 5 | `sanitizer.rst` | ✓ canonical |
| `PipelineExecution` | 5 | `pipeline-execution.rst` | ✓ canonical |
| `PermissionCache` | 4 | `permission-cache.rst` | ✓ canonical |
| `AlertRepo` | 4 | `alert-repo.rst` | ✓ canonical |
| `PermissionService` | 3 | `permission-service.rst` | ✓ canonical |
| `AlertHook` | 3 | `alert-hook.rst` | ✓ canonical |
| `AuditQueryService` | 3 | `audit-query-service.rst` | ✓ canonical |
| `ExportWorker` | 3 | `export-worker.rst` | ✓ canonical |
| `ExportJob` | 3 | `export-job.rst` | ✓ canonical |
| `PIIScanner` | 3 | `pii-scanner.rst` | ✓ canonical |
| `ApplicationLog` | 3 | `application-log.rst` | ✓ canonical |
| `AuditRepo` | 2 | `audit-repo.rst` | ✓ canonical |
| `PipelineLog` | 2 | `pipeline-log.rst` | ✓ canonical |
| `FilterValidator` | 2 | `filter-validator.rst` | ✓ canonical |
| `CursorEncoder` | 2 | `cursor-encoder.rst` | ✓ canonical |
| `Campaign` | 2 | `campaign.rst` | ✓ canonical |
| `Action` | 2 | `action.rst` | ✓ canonical |
| `AgentDailyStatRepo` | 2 | `agent-daily-stat-repo.rst` | ✓ canonical |
| `SegmentResolver` | 2 | `segment-resolver.rst` | ✓ canonical |
| `SavedView` | 2 | `saved-view.rst` | ✓ canonical |
| `BaseReportService` | 2 | `base-report-service.rst` | ✓ canonical |
| `Bucket` | 2 | `bucket.rst` | ✓ canonical |
| `AlertRule`, `Alert`, `Subscription`, `AuditValidator`, `Metric`, `InfrastructureLog`, `SystemHealth`, `TechnicalMetric`, `AccessGroup`, `AgentReportService`, `TransferReportService`, `IvrNavigationReportService`, `CallerReportService` | 1 c/u | (canonical match) | ✓ canonical |
| `AuditRepo (FTS)` | 1 | `audit-repo.rst` | ⚠ variante con (FTS) — limpiar |
| `Trunk SIP` | 1 | (no en domain-model) | ⚠ infraestructura |
| `Cron expiracion` | 1 | (no en domain-model) | ⚠ proceso/job |
| `Caller UC\n(UC_RPT_01..17)` | 1 | (placeholder textual) | ⚠ no es entidad |
| `Sistema (consumidores)` | 1 | (placeholder) | ⚠ no es entidad |

### 3.4 Clasificación de los 48 sistemas

| Categoría | Count | Acción para uml-07 standalone |
|---|---|---|
| **Canonical match exacto** | 41 | Usar nombre tal cual + `:doc:` en seealso |
| **Variantes con paréntesis** | 1 (`AuditRepo (FTS)`) | Normalizar a `AuditRepo`; nota explicativa en label |
| **Placeholders genéricos** | 4 (`Sistema`, `Sistema (consumidores)`, `User destino`, `Caller UC...`) | Eliminar — reemplazar por actores específicos |
| **Infraestructura externa** | 2 (`Trunk SIP`, `Cron expiracion`) | Marcar como `<<infraestructura>>` o `<<sistema_externo>>` (decisión Phase 7); NO requieren archivo en domain-model si son fronteras del sistema |

### 3.5 Cross-refs `:doc:` a domain-model

- **Total**: 57 entidades referenciadas, **todas existen** en `domain-model/`. ✓
- **Cobertura**: 57 / 67 = **85% del domain-model** ya está referenciado por al menos
  un UC de los 53 nuevos del predecesor.
- **No referenciadas** (10 entidades): `abandonment-report-service`, `index`, `nav-domain`,
  `menu`, `report` (clase abstracta), `historical-report`, `scheduled-report`,
  `scheduled-report-list-service`, `scheduled-report-repo`, `overview`. Algunas son
  legítimamente no usadas por UCs activos (e.g. `historical-report` heredado de specs
  pasadas).

## 4. Conclusión sobre domain-model gap

**Hipótesis original (heredada Q3 del predecesor):** "~18 clases faltantes en domain-model
referenciadas por UCs."

**Realidad observada:** Los 48 sistemas usados como actor `<<sistema>>` en los 83 uml-06
existentes **TODOS tienen archivo canónico en domain-model**, salvo:

1. 4 placeholders genéricos (no son entidades, son artefactos de redacción).
2. 2 entidades de infraestructura externa (`Trunk SIP`, `Cron expiracion`) que son
   **fronteras del sistema**, no parte del domain interno.

**Implicación para el WP:**

- ❌ El scope de "crear ~18 clases nuevas" **NO se confirma** desde la extracción de uml-06.
- ✅ El scope de "completar métodos faltantes" sigue siendo válido pero requiere análisis
  adicional sobre `flujo-principal.rst` + `implementacion-tecnica.rst` (no sobre los
  diagrams uml-06).

**Acción:** redirigir el scope de domain-model completion a:

1. **No crear clases nuevas** salvo que aparezcan referenciadas en specs textuales con
   métodos canónicos no presentes en domain-model.
2. **Sí auditar métodos** declarados en `flujo-principal.rst` / `implementacion-tecnica.rst`
   y faltantes en domain-model. Documento dedicado: `analyze/domain-model-completion-analysis.md`.
3. **Sí limpiar placeholders y variantes** en los uml-07 standalone:
   - `Sistema` genérico → reemplazar por entidad específica.
   - `User destino` → marcar con `<<beneficiario>>` sin función o con función específica.
   - `AuditRepo (FTS)` → `AuditRepo` con nota.
   - `Trunk SIP`, `Cron expiracion` → considerar `<<sistema_externo>>` (decisión SP-02).

## 5. Vocabulario de actores adoptado para uml-07 standalone

### 5.1 Funciones RBAC iniciadoras (sin stereotype)

Una función específica por UC. Ejemplos canónicos:

```
actor "view_audit_log" as INVOKER             ← UC_AUD_01..04 (audit module)
actor "search_audit_log" as INVOKER           ← UC_AUD_02
actor "export_audit_log" as INVOKER           ← UC_AUD_03
actor "generate_compliance_report" as INVOKER ← UC_AUD_04
actor "view_reports" as INVOKER               ← UC_RPT_01..09, 12-17
actor "manage_own_views" as INVOKER           ← UC_RPT_10
actor "share_reports" as INVOKER              ← UC_RPT_11
actor "view_alerts" as INVOKER                ← UC_ALR_02
actor "configure_team_alerts" as INVOKER      ← UC_ALR_01
actor "acknowledge_alert" as INVOKER          ← UC_ALR_03
actor "view_alert_history" as INVOKER         ← UC_ALR_04
actor "manage_own_subscriptions" as F_OWN     ← UC_ALR_05 (multi-invoker)
actor "subscribe_to_alert" as F_ADMIN         ← UC_ALR_05 (multi-invoker)
... (~70 funciones más, una por UC)
```

### 5.2 Funciones RBAC beneficiarias (`<<beneficiario>>`)

Función que recibe del UC sin iniciar:

```
actor "view_audit_log" as view_audit_log <<beneficiario>>
```

Aparece en 37 UCs (todo UC que emite AuditEvent → `view_audit_log` consume el log).

### 5.3 Sistemas (`<<sistema>>`) — nombre canónico domain-model

Tabla de mapping (uml-06 actor label → domain-model file):

| Actor label | Domain-model file | Aliases comunes |
|---|---|---|
| `AuditService` | `audit-service` | AS |
| `AuditQueryService` | `audit-query-service` | AQS |
| `AuditRepo` | `audit-repo` | AR |
| `AuditValidator` | `audit-validator` | AV |
| `Call` | `call` | CALL |
| `Session` | `session` | SESSION |
| `User` | `user` | (en seealso) |
| `Assignment` | `assignment` | A |
| `AssignmentRepo` | `assignment-repo` | AR |
| `Function` | `function` | F |
| `FunctionGroup` | `function-group` | FG |
| `AccessGroup` | `access-group` | AG |
| `AccessGroupFunction` | `access-group-function` | AGF |
| `RbacRepo` | `rbac-repo` | (referenciada) |
| `SeparationRule` | `separation-rule` | SR |
| `RuleValidator` | `rule-validator` | RV |
| `EvaluatorReloader` | `evaluator-reloader` | EE / ER |
| `PermissionService` | `permission-service` | PS |
| `PermissionCache` | `permission-cache` | PC |
| `ExceptionalPermission` | `exceptional-permission` | EP |
| `ExceptionalPermissionRepo` | `exceptional-permission-repo` | (referenciada) |
| `AlertRule` | `alert-rule` | AR |
| `Alert` | `alert` | A |
| `AlertRepo` | `alert-repo` | AR |
| `AlertHook` | `alert-hook` | AH |
| `Threshold` | `threshold` | (referenciada) |
| `Subscription` | `subscription` | S |
| `Campaign` | `campaign` | CAMP |
| `Action` | `action` | A |
| `AgentDailyStatRepo` | `agent-daily-stat-repo` | REPO |
| `AgentReportService` | `agent-report-service` | SVC |
| `BaseReportService` | `base-report-service` | SVC |
| `TransferReportService` | `transfer-report-service` | SVC |
| `IvrNavigationReportService` | `ivr-navigation-report-service` | SVC |
| `CallerReportService` | `caller-report-service` | SVC |
| `KpiCalculator` | `kpi-calculator` | KPI |
| `Bucket` | `bucket` | BK |
| `SegmentResolver` | `segment-resolver` | SR |
| `SavedView` | `saved-view` | SV |
| `SavedFilter` | `saved-filter` | SF |
| `FilterValidator` | `filter-validator` | FV |
| `ColumnCatalog` | `column-catalog` | CC |
| `Comparative` | `comparative` | (referenciada) |
| `CursorEncoder` | `cursor-encoder` | CE |
| `Sanitizer` | `sanitizer` | SAN |
| `PIIScanner` | `pii-scanner` | PII |
| `TimingCalculator` | `timing-calculator` | TC |
| `ApplicationLog` | `application-log` | LOG |
| `InfrastructureLog` | `infrastructure-log` | LOG |
| `PipelineLog` | `pipeline-log` | PL |
| `PipelineExecution` | `pipeline-execution` | PE |
| `Metric` | `metric` | M |
| `TechnicalMetric` | `technical-metric` | TM |
| `SystemHealth` | `system-health` | SH |
| `InternalMailbox` | `internal-mailbox` | MB |
| `ExportWorker` | `export-worker` | WORKER |
| `ExportJob` | `export-job` | JOB |

### 5.4 Sistemas externos (`<<sistema_externo>>` — propuesta)

Entidades fuera del dominio del IACT que aparecen como fronteras:

| Actor label | Naturaleza | Propuesta |
|---|---|---|
| `Trunk SIP` | Carrier SIP de telefonía | `<<sistema_externo>>` o `<<infraestructura>>` |
| `Cron expiracion` | Job scheduler | `<<sistema_externo>>` o `<<scheduler>>` |

**Decisión SP-02 PILOT:** definir el stereotype final tras validar 5 sample UCs.

### 5.5 Caller (`<<externo>>`)

Único actor externo no autenticado:

```
actor "Caller (cliente externo)" as CALLER <<externo>>
```

Aparece en UC_CLI_01..05 y como actor secundario en UC_OPR_02..05, UC_SUP_01..02.

## 6. Anti-patrones a evitar (heredados de uml-06)

Reglas para los 83 uml-07 standalone:

1. ❌ **No usar `Sistema` genérico** como actor. Reemplazar por entidad específica.
2. ❌ **No usar `User destino` sin función** específica si es función RBAC. Si es
   cualquier User receptor, usar `<<beneficiario>>` con label `User destino`.
3. ❌ **No usar variantes con paréntesis** (`AuditRepo (FTS)`). Usar nombre canónico
   y agregar nota si necesario.
4. ❌ **No usar `<\|--` entre actores** (BR-006).
5. ❌ **No usar SP/SQL/codenames como UC** (R-12 uml-07).
6. ❌ **No usar roles agregados** (`Operator`, `Supervisor`, `AccessAdmin`) como
   actores RBAC. La única excepción es `Caller` (rol externo, no autenticado).

## 7. Output

- `uc-vocabulary-extraction.json` — extracción machine-readable.
- Este documento — análisis y vocabulario adoptado.

## 8. Próximo análisis (Phase 3, segundo doc)

`analyze/domain-model-completion-analysis.md` — auditoría de **métodos** faltantes en
clases existentes del domain-model, leyendo `flujo-principal.rst` e
`implementacion-tecnica.rst` de los 83 UCs.
