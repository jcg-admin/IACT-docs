```yml
created_at: 2026-05-07 19:45:26
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-008 Executable Task Plan
```

# T-008 — Task plan ejecutable: UML diagrams deep audit

> 116 tareas atomicas T-NNN. Cada tarea es 1 commit Tim Pope.
> Build incremental obligatorio tras cada tarea con cambios.

## Resumen

- **20 T-CLASS** — crear stubs de clase nueva en domain-model.
- **39 T-COMPLEMENT** — anadir ejes faltantes a archivos clase B.
- **53 T-VERIFY** — verificacion semantica vs flujo-principal de archivos clase A.
- **4 TR** — TRACK (build clean + cierre WP).

## Bloque 1: T-CLASS (20 tareas)

Cada tarea: crear archivo en `source/arquitectura-tecnica/domain-model/`
siguiendo la plantilla de T-005 §4. Build incremental + commit.

### Lote 1: clases base (sin dependencias internas)

- [ ] **T-CL-01** — Crear `alert-rule-repo.rst` (`AlertRuleRepo`, consumida por uc-alr-01).
- [ ] **T-CL-02** — Crear `campaign-daily-stat-repo.rst` (`CampaignDailyStatRepo`, consumida por uc-rpt-14).
- [ ] **T-CL-03** — Crear `function-group-membership.rst` (`FunctionGroupMembership`, consumida por uc-acc-04).
- [ ] **T-CL-04** — Crear `hmac-verifier.rst` (`HmacVerifier`, consumida por uc-aud-04).
- [ ] **T-CL-05** — Crear `impact-report.rst` (`ImpactReport`, consumida por uc-adm-03).
- [ ] **T-CL-06** — Crear `segment-scope.rst` (`SegmentScope`, consumida por uc-inc-rpt-01).
- [ ] **T-CL-07** — Crear `subscription-repo.rst` (`SubscriptionRepo`, consumida por uc-alr-05).
- [ ] **T-CL-08** — Crear `user-access-group-assignment.rst` (`UserAccessGroupAssignment`, consumida por uc-acc-04).
- [ ] **T-CL-09** — Crear `alert-history-summary.rst` (`AlertHistorySummary`, consumida por uc-alr-04).
- [ ] **T-CL-10** — Crear `disparador-etl.rst` (`DisparadorETL`, consumida por uc-pip-04).

### Lote 2: servicios con dependencias

- [ ] **T-CL-11** — Crear `alert-history-service.rst` (`AlertHistoryService`, consumida por uc-alr-04).
- [ ] **T-CL-12** — Crear `campaign-report-service.rst` (`CampaignReportService`, consumida por uc-rpt-14).
- [ ] **T-CL-13** — Crear `general-audit-service.rst` (`GeneralAuditService`, consumida por uc-aud-01).
- [ ] **T-CL-14** — Crear `errores-etl-service.rst` (`ErroresETLService`, consumida por uc-pip-02).
- [ ] **T-CL-15** — Crear `resumen-salud.rst` (`ResumenSalud`, consumida por uc-pip-01).
- [ ] **T-CL-16** — Crear `resumen-salud-builder.rst` (`ResumenSaludBuilder`, consumida por uc-pip-01).
- [ ] **T-CL-17** — Crear `segment-change-listener.rst` (`SegmentChangeListener`, consumida por uc-alr-05).
- [ ] **T-CL-18** — Crear `infra-log-store.rst` (`InfraLogStore`, consumida por uc-log-05).
- [ ] **T-CL-19** — Crear `log-store.rst` (`LogStore`, consumida por uc-log-01).
- [ ] **T-CL-20** — Crear `supervision-etl-service.rst` (`SupervisionETLService`, consumida por uc-pip-01).

**Gate al cierre del bloque:** los 20 archivos existen,
build incremental EXIT=0, todas las clases referenciadas en
clases-de-clases.rst de los 92 archivos resuelven a un
archivo existente.

## Bloque 2: T-COMPLEMENT (39 tareas)

Cada tarea sigue el protocolo:

1. Leer el archivo actual y el `flujo-principal.rst` del UC.
2. Identificar ejes UML-07 faltantes (de la matriz T-004 §4).
3. Aplicar el patron correspondiente de T-006.
4. Verificar cross-refs `:doc:` con `ls` antes de guardar.
5. Build incremental `sphinx-build -W -j 1`.
6. Commit Tim Pope: `Complement diagrama-de-X for uc-Y`.


### Cluster `reports`

- [ ] **T-CO-01** — `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-02** — `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso-relacion-de-inclusion.rst` (tipo: caso-de-uso-relacion, ejes faltantes: extension, generalizacion, comprension_dominio)
- [ ] **T-CO-03** — `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-actividad-crear.rst` (tipo: otro(actividad-crear), ejes faltantes: comprension_dominio)
- [ ] **T-CO-04** — `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-aplicar.rst` (tipo: otro(actividad-aplicar), ejes faltantes: comprension_dominio)
- [ ] **T-CO-05** — `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-compartir.rst` (tipo: otro(actividad-compartir), ejes faltantes: comprension_dominio)
- [ ] **T-CO-06** — `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-07** — `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-secuencia-detalle.rst` (tipo: otro(secuencia-detalle), ejes faltantes: comprension_dominio)
- [ ] **T-CO-08** — `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-09** — `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, ejes faltantes: comprension_dominio)
- [ ] **T-CO-10** — `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-11** — `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, ejes faltantes: comprension_dominio)
- [ ] **T-CO-12** — `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-13** — `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-14** — `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-distribucion-de-menus.rst` (tipo: otro(distribucion-de-menus), ejes faltantes: comprension_dominio)
- [ ] **T-CO-15** — `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-16** — `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-flujo-de-anonimizacion-etl.rst` (tipo: otro(flujo-de-anonimizacion-etl), ejes faltantes: comprension_dominio)

### Cluster `logs`

- [ ] **T-CO-17** — `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-18** — `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-19** — `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-secuencia-pipeline-log.rst` (tipo: otro(secuencia-pipeline-log), ejes faltantes: comprension_dominio)
- [ ] **T-CO-20** — `requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-21** — `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-22** — `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst` (tipo: otro(secuencia-exportacion-logs), ejes faltantes: comprension_dominio) — depende de T-CL: LogStore
- [ ] **T-CO-23** — `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-24** — `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst` (tipo: otro(secuencia-tail-sse), ejes faltantes: comprension_dominio) — depende de T-CL: InfraLogStore
- [ ] **T-CO-25** — `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-26** — `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-componentes.rst` (tipo: componentes, ejes faltantes: panorama)
- [ ] **T-CO-27** — `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)

### Cluster `pipeline`

- [ ] **T-CO-28** — `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-29** — `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-30** — `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-31** — `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-componentes.rst` (tipo: componentes, ejes faltantes: panorama)
- [ ] **T-CO-32** — `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-33** — `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, ejes faltantes: comprension_dominio) — depende de T-CL: DisparadorETL

### Cluster `audit`

- [ ] **T-CO-34** — `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-35** — `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, ejes faltantes: comprension_dominio)
- [ ] **T-CO-36** — `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-flujo-de-firma.rst` (tipo: otro(flujo-de-firma), ejes faltantes: comprension_dominio)
- [ ] **T-CO-37** — `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst` (tipo: otro(secuencia-verify), ejes faltantes: comprension_dominio) — depende de T-CL: HmacVerifier

### Cluster `permissions`

- [ ] **T-CO-38** — `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst` (tipo: estados, ejes faltantes: comprension_dominio)
- [ ] **T-CO-39** — `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst` (tipo: estados, ejes faltantes: comprension_dominio)

## Bloque 3: T-VERIFY (53 tareas, semantico)

Cada tarea sigue el protocolo:

1. Leer `flujo-principal.rst` del UC consumidor.
2. Leer el diagrama actual.
3. Verificar: el diagrama refleja **fielmente** el flujo principal?
4. Si si: marcar [x] sin cambio.
5. Si no: reclasificar a B y crear T-CO-extra (T-CO-EX-NN).


### Cluster `reports`

- [ ] **T-VE-01** — `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-02** — `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-03** — `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-estados-saved-view.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-04** — `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-estados-share.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-05** — `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-06** — `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-07** — `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-08** — `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-09** — `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-10** — `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).

### Cluster `logs`

- [ ] **T-VE-11** — `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-pipeline.rst` (tipo: otro(pipeline), score: 2/2).
- [ ] **T-VE-12** — `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-tail-sse.rst` (tipo: otro(tail-sse), score: 2/2).
- [ ] **T-VE-13** — `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-componentes-pipeline-log.rst` (tipo: otro(componentes-pipeline-log), score: 2/2).
- [ ] **T-VE-14** — `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-componentes-export.rst` (tipo: otro(componentes-export), score: 2/2).
- [ ] **T-VE-15** — `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-pipeline-infraestructura.rst` (tipo: otro(pipeline-infraestructura), score: 2/2).
- [ ] **T-VE-16** — `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-estados-overall.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-17** — `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-pipeline-metricas.rst` (tipo: otro(pipeline-metricas), score: 2/2).

### Cluster `pipeline`

- [ ] **T-VE-18** — `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-19** — `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-estados-ejecucion-etl.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-20** — `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-21** — `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-22** — `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-estados-frescura-datos.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-23** — `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-estados-reintento.rst` (tipo: estados, score: 2/2).

### Cluster `audit`

- [ ] **T-VE-24** — `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-25** — `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-26** — `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-27** — `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-componentes-fts.rst` (tipo: otro(componentes-fts), score: 2/2).
- [ ] **T-VE-28** — `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-29** — `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-30** — `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-estados-export-job.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-31** — `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).

### Cluster `access`

- [ ] **T-VE-32** — `requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst` (tipo: otro(agr-como-agregacion), score: 2/2).

### Cluster `admin`

- [ ] **T-VE-33** — `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-34** — `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-35** — `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-36** — `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-estados-funcion.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-37** — `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-38** — `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-impacto.rst` (tipo: otro(impacto), score: 2/2).

### Cluster `alerts`

- [ ] **T-VE-39** — `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-40** — `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-41** — `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-estados-regla.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-42** — `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-43** — `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-44** — `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-45** — `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-46** — `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-estados-transicion.rst` (tipo: estados, score: 2/2).
- [ ] **T-VE-47** — `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-48** — `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-49** — `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-50** — `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-secuencia.rst` (tipo: secuencia, score: 2/2).
- [ ] **T-VE-51** — `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-actividad.rst` (tipo: actividad, score: 2/2).
- [ ] **T-VE-52** — `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst` (tipo: clases, score: 2/2).
- [ ] **T-VE-53** — `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-estados-subscription.rst` (tipo: estados, score: 2/2).

## Bloque 4: TRACK (4 tareas)

- [ ] **TR-01** — Build clean serial deterministic.
  ```bash
  WP=.thyrox/context/work/2026-05-07-14-49-04-uml-diagrams-deep-audit
  ISO=$(date -u +%Y-%m-%dT%H-%M-%S)
  LOG="$WP/track/build-logs/sphinx-strict-final-$ISO.log"
  mkdir -p "$(dirname "$LOG")"
  make clean
  sphinx-build -W -j 1 -b html source build/html >"$LOG" 2>&1
  echo "EXIT=$?" >> "$LOG"
  ```
- [ ] **TR-02** — Verificar 0 warnings + 0 cross-refs rotos.
- [ ] **TR-03** — Crear `track/uml-deep-audit-changelog.md` (Keep a Changelog) +
  `track/lessons-learned.md` con learnings sobre proceso archivo-por-archivo.
- [ ] **TR-04** — Cerrar WP: `wp-state.md status=Cerrado` +
  post-mortem comparando profundidad vs WP previo.

## Convenciones de commit

| Bloque | Subject pattern |
|---|---|
| T-CL-NN | `Add {ClassName} domain-model stub` |
| T-CO-NN | `Complement diagrama-de-{tipo} for {uc-slug}` |
| T-VE-NN (sin cambio) | (no commit, solo marca [x] en este plan) |
| T-VE-NN (con fix) | `Fix diagrama-de-{tipo} for {uc-slug}` |
| TR-NN | `{Action} for uml-deep-audit WP` |

## Refs

- T-001 ... T-004: Phase 1 + 3 (audit).
- T-005: `strategy/new-classes-catalog.md`.
- T-006: `strategy/uml07-patterns-by-category.md`.
- T-007: `strategy/execution-order.md` (DAG).
