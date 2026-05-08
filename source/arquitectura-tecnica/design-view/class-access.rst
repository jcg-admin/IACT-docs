.. meta::
 :artefacto: AT_DESIGN_CLASS_ACCESS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_access:

============================================================
Design View — MOD_Access: Estructura de Clases
============================================================

Modulo de **asignaciones RBAC**: gestiona las relaciones entre
usuarios y grupos de funciones, validando reglas de separacion antes de
crear o modificar cualquier asignacion.

Las clases mostradas viven en ``domain-model/``. Aqui solo se
ven como cajas y se enfatizan sus relaciones internas en este
bounded context.

.. uml::
 :caption: MOD_Access — clases canonicas y relaciones internas.

 @startuml

 class Assignment
 class AccessGroup
 class FunctionGroup
 class SeparationRule
 class AssignmentRepo <<sistema>>
 class AccessGroupRepo <<sistema>>
 class SeparationRuleRepo <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 Assignment --> FunctionGroup : asigna
 Assignment --> AccessGroup : opcional
 SeparationRule --> FunctionGroup : restringe pares
 AccessGroup *-- FunctionGroup : agrupa

 AssignmentRepo ..> Assignment : persiste
 AccessGroupRepo ..> AccessGroup
 SeparationRuleRepo ..> SeparationRule

 AuthorizationGuard ..> SeparationRuleRepo : valida separacion de deberes
 AuthorizationGuard ..> AssignmentRepo : crea/revoca

 Assignment ..> AuditService : emite AuditEvent
 SeparationRule ..> AuditService : emite AuditEvent

 @enduml

----

UCs cubiertos por este modulo
==============================

UC_ACC_01..09 — gestion de asignaciones, validacion de separacion,
revocacion, expiracion. Ver
:doc:`/arquitectura-tecnica/use-case-view/access/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/access-group`
 - :doc:`/arquitectura-tecnica/domain-model/function-group`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo`
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/access/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-access`
