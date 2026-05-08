.. meta::
 :artefacto: AT_DESIGN_FLOW_LOG_RETENTION
 :tipo: Diagrama Arquitectonico — Design View — Activity Diagram
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: Logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_flow_log_retention:

============================================================
Design View — Flujo de Retencion: SystemLog
============================================================

Flujo de actividad del proceso de retencion y purga de
``SystemLog``. A diferencia de ``AuditEvent`` (regulatorio,
hash chain, retencion larga), ``SystemLog`` es operativo,
mutable solo via purga, y su retencion sigue una politica
configurable mas corta.

.. uml::
 :caption: SystemLog retention — scheduler -> classify -> purge.

 @startuml

 start

 :scheduler.trigger();
 note right
   Disparo: cron diario o
   evento "log_threshold_exceeded"
 end note

 :calcular cutoff =
   now() - retention_days;

 if (storage_size > threshold?) then (yes)
   :priorizar purga por tamano;
 else (no)
   :ejecutar purga normal por fecha;
 endif

 :SELECT logs WHERE
   created_at < cutoff
   AND level NOT IN ('ERROR', 'CRITICAL');

 if (logs to purge?) then (none)
   stop
 else (>0)
 endif

 :batch DELETE
   (chunks de 10k filas);

 :emit metric
   (logs_purged_total);

 :update job_execution_log
   (status = SUCCESS,
    records_processed);

 stop

 @enduml

Politica de retencion
======================

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Level
   - Retencion (dias)
   - Justificacion
 * - DEBUG
   - 7
   - Diagnostico inmediato; volumen alto
 * - INFO
   - 30
   - Trazabilidad operacional rutinaria
 * - WARNING
   - 90
   - Investigacion de patrones
 * - ERROR
   - 365
   - Diagnostico de incidentes a largo plazo
 * - CRITICAL
   - sin purga
   - Preservacion permanente

``ERROR`` y ``CRITICAL`` no se purgan automaticamente — la
purga manual requiere autorizacion administrativa
(``log_purge_force`` permission).

Invariantes
============

- **I-LOG-01:** la purga es batch — chunks de 10k filas para
  no bloquear writes concurrentes.
- **I-LOG-02:** todo run de purga deja una fila en
  ``job_execution_log`` con ``records_procesados``.
- **I-LOG-03:** ``CRITICAL`` y errores marcados con
  ``preserve = TRUE`` son inmunes a la purga automatica.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log` —
   entidad y campo ``level``.
 - :doc:`bounded-context` — contexto del modulo Logs.
 - :doc:`interaction-pattern` — patron de captura del
   logger.
 - :doc:`/arquitectura-tecnica/design-view/audit/audit-event-lifecycle` —
   distincion ``SystemLog`` (operativo) vs ``AuditEvent``
   (regulatorio).
