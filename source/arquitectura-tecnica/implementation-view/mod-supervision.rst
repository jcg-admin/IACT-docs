.. meta::
 :artefacto: AT_IMPL_MOD_SUPERVISION
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_supervision:

==========================================
Implementation View — MOD_Supervision
==========================================

Componentes y paquetes de codigo del modulo de supervision en tiempo real.
Cubre monitoreo de ``Call`` activas (readonly desde BDOperativa, CNST-007),
barge-in del supervisor y broadcast via ``InternalMailbox``.

.. uml::
 :caption: Implementation View MOD_Supervision — componentes de supervision en tiempo real.

 @startuml

 package "MOD_Supervision" {
   component "SupervisionView\nBargeInView\nBroadcastView" as SupervisionView <<api>>
   component "SupervisionSerializer\nBroadcastSerializer" as SupervisionSerializer <<serializer>>
   component "SupervisionService\nmonitorear llamadas activas\nbarge-in a Call\nenviar broadcast" as SupervisionService <<service>>
   component "CallRepository\nInternalMailboxRepository" as SupervisionRepo <<repository>>
   component "CallORM\nInternalMailboxORM" as SupervisionORM <<orm>>
 }

 database "BDOperativa\n(MariaDB, readonly)" as BDOperativa
 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 SupervisionView --> SupervisionSerializer : valida
 SupervisionView --> SupervisionService : invoca
 SupervisionService --> SupervisionRepo : consulta / persiste
 SupervisionRepo --> SupervisionORM : mapea
 SupervisionORM --> BDOperativa : SELECT calls activas\n<<CNST-007: readonly>>
 SupervisionORM --> AlmacenDatos : INSERT audit_events\nINSERT internal_mailbox

 note right of SupervisionService
   Call: leido desde BDOperativa (readonly CNST-007).
   barge-in: supervisor se une a llamada activa.
   InternalMailbox: broadcast a agentes del equipo.
   AuditEvent{CONFIG_CHANGED, details:{barge_in:call_id}}.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
