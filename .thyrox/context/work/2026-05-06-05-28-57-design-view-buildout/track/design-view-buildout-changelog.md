```yml
created_at: 2026-05-06 06:35:00
project: IACT-docs
work_package: 2026-05-06-05-28-57-design-view-buildout
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — Design View Buildout

## Resumen

| Metrica | Valor |
|---|---|
| Files creados/actualizados | 32 (1 overview + 10 class + 10 seq + 6 act + 5 state) |
| UCs in-scope cubiertos | 65 (out: opr, sup, cli per decision del ejecutor) |
| Audit `validate-design-view.sh` | PASSED 32 archivos, 65 actores `<<sistema>>`, 0 violaciones C-01..C-06 |
| Build strict final | EXIT=0, 0 warnings, 3 misses known false-positives |
| Cache PlantUML | 1197 SVGs, 0 con Syntax Error, 0 con Cannot find Graphviz |

## Added

### Package overview (1)

- `package-overview.rst` — vista global de 10 modulos in-scope
  con dependencias, capas conceptuales y orden de lectura.
  Documenta explicitamente que MOD_Operator, MOD_Supervision
  y MOD_Caller estan out-of-scope per decision del ejecutor.

### Class diagrams (10)

- class-auth, class-users, class-access, class-permissions,
  class-admin, class-audit, class-pipeline, class-reports,
  class-alerts, class-logs.

NO duplican domain-model — solo agrupan + relaciones internas.

### Activity diagrams (6 cross-modulo)

- act-rbac-effective-set-eval (verify pipeline).
- act-jwt-auth (login + refresh + blacklist).
- act-sod-check (CNST-005 pre-mutacion RBAC).
- act-etl-pipeline-execution.
- act-alert-evaluation.
- act-export-async.

### State diagrams (5 entidades con ciclo)

- state-session, state-assignment,
  state-pipeline-execution, state-alert-event,
  state-export-job.

### Audit script

- `scripts/validate-design-view.sh` con C-01..C-06.

## Changed

- `design-view/index.rst` v3.1.0: reorganizado por tipo de
  diagrama UML, removido caller/operator/supervision toctree
  entries.
- `design-view/seq-{access,admin,permissions,auth,users,audit,
  pipeline,reports,alerts,logs}.rst` v2.0.0: armonizados al
  vocabulario canonico del domain-model (reemplaza
  ServicioAcceso, ServicioRBAC, RepositorioAssignment, etc.).

## Removed

7 archivos out-of-scope por decision del ejecutor:

- class-operator.rst, class-supervision.rst, class-caller.rst.
- seq-operator.rst, seq-supervision.rst, seq-caller.rst.
- state-call.rst (Call FSM solo aplica a operator/caller).

## Fixed

- seq-supervision.rst: `note bottom of` -> `note over`
  (PlantUML sequence diagrams no soportan `note bottom of`).
- class-reports.rst: cross-ref roto
  `domain-model/agent-daily-stat` -> `agent-daily-stat-repo`.
- 165 SVGs con error "Cannot find Graphviz" eliminados +
  regenerados tras instalar graphviz (cause: PlantUML default
  busca /opt/local/bin/dot, no /usr/bin/dot).

## Aceptado / no fixeado

### 3 cache misses residuales en build

Identicos a los del WP plantuml-cache-prerender-update:

- base-cognitiva/_uml/uml-12-diagramas-componentes/una-pagina-web-con-un-applet-java
- base-cognitiva/plantuml-guide/ejemplos/test-component-diagram
- base-cognitiva/plantuml-guide/ejemplos/test-uc-diagram

Hipotesis: hash discrepancy entre prerender y runtime. WP futuro
para investigacion.

### MOD_Operator/Supervision/Caller out-of-scope

Decision del ejecutor durante el WP. Documentado en
package-overview.rst con nota inline. Si futuros WPs deciden
implementar, su DesignView se construira como WP separado
consumiendo este package-overview como base.

## Verified

- `validate-design-view.sh`: 32 PASS, 0 FAIL, 0 violaciones.
- `validate-naming-corpus.sh` (creado en WP paralelo): los
  archivos del design-view NO contribuyen violaciones (todos
  los identifiers en ingles).
- Build strict EXIT=0, 0 warnings post-fix de 33 titulos
  overline, post-deletion de 7 archivos out-of-scope, post-fix
  de cross-ref roto, post-regeneration de SVGs.

## Status de promocion a CHANGELOG.md raiz

Aplica al merge a main. DesignView completo es entrega
sustantiva al corpus arquitectonico.

## WPs sucesores derivados

1. (low) `design-view-cache-runtime-hash-debug` — investigar
   las 3 hash discrepancies residuales.
2. (medium, condicional) `design-view-buildout-operator-sup-caller`
   — si/cuando se decida implementar esos modulos.

## Refs

- Predecesores: `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass`
  (UseCaseView), `2026-05-05-21-56-47-functional-decomposition-
  antipattern-audit` (audit Brown 1998), `2026-05-06-01-29-18-
  plantuml-cache-corruption-remediation` (cache regenerado).
- WPs paralelos: `2026-05-06-06-24-49-naming-violations-
  arquitectura-tecnica-fix` (cerrado), `2026-05-06-06-32-20-
  spanish-class-names-corpus-audit` (en curso).
- Build log final: `execute/build-logs/sphinx-strict-fully-
  clean-2026-05-06T06-19-50.log`.
- Audit log: corrida desde linea de comandos.
- Reglas operacionales seguidas: `.claude/rules/long-running-
  commands.md` R-1, R-2, R-2.1, R-2.2.
