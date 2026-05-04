.. meta::
 :artefacto: AT_DOMINIO_03_CALLS
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_calls:

=========================================
Modelo de Dominio — Bounded Context Calls
=========================================

4.3 Calls
---------

Dos clases: ``Call`` y ``Campaign``. Datos de solo lectura
provenientes de la base de datos operativa (CNST-007). El corpus
IACT no realiza operaciones de escritura sobre estas entidades.

.. uml::
 :caption: Bounded context Calls — datos operativos del call
           center (solo lectura).

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
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
