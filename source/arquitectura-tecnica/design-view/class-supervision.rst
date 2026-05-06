.. meta::
 :artefacto: AT_DESIGN_CLASS_SUPERVISION
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: supervision
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_supervision:

============================================================
Design View — MOD_Supervision: Estructura de Clases
============================================================

Modulo de **supervision en tiempo real**: ver estado del equipo,
barge-in en llamada activa, broadcast de mensajes al segmento
del Supervisor (CNST-008 isolation por scope).

.. uml::
 :caption: MOD_Supervision — clases canonicas y relaciones internas.

 @startuml

 class User
 class Call
 class InternalMessage
 class InternalMailbox
 class SegmentResolver <<sistema>>
 class PermissionService <<sistema>>
 class AuditService <<sistema>>

 User --> Call : barge-in
 User ..> InternalMessage : crea broadcast
 InternalMessage --> InternalMailbox : encolado en
 SegmentResolver ..> User : resuelve segmento del Supervisor

 PermissionService ..> User : verify_function
 InternalMessage ..> AuditService : on broadcast
 Call ..> AuditService : on barge-in

 note right of SegmentResolver
   CNST-008: target_team o segment_codes
   deben estar en el segmento del Supervisor.
 end note

 @enduml

----

UCs cubiertos
==============

UC_SUP_01..03 — ver estado del equipo, barge-in en llamada,
mensaje broadcast al equipo. Ver
:doc:`/arquitectura-tecnica/use-case-view/supervision/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/call`
 - :doc:`/arquitectura-tecnica/domain-model/internal-message`
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/supervision/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-supervision`
