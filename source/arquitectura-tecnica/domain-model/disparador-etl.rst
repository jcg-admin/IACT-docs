.. meta::
 :artefacto: AT_DM_CLASS_DISPARADOR_ETL
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_disparador_etl:

==============
DisparadorETL
==============

Disparador (trigger) interno del pipeline ETL de supervision.
Aplica vocabulario STD-010 — el termino canonico es
"Disparador" en lugar del tecnico "Trigger". Coordina dos
modos de invocacion del pipeline:

1. **Programado** — cron expression que dispara runs
   periodicos del ETL.
2. **Manual** — invocacion explicita desde uc-pip-04
   (reintento solicitado por usuario con capability
   ``manage_pipeline``).

NO ejecuta el ETL directamente; encola un mensaje en
``InternalMailbox`` que sera consumido por el
``Procesador Asincrono`` (worker ETL).

.. uml::
 :caption: DisparadorETL — disparo programado o manual
           del pipeline ETL.

 @startuml

 class DisparadorETL {
   - cron_expression : String
   - mailbox : InternalMailbox
   --
   + schedule(cron : String) : void
   + invocar_reproceso(actor_user_id : UUID, \
                        scope : ETLScope) : ETLRunId
   + cancel_scheduled() : void
 }

 class ETLScope {
   + pipeline_id : UUID
   + from_date : Date
   + to_date : Date
 }

 class ETLRunId

 DisparadorETL ..> ETLScope : accepts
 DisparadorETL ..> ETLRunId : returns

 @enduml

Operaciones principales
=======================

- ``schedule(cron)`` — registra una expresion cron para
  disparos periodicos.
- ``invocar_reproceso(actor, scope)`` — encola un mensaje
  al ``Procesador Asincrono`` para reprocesar el rango
  indicado. Devuelve ``etl_run_id`` para tracking.
- ``cancel_scheduled()`` — desactiva el schedule actual.

Restricciones aplicables
========================

- **CNST-025** — el disparo manual se audita via
  ``AuditService.emit("ETL_REINTENTO_SOLICITADO")``.
- **BR-009** — la cancelacion de schedule es logica
  (``state=PAUSED``).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  reintento manual de ETL.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
  consulta del estado del schedule.

Relaciones
==========

- Encola en ``InternalMailbox`` para consumo del
  ``Procesador Asincrono`` (worker ETL).
- Es invocado por ``Servicio de Aplicacion`` y por el
  ``Planificador`` (cron).
- Es subordinado a ``SupervisionETLService``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
