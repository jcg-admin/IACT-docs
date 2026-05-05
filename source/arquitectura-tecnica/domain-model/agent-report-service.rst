.. meta::
 :artefacto: AT_DM_CLASS_AGENT_REPORT_SERVICE
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

.. _dm_class_agent_report_service:

==================
AgentReportService
==================

Servicio de reporte de agentes. Lista y detalle por periodo.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AgentReportService — stub pendiente de desarrollo.

 @startuml

 class AgentReportService {
  + list(filters, period, page)
  + detail(agent_id, period)
 }

 @enduml
