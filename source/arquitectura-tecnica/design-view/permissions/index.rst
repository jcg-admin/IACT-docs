.. meta::
 :artefacto: AT_DESIGN_MOD_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_permissions:

============================================================
Design View — MOD_Permissions: Vista de Diseño
============================================================

Caja del modulo **MOD_Permissions** (resolucion runtime de
permisos efectivos). Calcula el effective_set de un usuario
combinando ``Assignment`` regulares + ``ExceptionalPermission``
ad-hoc + cache para gateway checks de alta frecuencia.

Materializa los UCs UC_PERM_01..10 documentados en
:doc:`/arquitectura-tecnica/use-case-view/permissions/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Permissions — agregador de effective_set
           (regulares + excepcionales). Detalle de cache y
           repos en :doc:`class`.

 @startuml

 package "MOD_Permissions" {
   class EffectivePermissionsAggregator <<service>>
   class ExceptionalPermission <<entity>>
   class PermissionCache <<service>>
 }

 class Assignment <<external>>
 class AuthorizationGuard <<external>>
 class AuditService <<external>>

 EffectivePermissionsAggregator ..> Assignment : <<lee regulares>>
 EffectivePermissionsAggregator ..> ExceptionalPermission : <<lee excepcionales>>
 EffectivePermissionsAggregator ..> PermissionCache : <<consulta / invalida>>

 AuthorizationGuard ..> EffectivePermissionsAggregator : <<resolve>>
 ExceptionalPermission ..> AuditService : <<emite grant/revoke>>

 note bottom of EffectivePermissionsAggregator
   Combina Assignment regulares
   + ExceptionalPermission ad-hoc.
   El cache evita re-calculo en
   gateway checks. Detalle en
   :doc:`class`.
 end note

 @enduml

Lectura del diagrama
====================

- **Servicio central:** ``EffectivePermissionsAggregator``
  combina las dos fuentes de capabilities (Assignment via
  AGRs/FunctionGroups + ExceptionalPermission ad-hoc) en un
  unico ``effective_set`` por usuario.
- **Cache:** ``PermissionCache`` evita re-calcular el
  effective_set en cada gateway check; se invalida ante
  cambios de Assignment, ExceptionalPermission o
  segmentacion del usuario.
- **Consumidor:** ``AuthorizationGuard`` invoca el resolver
  para verificar capabilities en cada operacion privilegiada.
- **Excepciones:** ``ExceptionalPermission`` permite
  conceder o revocar capabilities ad-hoc fuera del catalogo
  AGR (UC_PERM_03/04); cada cambio se audita.

Ver el flujo de calculo completo en :doc:`activity`.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator`
  — EffectivePermissionsAggregator.
- :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
  ExceptionalPermission entity.
- :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo`
  — ExceptionalPermissionRepo.
- :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
  PermissionCache.
- :doc:`/arquitectura-tecnica/domain-model/permission-service` —
  PermissionService.
- :doc:`/arquitectura-tecnica/domain-model/rbac-repo` —
  RBACRepo (consolidador).
- :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
  AuthorizationGuard (consumidor externo).
- :doc:`/arquitectura-tecnica/domain-model/audit-service`.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Permissions

 class
 sequence
 activity

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/permissions/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/access/index` —
   modulo emisor de Assignment.
 - :doc:`/arquitectura-tecnica/design-view/auth/index` —
   modulo que invoca AuthorizationGuard.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
