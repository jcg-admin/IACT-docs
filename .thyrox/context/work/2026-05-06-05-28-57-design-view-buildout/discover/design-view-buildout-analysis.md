```yml
created_at: 2026-05-06 05:30:00
project: IACT-docs
work_package: 2026-05-06-05-28-57-design-view-buildout
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Phase 1 DISCOVER — Design View Buildout

## 1. Objetivo / Por que

Construir la **Vista Logica (Kruchten 4+1) / Functional + Information (Rozanski)** del sistema IACT, materializando los UCs ya documentados en una representacion de diseno: paquetes, interacciones, flujos y ciclos de vida. Es el siguiente eslabon obligatorio per la jerarquia de dependencias arquitectonicas (DesignView desbloquea Implementation/Process/Deploy).

## 2. Stakeholders

| Stakeholder | Necesidad |
|---|---|
| Arquitectos tecnicos | Vista de diseno coherente como fuente de truth para decisiones |
| Devs backend/frontend | Identificar que clases del domain-model usar y como interactuan |
| Auditores | Trazabilidad UC → diseno → implementacion |
| Futuros WPs (ImpView, ProcView, DepView) | DesignView como insumo de entrada |

## 3. Uso operacional

Los diagramas se renderizan en HTML via Sphinx + sphinxcontrib.plantuml. Los devs los consultan al implementar features. Sirven como contrato visual entre arquitectura y codigo.

## 4. Atributos de calidad

| Atributo | Como se garantiza |
|---|---|
| Fidelidad al domain-model | Audit script: TODO actor `<<sistema>>` debe existir en `domain-model/*.rst` |
| Conformidad OOP (no FD) | Vocabulario heredado del audit Brown 1998 ✓ clean |
| Consistencia naming | Solo nombres canonicos del domain-model — sin localizar (no `ServicioX`) |
| Cohesion modular | Class diagram per modulo agrupa solo clases de ese bounded context |
| Trazabilidad UC | Cada seq-/act-/state- referencia los UCs que cubre |
| Build clean | `sphinx-build -W` post cada batch |

## 5. Restricciones

- **Sin scripts** de generacion masiva (manual UC-by-UC).
- **Solo nombres canonicos** del domain-model.
- **Naming** auto-explicativo: `{tipo}-{slug-descriptivo}.rst` (no IDs numericos).
- **Branch:** `feature/cnst-033-uml-conformance`.
- **Build logs** ISO 8601 en `execute/build-logs/`.
- **Reglas R-1..R-2.2** de `.claude/rules/long-running-commands.md`.
- **Tim Pope commits** (per `.claude/rules/commit-conventions.md`).

## 6. Contexto / sistemas vecinos

```
DomainModel ✓ (85 clases, audit Brown 1998 clean)
    ↑
UseCaseView ✓ (99 archivos uml-07 standalone)
    ↑
DesignView ← ESTE WP (40 archivos: 1 overview + 13 class + 14 seq + 6 act + 6 state)
    ↓
ImplementationView (bloqueada hasta cierre)
ProcessView (bloqueada hasta cierre + DeployView)
DeployView (bloqueada hasta cierre + ImplementationView)
```

## 7. Fuera de alcance

- **NO** redibujar clases del domain-model (delegado via `:doc:`).
- **NO** componentes/distribucion (uml-12, uml-13 → ImplementationView, DeployView).
- **NO** codigo Python/SQL real.
- **NO** tests (out of scope del corpus de docs).

## 8. Criterios de exito

1. `source/arquitectura-tecnica/design-view/` con 40 archivos:
   - 1 `package-overview.rst`
   - 13 `class-{mod}.rst`
   - 14 `seq-{mod}.rst` (update de existentes)
   - 6 `act-{flujo}.rst`
   - 6 `state-{entidad}.rst`
2. `index.rst` actualizado con todos los toctree.
3. Build strict `-W`: 0 warnings.
4. Audit script `validate-design-view.sh` (analogo al uml-07): 0 violaciones.
5. Coverage analysis pre-cierre: cada UC mapeado a algun seq/act que lo cubre.

## Fase 3 ANALYZE — embebido aqui (WP mediano)

### 3.1 Inventario de modulos

```
13 modulos (alineados con use-case-view/):
access · admin · alerts · audit · auth · caller · logs ·
operator · permissions · pipeline · reports · supervision · users
```

### 3.2 Inventario de orchestrators del domain-model (candidatos para clases en class-{mod})

| Categoria | Ejemplos | Cantidad aprox |
|---|---|---|
| Repositories | `user-repo`, `function-repo`, `function-group-repo`, `assignment-repo`, `audit-repo`, `alert-repo`, `assignment-repo`, `pipeline-execution-repo`, `scheduled-report-repo`, `exceptional-permission-repo`, `access-group-repo`, `agent-daily-stat-repo`, `rbac-repo`, `separation-rule-repo` | ~14 |
| Services | `permission-service`, `audit-service`, `audit-query-service`, `agent-report-service`, `caller-report-service`, `abandonment-report-service`, `ivr-navigation-report-service`, `scheduled-report-list-service`, `base-report-service`, `transfer-report-service` | ~10 |
| Guards / Policies | `authorization-guard`, `idempotency-policy`, `expiration-policy` | ~3 |
| Utilities / Aggregators | `effective-permissions-aggregator`, `kpi-calculator`, `password-generator`, `metrics-cache`, `permission-cache`, `segment-resolver`, `cursor-encoder`, `evaluator-reloader` | ~8 |

### 3.3 Mapeo modulo → orchestrators principales

| Modulo | Orchestrators clave del domain-model |
|---|---|
| access | `assignment-repo`, `separation-rule-repo`, `authorization-guard`, `audit-service` |
| admin | `function-repo`, `function-group-repo`, `separation-rule-repo`, `audit-service` |
| alerts | `alert-repo`, `alert-rule`, `evaluator-reloader`, `audit-service` |
| audit | `audit-repo`, `audit-query-service`, `audit-service`, `audit-validator` |
| auth | `authorization-guard`, `blacklisted-token`, `idempotency-policy`, `expiration-policy`, `password-generator` |
| caller | `caller-report-service`, `permission-service`, `audit-service` |
| logs | `application-log`, `infrastructure-log`, `audit-query-service` |
| operator | `internal-mailbox`, `internal-message`, `permission-service`, `audit-service` |
| permissions | `permission-service`, `permission-cache`, `effective-permissions-aggregator`, `exceptional-permission-repo`, `authorization-guard` |
| pipeline | `pipeline-execution-repo`, `metrics-cache`, `audit-service` |
| reports | `agent-report-service`, `caller-report-service`, `abandonment-report-service`, `ivr-navigation-report-service`, `scheduled-report-list-service`, `kpi-calculator`, `export-worker`, `export-job` |
| supervision | `internal-mailbox`, `internal-message`, `segment-resolver`, `audit-service` |
| users | `user-repo`, `password-generator`, `audit-service` |

### 3.4 Flujos cross-modulo candidatos para `act-` (Phase 10D)

1. **`act-rbac-effective-set-eval.rst`** — flujo de calculo del effective_set (intersecta permissions + access + auth)
2. **`act-etl-pipeline-execution.rst`** — flujo ETL (pipeline + audit)
3. **`act-alert-evaluation.rst`** — flujo de evaluacion de alertas (alerts + metrics)
4. **`act-sod-check.rst`** — flujo Separation of Duties (access + admin)
5. **`act-jwt-auth.rst`** — flujo JWT auth + refresh + blacklist (auth)
6. **`act-export-async.rst`** — flujo exportacion asincrona de reportes (reports + audit)

### 3.5 Entidades con ciclo de vida candidatas para `state-` (Phase 10E)

1. **`state-call.rst`** — Call FSM (~10 estados: queued/ringing/answered/onHold/.../wrap/closed)
2. **`state-alert-event.rst`** — AlertEvent (raised/acknowledged/resolved/silenced)
3. **`state-pipeline-execution.rst`** — PipelineExecution (running/completed/failed/cancelled)
4. **`state-session.rst`** — Session (active/expired/revoked/blacklisted)
5. **`state-assignment.rst`** — Assignment (active/expired/revoked)
6. **`state-export-job.rst`** — ExportJob (pending/processing/ready/failed/expired)

### 3.6 Inconsistencia confirmada en `seq-*.rst` actuales

Los 14 `seq-{mod}.rst` usan vocabulario localizado:

```
participant InterfazAdmin        <<frontend>>
participant ServicioAcceso       <<api>>
participant ServicioRBAC         <<domain>>
participant RepositorioAssignment <<repository>>
database    AlmacenDatos         <<postgresql>>
```

Vocabulario canonico requerido (post-audit Brown 1998):

```
actor "create_separation_rule" as create_separation_rule
actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
actor "AssignmentRepo" as AssignmentRepo <<sistema>>
actor "AuditService" as AuditService <<sistema>>
```

## Stopping Point Manifest

| ID | Fase | Tipo | Evento | Accion |
|---|---|---|---|---|
| SP-01 | 1→3 | gate-fase | analysis aprobado | Avanzar Phase 3 (embebido) → Phase 5 |
| SP-02 | 5→6 | gate-fase | strategy aprobada | Avanzar Phase 6 PLAN |
| SP-03 | 8→10 | gate-fase | task-plan validado | Avanzar Phase 10 EXECUTE |
| SP-04 | 10 batch | gate-tecnico | build clean tras cada batch (modulo) | Continuar siguiente batch |
| SP-05 | 10→11 | gate-tecnico | build final clean + audit clean | Avanzar Phase 11 TRACK |
| SP-06 | 11→cierre | gate-humano | lessons + changelog aprobados | Cerrar WP |
