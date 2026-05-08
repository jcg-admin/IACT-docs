```yml
created_at: 2026-05-06 05:35:00
project: IACT-docs
work_package: 2026-05-06-05-28-57-design-view-buildout
phase: Phase 6 — PLAN
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Phase 6 PLAN — Design View Buildout

## Scope statement

**In-scope:**

1. 1 archivo `package-overview.rst` — vista global de paquetes/modulos.
2. 13 archivos `class-{mod}.rst` — uno por modulo (access, admin, alerts, audit, auth, caller, logs, operator, permissions, pipeline, reports, supervision, users).
3. 14 archivos `seq-{mod}.rst` — armonizacion de los existentes al vocabulario canonico (incluye `seq-users.rst` que existe).
4. 6 archivos `act-{flujo}.rst`:
   - `act-rbac-effective-set-eval.rst`
   - `act-etl-pipeline-execution.rst`
   - `act-alert-evaluation.rst`
   - `act-sod-check.rst`
   - `act-jwt-auth.rst`
   - `act-export-async.rst`
5. 6 archivos `state-{entidad}.rst`:
   - `state-call.rst`
   - `state-alert-event.rst`
   - `state-pipeline-execution.rst`
   - `state-session.rst`
   - `state-assignment.rst`
   - `state-export-job.rst`
6. Update `index.rst` con nuevos toctrees por seccion.
7. Audit script `scripts/validate-design-view.sh`.
8. Build strict `-W` 0 warnings.

**Total:** 40 archivos + 1 script + 1 index update.

**Out-of-scope:**

- Diagramas de componentes (uml-12) → ImplementationView.
- Diagramas de distribucion (uml-13) → DeployView.
- Cualquier modificacion a `domain-model/` o `use-case-view/` (esos WPs estan cerrados).
- Codigo Python real, tests, deployment configs.

## Roadmap por batches

| Batch | Contenido | Cantidad | SP gate |
|---|---|---|---|
| B-01 | `package-overview.rst` | 1 | Build incremental OK |
| B-02 | 13 `class-{mod}.rst` | 13 | Build incremental OK + audit C-02 |
| B-03 | Update 14 `seq-{mod}.rst` | 14 | Diff revisable, build OK |
| B-04 | 6 `act-{flujo}.rst` | 6 | Build OK |
| B-05 | 6 `state-{entidad}.rst` | 6 | Build OK |
| B-06 | `index.rst` toctree update + audit script | 2 | Audit run clean |
| B-07 | Prerender PlantUML + strict build final | 1 cmd | EXIT=0, 0 warnings, 0 misses nuevos |

Total: 7 batches → 1 commit por batch (excepto B-02..B-05 que pueden ser multi-commit por modulo).

## Aprobaciones

- ✓ Pre-aprobado por usuario en chat para "ejecutar TODO en loop".
- ✓ SP-01 implicito (analysis aprobado vía respuesta usuario).
- ✓ SP-02 implicito (strategy aprobada vía respuesta usuario).
- Pendiente: SP-04 gate tecnico tras B-02 (antes de B-03).
