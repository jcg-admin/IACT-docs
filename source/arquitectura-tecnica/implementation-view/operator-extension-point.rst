.. meta::
 :artefacto: AT_IMPL_MOD_OPERATOR_CALLS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_operator_calls:

==========================================
Implementation View — MOD_OperatorCalls
==========================================

Componentes y paquetes de codigo del modulo de llamadas del operador.
Cubre lectura de ``Call`` y ``Campaign`` desde ``BDOperativa`` (MariaDB,
CNST-007: solo lectura), sin escritura en la BD operativa.

.. uml::
 :caption: Implementation View MOD_OperatorCalls — componentes de llamadas de operadores.

 @startuml

 package "MOD_OperatorCalls" {
   component "CallView\nCampaignView\nCallHistoryView" as CallView <<api>>
   component "CallSerializer\nCampaignSerializer" as CallSerializer <<serializer>>
   component "CallService\nconsultar llamadas y campanas\nno escritura en BDOperativa" as CallService <<service>>
   component "CallRepository\nCampaignRepository" as CallRepo <<repository>>
   component "CallORM\nCampaignORM" as CallORM <<orm>>
 }

 database "BDOperativa\n(MariaDB, readonly)" as BDOperativa
 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 CallView --> CallSerializer : valida
 CallView --> CallService : invoca
 CallService --> CallRepo : consulta
 CallRepo --> CallORM : mapea
 CallORM --> BDOperativa : SELECT <<CNST-007: readonly>>
 CallORM --> AlmacenDatos : INSERT audit_events

 note right of CallService
   Call{call_id, agent_id, campaign_id, state, started_at}.
   Campaign: metadatos de campana activa.
   CNST-007: IACT solo lee BDOperativa (MariaDB).
   NUNCA escribe en BDOperativa.
   AuditEvent{ACCESS_CHANGE} en AlmacenDatos.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/campaign`
