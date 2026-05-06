.. meta::
 :artefacto: AT_DESIGN_CLASS_ADMIN
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_admin:

============================================================
Design View — MOD_Admin: Estructura de Clases
============================================================

Modulo de **configuracion del catalogo RBAC**: gestiona el ciclo
de vida de funciones, agrupadores del sistema y reglas SoD. Es
el unico modulo que puede mutar el catalogo declarativo.

.. uml::
 :caption: MOD_Admin — clases canonicas y relaciones internas.

 @startuml

 class Function
 class FunctionGroup
 class SeparationRule
 class FunctionRepo <<sistema>>
 class FunctionGroupRepo <<sistema>>
 class SeparationRuleRepo <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 FunctionGroup *-- Function : contiene
 SeparationRule --> Function : conjuntoA
 SeparationRule --> Function : conjuntoB

 FunctionRepo ..> Function
 FunctionGroupRepo ..> FunctionGroup
 SeparationRuleRepo ..> SeparationRule

 AuthorizationGuard ..> FunctionRepo : verify_function
 Function ..> AuditService : on create/update
 FunctionGroup ..> AuditService : on assign
 SeparationRule ..> AuditService : on create/disable

 @enduml

----

UCs cubiertos
==============

UC_ADM_01 (gestionar reglas SoD) · UC_ADM_02 (catalogo de
funciones) · UC_ADM_03 (catalogo de agrupadores). Ver
:doc:`/arquitectura-tecnica/use-case-view/admin/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function`
 - :doc:`/arquitectura-tecnica/domain-model/function-group`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 - :doc:`/arquitectura-tecnica/domain-model/function-repo`
 - :doc:`/arquitectura-tecnica/domain-model/function-group-repo`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/admin/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-admin`
