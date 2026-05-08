```yml
created_at: 2026-05-07 15:55:15
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-003 UML-07 Conformance Scoring
```

# T-003 — UML-07 conformance scoring (92 archivos)

> Heurísticas mecánicas aplicadas archivo-por-archivo,
> inspiradas en `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`.
> Cada eje aplica solo cuando es relevante al tipo del diagrama.

## 1. Criterios de evaluación

| Eje UML-07 | Heurística observable | Tipos aplicables |
|---|---|---|
| **Representación** | Tiene `actor`, `rectangle "<sistema>"`, `usecase`, flecha `-->` | caso-de-uso |
| **Inclusión** | Tiene `<<include>>` o `<<incluir>>` | caso-de-uso |
| **Extensión** | Tiene `<<extend>>` o `<<extender>>` | caso-de-uso |
| **Generalización** | Tiene `--\|>` o `<\|--` (herencia) | caso-de-uso |
| **Comprensión del dominio** | ≥1 cross-ref `:doc:` a domain-model | todos |
| **Profundización** | ≥1 diagrama hermano en el UC | todos |
| **Panorama** | ≥2 actores o ≥4 identificadores | caso-de-uso, componentes |

Clasificación final por % ejes aplicables aprobados:

- **A** (verify) ≥80% — solo verificar manual.
- **B** (complement) 40-79% — añadir lo que falta.
- **C** (recreate) <40% — recrear desde cero.

## 2. Distribución de clases

| Clase | Archivos |
|---|---|
| **A** | 53 |
| **B** | 39 |
| **C** | 0 |
| **Total** | 92 |

## 3. Distribución por cluster × clase

| Cluster | A | B | C | Total |
|---|---|---|---|---|
| access | 1 | 0 | 0 | 1 |
| admin | 6 | 0 | 0 | 6 |
| alerts | 15 | 0 | 0 | 15 |
| audit | 8 | 4 | 0 | 12 |
| logs | 7 | 11 | 0 | 18 |
| permissions | 0 | 2 | 0 | 2 |
| pipeline | 6 | 6 | 0 | 12 |
| reports | 10 | 16 | 0 | 26 |

## 4. Distribución por tipo × clase

| Tipo | A | B | C | Total |
|---|---|---|---|---|
| actividad | 10 | 20 | 0 | 30 |
| estados | 13 | 2 | 0 | 15 |
| clases | 14 | 0 | 0 | 14 |
| secuencia | 7 | 3 | 0 | 10 |
| componentes | 0 | 2 | 0 | 2 |
| otro(agr-como-agregacion) | 1 | 0 | 0 | 1 |
| otro(impacto) | 1 | 0 | 0 | 1 |
| otro(componentes-fts) | 1 | 0 | 0 | 1 |
| otro(flujo-de-firma) | 0 | 1 | 0 | 1 |
| otro(secuencia-verify) | 0 | 1 | 0 | 1 |
| otro(pipeline) | 1 | 0 | 0 | 1 |
| otro(tail-sse) | 1 | 0 | 0 | 1 |
| otro(componentes-pipeline-log) | 1 | 0 | 0 | 1 |
| otro(secuencia-pipeline-log) | 0 | 1 | 0 | 1 |
| otro(componentes-export) | 1 | 0 | 0 | 1 |
| otro(secuencia-exportacion-logs) | 0 | 1 | 0 | 1 |
| otro(pipeline-infraestructura) | 1 | 0 | 0 | 1 |
| otro(secuencia-tail-sse) | 0 | 1 | 0 | 1 |
| otro(pipeline-metricas) | 1 | 0 | 0 | 1 |
| caso-de-uso-relacion | 0 | 1 | 0 | 1 |
| otro(actividad-crear) | 0 | 1 | 0 | 1 |
| otro(actividad-aplicar) | 0 | 1 | 0 | 1 |
| otro(actividad-compartir) | 0 | 1 | 0 | 1 |
| otro(secuencia-detalle) | 0 | 1 | 0 | 1 |
| otro(distribucion-de-menus) | 0 | 1 | 0 | 1 |
| otro(flujo-de-anonimizacion-etl) | 0 | 1 | 0 | 1 |

## 5. Detalle por archivo

| # | Archivo | Tipo | Aprobados/Aplicables | % | Clase |
|---|---|---|---|---|---|
| 1 | `requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst` | otro(agr-como-agregacion) | 2/2 | 100% | **A** |
| 2 | `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 3 | `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst` | estados | 2/2 | 100% | **A** |
| 4 | `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 5 | `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-estados-funcion.rst` | estados | 2/2 | 100% | **A** |
| 6 | `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 7 | `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-impacto.rst` | otro(impacto) | 2/2 | 100% | **A** |
| 8 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 9 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 10 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-estados-regla.rst` | estados | 2/2 | 100% | **A** |
| 11 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 12 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta.rst` | estados | 2/2 | 100% | **A** |
| 13 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 14 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 15 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-estados-transicion.rst` | estados | 2/2 | 100% | **A** |
| 16 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 17 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 18 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 19 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 20 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 21 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 22 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-estados-subscription.rst` | estados | 2/2 | 100% | **A** |
| 23 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 24 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 25 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 26 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-componentes-fts.rst` | otro(componentes-fts) | 2/2 | 100% | **A** |
| 27 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 28 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 2/2 | 100% | **A** |
| 29 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-estados-export-job.rst` | estados | 2/2 | 100% | **A** |
| 30 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 31 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-pipeline.rst` | otro(pipeline) | 2/2 | 100% | **A** |
| 32 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-tail-sse.rst` | otro(tail-sse) | 2/2 | 100% | **A** |
| 33 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-componentes-pipeline-log.rst` | otro(componentes-pipeline-log) | 2/2 | 100% | **A** |
| 34 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-componentes-export.rst` | otro(componentes-export) | 2/2 | 100% | **A** |
| 35 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-pipeline-infraestructura.rst` | otro(pipeline-infraestructura) | 2/2 | 100% | **A** |
| 36 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-estados-overall.rst` | estados | 2/2 | 100% | **A** |
| 37 | `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-pipeline-metricas.rst` | otro(pipeline-metricas) | 2/2 | 100% | **A** |
| 38 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 39 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-estados-ejecucion-etl.rst` | estados | 2/2 | 100% | **A** |
| 40 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 41 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 2/2 | 100% | **A** |
| 42 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-estados-frescura-datos.rst` | estados | 2/2 | 100% | **A** |
| 43 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-estados-reintento.rst` | estados | 2/2 | 100% | **A** |
| 44 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 45 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 46 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-estados-saved-view.rst` | estados | 2/2 | 100% | **A** |
| 47 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-estados-share.rst` | estados | 2/2 | 100% | **A** |
| 48 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 49 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 50 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 51 | `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 52 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 53 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-clases.rst` | clases | 2/2 | 100% | **A** |
| 54 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 55 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 56 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-flujo-de-firma.rst` | otro(flujo-de-firma) | 1/2 | 50% | **B** |
| 57 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst` | otro(secuencia-verify) | 1/2 | 50% | **B** |
| 58 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 59 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 60 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-secuencia-pipeline-log.rst` | otro(secuencia-pipeline-log) | 1/2 | 50% | **B** |
| 61 | `requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 62 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 63 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst` | otro(secuencia-exportacion-logs) | 1/2 | 50% | **B** |
| 64 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 65 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst` | otro(secuencia-tail-sse) | 1/2 | 50% | **B** |
| 66 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 67 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-componentes.rst` | componentes | 1/2 | 50% | **B** |
| 68 | `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 69 | `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst` | estados | 1/2 | 50% | **B** |
| 70 | `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst` | estados | 1/2 | 50% | **B** |
| 71 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 72 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 73 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 74 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-componentes.rst` | componentes | 1/2 | 50% | **B** |
| 75 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 76 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | 50% | **B** |
| 77 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 78 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso-relacion-de-inclusion.rst` | caso-de-uso-relacion | 2/5 | 40% | **B** |
| 79 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-actividad-crear.rst` | otro(actividad-crear) | 1/2 | 50% | **B** |
| 80 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-aplicar.rst` | otro(actividad-aplicar) | 1/2 | 50% | **B** |
| 81 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-compartir.rst` | otro(actividad-compartir) | 1/2 | 50% | **B** |
| 82 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 83 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-secuencia-detalle.rst` | otro(secuencia-detalle) | 1/2 | 50% | **B** |
| 84 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 85 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | 50% | **B** |
| 86 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 87 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | 50% | **B** |
| 88 | `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 89 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 90 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-distribucion-de-menus.rst` | otro(distribucion-de-menus) | 1/2 | 50% | **B** |
| 91 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | 50% | **B** |
| 92 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-flujo-de-anonimizacion-etl.rst` | otro(flujo-de-anonimizacion-etl) | 1/2 | 50% | **B** |

## 6. Archivos clase C (recreate desde cero)

(ninguno)

## 7. Archivos clase B (complement)

**39 archivos** requieren complemento:

| # | Archivo | Tipo | Score | Ejes faltantes |
|---|---|---|---|---|
| 1 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 2 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 3 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-flujo-de-firma.rst` | otro(flujo-de-firma) | 1/2 | comprension_dominio |
| 4 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst` | otro(secuencia-verify) | 1/2 | comprension_dominio |
| 5 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 6 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 7 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-secuencia-pipeline-log.rst` | otro(secuencia-pipeline-log) | 1/2 | comprension_dominio |
| 8 | `requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 9 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 10 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst` | otro(secuencia-exportacion-logs) | 1/2 | comprension_dominio |
| 11 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 12 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst` | otro(secuencia-tail-sse) | 1/2 | comprension_dominio |
| 13 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 14 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-componentes.rst` | componentes | 1/2 | panorama |
| 15 | `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 16 | `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst` | estados | 1/2 | comprension_dominio |
| 17 | `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst` | estados | 1/2 | comprension_dominio |
| 18 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 19 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 20 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 21 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-componentes.rst` | componentes | 1/2 | panorama |
| 22 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 23 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | comprension_dominio |
| 24 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 25 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso-relacion-de-inclusion.rst` | caso-de-uso-relacion | 2/5 | extension, generalizacion, comprension_dominio |
| 26 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-actividad-crear.rst` | otro(actividad-crear) | 1/2 | comprension_dominio |
| 27 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-aplicar.rst` | otro(actividad-aplicar) | 1/2 | comprension_dominio |
| 28 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-compartir.rst` | otro(actividad-compartir) | 1/2 | comprension_dominio |
| 29 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 30 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-secuencia-detalle.rst` | otro(secuencia-detalle) | 1/2 | comprension_dominio |
| 31 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 32 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | comprension_dominio |
| 33 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 34 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-secuencia.rst` | secuencia | 1/2 | comprension_dominio |
| 35 | `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 36 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 37 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-distribucion-de-menus.rst` | otro(distribucion-de-menus) | 1/2 | comprension_dominio |
| 38 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-actividad.rst` | actividad | 1/2 | comprension_dominio |
| 39 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-flujo-de-anonimizacion-etl.rst` | otro(flujo-de-anonimizacion-etl) | 1/2 | comprension_dominio |

## 8. Archivos clase A (verify only)

**53 archivos** clasificados A — verificación manual ligera.

## 9. Próximos pasos

- T-004: matriz consolidada A/B/C × clases nuevas requeridas.
- T-005: catálogo de stubs de clase nueva.
- T-006: definir patrones UML-07 obligatorios por categoría de UC.

## Refs

- T-001: inventario.
- T-002: cobertura domain-model.
- Material UML-07: `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`.
