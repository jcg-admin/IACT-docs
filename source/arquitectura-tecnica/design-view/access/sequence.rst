.. meta::
 :artefacto: AT_DESIGN_SEQ_ACCESS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: access
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_access:

============================================================
Design View — MOD_Access: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Access: asignacion de
``FunctionGroup`` a un usuario con verificacion previa de
``SeparationRule`` (separation of duties) antes de crear el ``Assignment``.

Actores ``<<sistema>>`` son clases canonicas del domain-model.
La funcion RBAC iniciadora es ``assign_functions_to_group``.

.. uml::
 :caption: MOD_Access — asignacion con verificacion separacion de deberes.

 @startuml

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 assign_functions_to_group -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> assign_functions_to_group : OK
 deactivate AuthorizationGuard

 assign_functions_to_group -> SeparationRuleRepo : check_separation(user_id, group_ref)
 activate SeparationRuleRepo
 SeparationRuleRepo --> assign_functions_to_group : sod_result
 deactivate SeparationRuleRepo

 alt conflicto de separacion detectado
   assign_functions_to_group --> assign_functions_to_group : 422 Separation Violation
 else sin conflicto
   assign_functions_to_group -> AssignmentRepo : create(Assignment)
   activate AssignmentRepo
   AssignmentRepo --> assign_functions_to_group : Assignment
   deactivate AssignmentRepo

   assign_functions_to_group -> AuditService : emit(AuditEvent)
   activate AuditService
   AuditService --> assign_functions_to_group : OK
   deactivate AuditService
 end

 note right of SeparationRuleRepo
   CNST-005: separacion evaluada en
   funciones, no en grupos.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/access/class`
 - :doc:`/arquitectura-tecnica/use-case-view/access/index`
 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
