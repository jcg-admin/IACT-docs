.. meta::
 :artefacto: AT_DESIGN_SEQ_SUPERVISION
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: supervision
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_supervision:

============================================================
Design View — MOD_Supervision: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Supervision: Supervisor envia
``InternalMessage`` broadcast al equipo, con resolucion de
destinatarios via ``SegmentResolver`` (CNST-008 isolation por
scope) y entrega via ``InternalMailbox`` por User.

.. uml::
 :caption: MOD_Supervision — broadcast con resolucion de segmento.

 @startuml

 actor "broadcast_team_messages" as broadcast_team_messages
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "InternalMessage" as InternalMessage <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 broadcast_team_messages -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> broadcast_team_messages : OK
 deactivate AuthorizationGuard

 broadcast_team_messages -> SegmentResolver : resolve(target, supervisor_scope)
 activate SegmentResolver
 SegmentResolver --> broadcast_team_messages : List<User>
 deactivate SegmentResolver

 broadcast_team_messages -> InternalMessage : create(content, urgency)
 activate InternalMessage
 InternalMessage --> broadcast_team_messages : InternalMessage
 deactivate InternalMessage

 loop por cada destinatario
   broadcast_team_messages -> InternalMailbox : enqueue(user, message)
   activate InternalMailbox
   InternalMailbox --> broadcast_team_messages : OK
   deactivate InternalMailbox
 end

 alt urgency = URGENT
   broadcast_team_messages -> InternalMailbox : push_realtime(users)
 end

 broadcast_team_messages -> AuditService : emit(AuditEvent)
 activate AuditService
 AuditService --> broadcast_team_messages : OK
 deactivate AuditService

 note bottom of SegmentResolver
   CNST-008: target_team o segment_codes
   deben estar en el segmento del Supervisor.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-supervision`
 - :doc:`/arquitectura-tecnica/use-case-view/supervision/index`
 - :doc:`/arquitectura-tecnica/domain-model/internal-message`
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
