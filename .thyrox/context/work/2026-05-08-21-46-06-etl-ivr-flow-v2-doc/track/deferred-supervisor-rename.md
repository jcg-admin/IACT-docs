```yml
created_at: 2026-05-08 22:30:00
project: IACT-docs
work_package: 2026-05-08-21-46-06-etl-ivr-flow-v2-doc
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Deferral — Rename global de actor `Supervisor` → `QualitySupervisor`

## Contexto

El corpus contiene **dos conceptos distintos bajo el mismo
nombre `Supervisor`**:

| Concepto | AGR | Funciones | Dominio | Scope |
|---|---|---|---|---|
| `Supervisor` de agentes | AGR-003 `quality_supervisor_group` + AGR-012 `call_center_supervisor_group` | `monitor_live_calls`, `barge_in_calls`, `broadcast_team_messages` | Call center — supervisa agentes en tiempo real | Fuera de scope (`MOD_Supervision`) |
| `Supervisor de Operaciones` | AGR-009 `pipeline_admin_group` | `pipeline.view_status`, `etl.retry`, `view_pipeline_errors` | IT/ops — monitorea ETL de datos IVR | **In scope** — UC_PIP_01..04 |

## Decision tomada en este WP — Alternativa 2

Reemplazar `Supervisor de Operaciones` por `PipelineAdmin` en
los specs y narrativa relacionada con UC_PIP_01..04. Esto
elimina la ambiguedad **inmediata** sin costo de rename
global.

### Archivos modificados (5)

- `source/requisitos/casos-uso/pipeline/uc-pip-01/actores-precondiciones.rst`
- `source/requisitos/casos-uso/pipeline/uc-pip-01/flujo-principal.rst`
- `source/requisitos/casos-uso/pipeline/uc-pip-02/actores-precondiciones.rst`
- `source/requisitos/casos-uso/pipeline/uc-pip-02/flujo-principal.rst`
- `source/arquitectura-tecnica/context-view/stakeholders.rst`
- `source/arquitectura-tecnica/pipeline-etl-iact/etl-procedures.rst`
- `source/arquitectura-tecnica/pipeline-etl-iact/index.rst` —
  agregada seccion **Actores y scope funcional** + warning
  explicito.

UC_PIP_03 ya usaba `Analista de Datos` (no afectado).
UC_PIP_04 y `use-case-view/pipeline/` ya usaban `PipelineAdmin`
(no afectados).

## Trabajo deferido — Alternativa 1

**Cuando:** WP futuro, condicionado a la activacion de
`MOD_Supervision` o `MOD_Operator`.

**Que:** Rename global del actor `Supervisor` a
`QualitySupervisor` (o `CallCenterSupervisor`) en todo el
corpus, manteniendo `PipelineAdmin` como rol IT/ops.

**Costo estimado:** ~30-40 archivos en
`use-case-view/`, `casos-uso/`, diagramas PlantUML y
`panorama-iact.rst`. Requiere sed escopado + actualizacion
de cross-refs.

**Trigger:** activacion de cualquiera de
- `MOD_Supervision` (UC_SUP_01..03)
- `MOD_Operator` (UC_OPR_01..10)
- WP de auditoria de nomenclatura del catalogo RBAC.

**Por que no se hizo ahora:** los modulos cuyo unico rol que
sufre la ambiguedad estan **fuera de scope** del proyecto
IACT. Renombrar un actor de modulos out-of-scope es trabajo
prematuro — el coste de ~40 archivos no se justifica antes
de tener consumidores activos de `MOD_Supervision`.

## Resumen

- **Alternativa 1** (rename global): correcta pero prematura.
- **Alternativa 2** (colapsar en `PipelineAdmin`):
  pragmatica, aplicada.
- **Alternativa 3** (solo glosario): rechazada, no resuelve
  el problema de raiz.

## Refs

- Fix aplicado en commit del WP `etl-ivr-flow-v2-doc`.
- Catalogo RBAC con definicion de los actores:
  `source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst`.
- UCs in-scope: `UC_PIP_01..04`.
- UCs out-of-scope: `UC_SUP_01..03`, `UC_OPR_01..10`.
