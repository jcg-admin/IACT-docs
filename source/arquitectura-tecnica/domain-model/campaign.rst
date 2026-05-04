.. meta::
 :artefacto: AT_DM_CLASS_CAMPAIGN
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Calls
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_campaign:

========
Campaign
========

Campana de llamadas del call center. Dato de solo lectura proveniente
de la base de datos operativa (CNST-007). Cada ``Call`` pertenece a
una ``Campaign``.

.. uml::
 :caption: Clase Campaign — campana operativa del call center (solo lectura).

 @startuml

 class Campaign {
   + campaign_id : String
   + name : String
   + service_type : String
   + region : String
 }

 note bottom of Campaign
   CNST-007: BD operativa de solo lectura.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-calls`
 :doc:`/arquitectura-tecnica/domain-model/call`
