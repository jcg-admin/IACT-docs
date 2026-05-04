.. meta::
 :artefacto: AT_DM_CLASS_SCHEDULED_REPORT_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_scheduled_report_repo:

===================
ScheduledReportRepo
===================

Repositorio de ScheduledReport y sus ejecuciones.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ScheduledReportRepo — stub pendiente de desarrollo.

 @startuml

 class ScheduledReportRepo {
  + list_by_actor(actor_id, filters)
  + get(id)
  + list_runs(id)
 }

 @enduml
