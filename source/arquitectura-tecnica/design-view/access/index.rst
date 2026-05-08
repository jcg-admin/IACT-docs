.. meta::
 :artefacto: AT_DESIGN_MOD_ACCESS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_access:

============================================================
Design View — MOD_Access: Vista de Diseño
============================================================

Caja del modulo **MOD_Access** (asignaciones RBAC). Este
modulo gestiona las relaciones entre usuarios y grupos de
funciones, validando reglas de separacion antes de crear o
modificar cualquier asignacion.

Materializa los UCs UC_ACC_01..09 documentados en
:doc:`/arquitectura-tecnica/use-case-view/access/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Access — entidades del bounded context y
           puntos de contacto inter-modulo. Subset curado
           para vista de modulo; el detalle de repositories
           y relaciones internas vive en
           :doc:`bounded-context`.

 @startuml

 package "MOD_Access" {
   class Assignment <<entity>>
   class AccessGroup <<entity>>
   class SeparationRule <<entity>>
 }

 class AuthorizationGuard <<service>>
 class AuditService <<service>>

 Assignment --> AccessGroup : opcional
 Assignment ..> SeparationRule : <<verifica>>
 AccessGroup *-- "*" Assignment : agrega

 AuthorizationGuard ..> Assignment : <<crea / revoca>>
 AuthorizationGuard ..> SeparationRule : <<valida SoD>>

 Assignment ..> AuditService : <<emite AuditEvent>>
 SeparationRule ..> AuditService : <<emite AuditEvent>>

 note bottom of Assignment
   3 entidades RBAC del bounded
   context. Repositories y detalles
   de implementacion en :doc:`bounded-context`.
 end note

 @enduml

Lectura del diagrama
====================

- **Tres entidades centrales** del bounded context: ``Assignment``
  (relacion User ↔ FunctionGroup), ``AccessGroup`` (agrupador
  predefinido de funciones), ``SeparationRule`` (restricciones
  de separation-of-duties).
- **AuthorizationGuard** (servicio del modulo Auth) es el
  iniciador externo de las mutaciones RBAC. Verifica la
  ``SeparationRule`` antes de crear o revocar ``Assignment``.
- **AuditService** (servicio del modulo Audit) recibe los
  eventos de cambio: cada creacion, revocacion, expiracion o
  conflicto de separacion emite ``AuditEvent`` inmutable.
- ``AccessGroup`` agrega instancias de ``Assignment`` de un
  usuario por agrupacion predefinida (AGR-001..012); la
  asignacion individual a una funcion sin AGR tambien es valida.

Clases canonicas que materializan el modulo
============================================

Las clases mostradas viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/assignment` —
  Assignment entity (UC_ACC_01/02/04).
- :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
  AssignmentRepo.
- :doc:`/arquitectura-tecnica/domain-model/access-group` —
  AccessGroup entity (UC_ACC_04).
- :doc:`/arquitectura-tecnica/domain-model/access-group-repo` —
  AccessGroupRepo.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
  SeparationRule (UC_ACC_05).
- :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo` —
  SeparationRuleRepo.
- :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
  AuthorizationGuard (gateway externo).
- :doc:`/arquitectura-tecnica/domain-model/audit-service` —
  AuditService (consumidor externo).

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Access

 bounded-context
 interaction-pattern
 assignment-lifecycle
 separation-check-flow

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/access/index` —
   UCs del modulo (vista de requisitos).
 - :doc:`/arquitectura-tecnica/design-view/index` —
   raiz de DesignView con todos los modulos.
 - :doc:`/arquitectura-tecnica/design-view/package-overview` —
   vista global de modulos y dependencias inter-modulo.
