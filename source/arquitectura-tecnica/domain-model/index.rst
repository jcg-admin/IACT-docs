.. meta::
 :artefacto: INDEX_AT_DOMAINMODEL
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 2.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at-domainmodel-index:

===========================
Domain Model — Vista Logica
===========================

Modelo de dominio canonico del sistema IACT. Contiene un archivo por
clase (67 clases en 8 bounded contexts). Las clases con ``:estado:
Pendiente`` son stubs identificados en UCs pero pendientes de
desarrollo completo de atributos canonicos.

Granularidad: una clase por archivo. Los diagramas de cada clase
incluyen sus atributos canonicos, metodos, enums propios y relaciones
directas con otras clases del mismo bounded context.

.. toctree::
 :maxdepth: 1
 :caption: Overview

 overview

.. toctree::
 :maxdepth: 1
 :caption: BC Auth — Autenticacion

 user
 user-repo
 session
 internal-mailbox
 internal-message
 blacklisted-token
 password-generator

.. toctree::
 :maxdepth: 1
 :caption: BC RBAC — Control de Acceso

 function
 function-repo
 function-group
 function-group-repo
 access-group
 access-group-repo
 access-group-function
 function-group-membership
 user-access-group-assignment
 impact-report
 assignment
 assignment-repo
 exceptional-permission
 exceptional-permission-repo
 separation-rule
 separation-rule-repo
 permission-service
 permission-cache
 effective-permissions-aggregator
 user-capability-resolver
 authorization-guard
 rbac-repo
 rule-validator
 menu
 menu-item
 menu-item-repo
 menu-lifecycle-service
 nav-domain
 section
 action

.. toctree::
 :maxdepth: 1
 :caption: BC Calls — Datos Operativos

 call
 campaign

.. toctree::
 :maxdepth: 1
 :caption: BC Reports — Reporteria

 report
 metric
 export-job
 scheduled-report
 saved-view
 saved-filter
 historical-report
 bucket
 comparative
 column-catalog
 filter-validator
 kpi-calculator
 segment-resolver
 segment-scope
 base-report-service
 abandonment-report-service
 agent-report-service
 agent-daily-stat-repo
 campaign-daily-stat-repo
 campaign-report-service
 caller-report-service
 ivr-navigation-report-service
 transfer-report-service
 scheduled-report-list-service
 scheduled-report-repo

.. toctree::
 :maxdepth: 1
 :caption: BC Pipeline

 pipeline-execution
 pipeline-execution-repo
 disparador-etl
 errores-etl-service
 resumen-salud
 resumen-salud-builder

.. toctree::
 :maxdepth: 1
 :caption: BC Alerts — Alertas

 alert
 threshold
 subscription
 subscription-repo
 alert-rule
 alert-rule-repo
 alert-repo
 alert-history-summary
 alert-history-service
 segment-change-listener
 evaluator-reloader
 rule-validator
 timing-calculator

.. toctree::
 :maxdepth: 1
 :caption: BC Audit — Auditoria

 audit-event
 audit-service
 audit-repo
 audit-query-service
 general-audit-service
 audit-validator
 hmac-verifier
 pii-scanner
 sanitizer
 cursor-encoder
 alert-hook
 export-worker

.. toctree::
 :maxdepth: 1
 :caption: BC Logs — Bitacoras

 application-log
 pipeline-log
 infrastructure-log
 log-store
 infra-log-store
 system-health
 technical-metric

.. toctree::
 :maxdepth: 1
 :caption: BC CrossCutting — Politicas y caches

 idempotency-policy
 expiration-policy
 metrics-cache

.. toctree::
 :maxdepth: 1
 :caption: Patrones documentales

 specification-pattern
 strategy-pattern
