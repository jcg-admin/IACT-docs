.. meta::
 :artefacto: AT_DM_CLASS_INFRA_LOG_STORE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_infra_log_store:

==============
InfraLogStore
==============

Almacen append-only de logs de **infraestructura interna**:
workers, schedulers, healthchecks, observabilidad de
componentes del backend. Distinto de ``LogStore`` (logs de
aplicacion expuestos al user) y de ``InfrastructureLog``
(la entidad).

Su separacion en un store dedicado permite:

1. **Retencion distinta** — los logs de infraestructura
   suelen tener retencion mas corta que los de aplicacion.
2. **Acceso restringido** — solo usuarios con codename
   ``view_infra_logs`` pueden consultarlos.
3. **No expuestos a tenants** — los logs internos no
   incluyen ``tenant_id`` y son cross-tenant por diseno.

.. uml::
 :caption: InfraLogStore — almacen de logs de
           infraestructura interna.

 @startuml

 class InfraLogStore {
   --
   + append(infra_log : InfrastructureLog) : void
   + tail(filters : InfraLogFilters, \
           limit : Integer) : List<InfrastructureLog>
   + query(filters : InfraLogFilters, \
            range : DateRange, \
            cursor : Cursor) : InfraLogQueryResult
 }

 class InfrastructureLog
 class InfraLogFilters {
   + component : String
   + level : LogLevel
   + host : String
 }

 InfraLogStore --> InfrastructureLog : persists
 InfraLogStore ..> InfraLogFilters : queries with

 @enduml

Operaciones principales
=======================

- ``append(infra_log)`` — persiste entry de infra log.
- ``tail(filters, limit)`` — devuelve las ultimas N entries
  recientes que matchean.
- ``query(filters, range, cursor)`` — consulta historica
  paginada.

Restricciones aplicables
========================

- **Append-only** — inmutable tras commit.
- **Retencion < LogStore** — politica de retencion tipica:
  30-90 dias (configurable).
- **Acceso restringido** — codename ``view_infra_logs``
  obligatorio.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/logs/uc-log-05/index` —
  consulta de logs de infraestructura.

Relaciones
==========

- Es escrito por hooks de logging interno del runtime.
- Es leido solo por endpoints autorizados (``view_infra_logs``).
- Distinto de ``LogStore``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`
 - :doc:`/arquitectura-tecnica/domain-model/log-store`
