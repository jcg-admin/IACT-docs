.. meta::
 :artefacto: AT_DM_CLASS_SCHEDULED_REPORT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_scheduled_report:

===============
ScheduledReport
===============

Programacion automatica de un reporte. Usa expresion cron para
definir la frecuencia de generacion. Se desactiva, no se elimina
(BR-009 v2.0.0).

.. uml::
 :caption: Clase ScheduledReport — programacion automatica de reporte.

 @startuml

 class ScheduledReport {
   + schedule_id : UUID
   + report_id : UUID
   + owner_user_id : UUID
   + schedule_expression : String   <<cron>>
   + next_run_at : DateTime
   + last_run_at : DateTime
   + state : ScheduleState
   --
   + create()             <<schedule_report>>
   + modify()
   + disable()            <<BR-009>>
 }

 enum ScheduleState {
   ACTIVE
   DISABLED
 }

 ScheduledReport -- ScheduleState

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/report`
