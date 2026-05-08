.. meta::
 :artefacto: AT_DESIGN_CLASS_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_permissions:

============================================================
Design View — MOD_Permissions: Estructura de Clases
============================================================

Modulo de **runtime check de permisos**: dado un usuario y una
funcion, determina si esta autorizado consultando el effective
set de funciones (intersecta assignments del catalogo + permisos
excepcionales). Es el modulo invocado en CADA operacion del
sistema.

.. uml::
 :caption: MOD_Permissions — clases canonicas y relaciones.

 @startuml

 class Function
 class FunctionGroup
 class Assignment
 class ExceptionalPermission
 class PermissionService <<sistema>>
 class PermissionCache <<sistema>>
 class EffectivePermissionsAggregator <<sistema>>
 class ExceptionalPermissionRepo <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 Assignment --> FunctionGroup
 FunctionGroup *-- Function
 ExceptionalPermission --> Function : grant ad-hoc

 PermissionService ..> EffectivePermissionsAggregator
 EffectivePermissionsAggregator ..> Assignment : consulta
 EffectivePermissionsAggregator ..> ExceptionalPermissionRepo
 PermissionService ..> PermissionCache : cache effective set
 AuthorizationGuard ..> PermissionService : verify(user, function)

 ExceptionalPermission ..> AuditService : create/revoke
 PermissionService ..> AuditService : grant/deny logged

 @enduml

----

UCs cubiertos
==============

UC_PERM_01..10 — asignar/revocar grupo, conceder permiso
excepcional, verificar permiso, gestionar grupos custom, etc.
Ver :doc:`/arquitectura-tecnica/use-case-view/permissions/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function`
 - :doc:`/arquitectura-tecnica/domain-model/function-group`
 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator`
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/permissions/index`
 - :doc:`/arquitectura-tecnica/design-view/permissions/sequence`
