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
 session
 internal-mailbox

.. toctree::
 :maxdepth: 1
 :caption: BC RBAC — Control de Acceso

 function
 function-group
 access-group
 access-group-function
 assignment
 exceptional-permission
 separation-rule
 permission-service
 permission-cache
 assignment-repo
 exceptional-permission-repo
 rbac-repo
 rule-validator
 menu
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
 base-report-service
 abandonment-report-service
 agent-report-service
 agent-daily-stat-repo
 caller-report-service
 ivr-navigation-report-service
 transfer-report-service
 scheduled-report-list-service
 scheduled-report-repo

.. toctree::
 :maxdepth: 1
 :caption: BC Pipeline ETL

 etl-ejecucion

.. toctree::
 :maxdepth: 1
 :caption: BC Alerts — Alertas

 alert
 threshold
 subscription
 alert-rule
 alert-repo
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
 audit-validator
 pii-scanner
 sanitizer
 cursor-encoder
 alert-hook
 export-worker

.. toctree::
 :maxdepth: 1
 :caption: BC Logs — Bitacoras

 application-log
 etl-log
 infrastructure-log
 system-health
 technical-metric
