.. meta::
 :artefacto: AT_DM_CLASS_SCHEDULED_REPORT_LIST_SERVICE
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

.. _dm_class_scheduled_report_list_service:

==========================
ScheduledReportListService
==========================

Servicio de listado y detalle de ScheduledReport para un actor.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ScheduledReportListService — stub pendiente de desarrollo.

 @startuml

 class ScheduledReportListService {
  + list(actor_id, filters, pagination)
  + detail(id, invoker)
  + runs(id, invoker, pagination)
 }

 @enduml
