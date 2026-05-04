.. meta::
 :artefacto: AT_DM_CLASS_AGENT_DAILY_STAT_REPO
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

.. _dm_class_agent_daily_stat_repo:

==================
AgentDailyStatRepo
==================

Repositorio de estadisticas diarias por agente.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AgentDailyStatRepo — stub pendiente de desarrollo.

 @startuml

 class AgentDailyStatRepo {
  + aggregate_by_agent(filters, period)
  + stream_by_agent(agent_id, period)
 }

 @enduml
