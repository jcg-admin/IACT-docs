.. meta::
 :artefacto: AT_DESIGN_CLASS_OPERATOR
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: operator
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_operator:

============================================================
Design View — MOD_Operator: Estructura de Clases
============================================================

Modulo de **operacion del agente**: cambio de estado del agente,
manejo de llamadas (in/out, hold/unhold, transfer), disposition,
breaks, dashboard, mailbox personal.

.. uml::
 :caption: MOD_Operator — clases canonicas y relaciones internas.

 @startuml

 class User
 class Call
 class Action
 class InternalMailbox
 class InternalMessage
 class PermissionService <<sistema>>
 class AuditService <<sistema>>

 User "1" -- "0..n" Action : ejecuta
 User "1" -- "0..n" Call : maneja
 User "1" -- "1" InternalMailbox : posee
 InternalMailbox *-- InternalMessage

 Action --> Call : sobre
 PermissionService ..> Action : verify_function

 Action ..> AuditService : on execute
 Call ..> AuditService : on transition

 note right of InternalMailbox
   CNST-002: cada User tiene un
   InternalMailbox dedicado.
 end note

 @enduml

----

UCs cubiertos
==============

UC_OPR_01..10 — cambiar estado del agente, llamada saliente,
hold/unhold, transfer, disposition, break/pausa, dashboard,
ver mailbox, etc. Ver
:doc:`/arquitectura-tecnica/use-case-view/operator/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/call`
 - :doc:`/arquitectura-tecnica/domain-model/action`
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 - :doc:`/arquitectura-tecnica/domain-model/internal-message`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/operator/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-operator`
