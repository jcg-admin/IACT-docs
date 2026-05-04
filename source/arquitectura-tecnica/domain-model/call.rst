.. meta::
 :artefacto: AT_DM_CLASS_CALL
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Calls
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_call:

====
Call
====

Registro de una llamada telefonica procesada por el call center.
Dato de solo lectura proveniente de la base de datos operativa
(CNST-007). El sistema IACT no realiza operaciones de escritura
sobre esta entidad.

.. uml::
 :caption: Clase Call — registro operativo de llamada (solo lectura).

 @startuml

 class Call {
   + call_id : String
   + started_at : DateTime
   + duration_seconds : Integer
   + agent_id : String
   + campaign_id : String
   + center : String
   + region : String
   + abandoned : Boolean
   + transferred : Boolean
 }

 class Campaign {
   + campaign_id : String
   + name : String
   + service_type : String
   + region : String
 }

 Call "*" -- "1" Campaign

 note bottom of Call
   CNST-007: BD operativa de solo lectura.
   Sin operaciones de escritura desde IACT.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/campaign`
