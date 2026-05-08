.. meta::
 :artefacto: AT_DM_CLASS_LOG_STORE
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

.. _dm_class_log_store:

=========
LogStore
=========

Almacen append-only de logs de aplicacion (``ApplicationLog``).
Abstrae la persistencia en almacenes especializados (TSDB,
columnar, full-text-search) sin acoplar al consumidor a una
tecnologia concreta.

Provee tres modos de acceso:

1. **Append** — escritura individual o batch de entries.
2. **Query** — consulta paginada con cursor para UI de
   reportes (``uc-log-04``).
3. **Tail SSE** — streaming continuo via Server-Sent Events
   para vista en tiempo real (``uc-log-01``).

.. uml::
 :caption: LogStore — almacen append-only con query
           paginado y tail SSE.

 @startuml

 class LogStore {
   --
   + append(log_entry : ApplicationLog) : void
   + append_batch(entries : List<ApplicationLog>) : void
   + query(filters : LogFilters, \
            range : DateRange, \
            cursor : Cursor) : LogQueryResult
   + tail_sse(filters : LogFilters) : Stream<ApplicationLog>
 }

 class ApplicationLog
 class LogFilters {
   + level : LogLevel
   + service : String
   + tenant_id : UUID
 }

 class LogQueryResult {
   + entries : List<ApplicationLog>
   + next_cursor : Cursor
 }

 LogStore --> ApplicationLog : persists
 LogStore ..> LogFilters : queries with
 LogStore ..> LogQueryResult : returns

 @enduml

Operaciones principales
=======================

- ``append(log_entry)`` — persiste una sola entrada (low
  volume).
- ``append_batch(entries)`` — persiste batch (alto volume,
  usado por ingest pipeline).
- ``query(filters, range, cursor)`` — consulta historica
  paginada via cursor.
- ``tail_sse(filters)`` — stream continuo, mantiene la
  conexion abierta enviando nuevas entries que matchean.

Restricciones aplicables
========================

- **Append-only** — no soporta delete ni update; los logs
  son inmutables tras commit.
- **CNST-018** — el filtrado por ``tenant_id`` respeta el
  alcance del usuario consultor.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/logs/uc-log-01/index` — tail
  SSE en tiempo real.
- :doc:`/requisitos/casos-uso/logs/uc-log-04/index` — query
  historica con export.

Relaciones
==========

- Es escrito por el ingest pipeline (worker async).
- Es leido por servicios de logs (consulta + tail).
- Distinto de ``InfraLogStore`` (logs de infraestructura
  interna).

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log`
 - :doc:`/arquitectura-tecnica/domain-model/infra-log-store`
