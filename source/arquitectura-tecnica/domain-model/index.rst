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
cada clase de dominio (26 clases en 7 bounded contexts) extraidas de
los diagramas canónicos en ``bounded-contexts/``.

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
 assignment
 exceptional-permission
 separation-rule

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

.. toctree::
 :maxdepth: 1
 :caption: BC Audit — Auditoria

 audit-event

.. toctree::
 :maxdepth: 1
 :caption: BC Logs — Bitacoras

 application-log
 etl-log
 infrastructure-log
 system-health
 technical-metric
