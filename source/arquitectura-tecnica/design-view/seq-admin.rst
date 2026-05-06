.. meta::
 :artefacto: AT_DESIGN_SEQ_ADMIN
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: admin
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_admin:

============================================================
Design View — MOD_Admin: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Admin: creacion de una nueva
``SeparationRule`` en el catalogo, con verificacion previa de
permiso ``create_separation_rule`` y emision de AuditEvent.

.. uml::
 :caption: MOD_Admin — crear regla SoD en catalogo.

 @startuml

 actor "create_separation_rule" as create_separation_rule
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 create_separation_rule -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> create_separation_rule : OK
 deactivate AuthorizationGuard

 create_separation_rule -> FunctionRepo : exists(conjuntoA)
 activate FunctionRepo
 FunctionRepo --> create_separation_rule : OK
 create_separation_rule -> FunctionRepo : exists(conjuntoB)
 FunctionRepo --> create_separation_rule : OK
 deactivate FunctionRepo

 create_separation_rule -> SeparationRuleRepo : create(rule)
 activate SeparationRuleRepo
 SeparationRuleRepo --> create_separation_rule : SeparationRule
 deactivate SeparationRuleRepo

 create_separation_rule -> AuditService : emit(AuditEvent\ntype=high)
 activate AuditService
 AuditService --> create_separation_rule : OK
 deactivate AuditService

 note right of AuditService
   P-39: cambios al catalogo RBAC
   son auditoria de criticidad alta.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-admin`
 - :doc:`/arquitectura-tecnica/use-case-view/admin/index`
 - :doc:`/arquitectura-tecnica/domain-model/function`
 - :doc:`/arquitectura-tecnica/domain-model/function-group`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 - :doc:`/arquitectura-tecnica/domain-model/function-repo`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
