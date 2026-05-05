.. meta::
 :artefacto: AT_UC_MOD_ACCESS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_access:

=================================================
MOD_Access — Asignacion de Accesos: UC por Modulo
=================================================

Vista funcional del RBAC: asignar y revocar funciones
individuales, gestionar agrupadores y reglas SoD. Coexiste
con ``MOD_Permissions`` (Hipótesis 1 — decisión
arquitectónica aprobada).

.. uml::
 :caption: MOD_Access — AccessAdmin gestiona asignaciones;
           Auditor lee.

 @startuml
 left to right direction

 actor User
 actor AccessAdmin
 actor Auditor

 User <|-- AccessAdmin
 User <|-- Auditor

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones\na Usuario" as UC_ACC_01
   usecase "UC_ACC_02\nRevocar Funciones\nde Usuario" as UC_ACC_02
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos" as UC_ACC_03
   usecase "UC_ACC_04\nAsignar Agrupador\na Usuario" as UC_ACC_04
   usecase "UC_ACC_05\nGestionar Reglas SoD" as UC_ACC_05
   usecase "UC_ACC_08\nOtorgar Permiso\nTemporal Excepcional" as UC_ACC_08
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as UC_ACC_09
 }

 User        --> UC_ACC_03
 AccessAdmin --> UC_ACC_01
 AccessAdmin --> UC_ACC_02
 AccessAdmin --> UC_ACC_04
 AccessAdmin --> UC_ACC_05
 AccessAdmin --> UC_ACC_08
 Auditor     --> UC_ACC_09

 UC_ACC_08 ..> UC_ACC_01 : <<extend>>

 note right of MOD_Access
   Codenames RBAC:
     User → view_assignments
     AccessAdmin (AGR-007) →
       assign_functions, revoke_functions,
       assign_function_groups,
       view_separation_rules,
       manage_separation_rules
     Auditor (AGR-008) → view_audit_log
   CNST-031: UC_ACC_08 con rango temporal.
 end note

 @enduml

Lectura del diagrama
====================

- Cualquier ``User`` autenticado consulta sus permisos
  efectivos (``UC_ACC_03``).
- ``AccessAdmin`` (AGR-007) gestiona asignaciones,
  revocaciones, agrupadores y reglas SoD.
- ``UC_ACC_08 Otorgar Permiso Temporal`` ``<<extend>>``
  ``UC_ACC_01`` cuando se requiere asignación con
  ventana temporal acotada (CNST-031).
- ``Auditor`` (AGR-008) consume ``UC_ACC_09`` para
  trazar cambios de acceso (read-only).

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/assignment` — Assignment entity.
- :doc:`/arquitectura-tecnica/domain-model/assignment-repo` — AssignmentRepo (UC_ACC_01/02/04).
- :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` — ExceptionalPermission entity.
- :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` — ExceptionalPermissionRepo (UC_ACC_08).
- :doc:`/arquitectura-tecnica/domain-model/rbac-repo` — RbacRepo.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule` — SeparationRule (UC_ACC_05).
- :doc:`/arquitectura-tecnica/domain-model/audit-event` — AuditEvent (UC_ACC_09).


.. toctree::
 :maxdepth: 1
 :caption: Casos de uso del módulo

 uc-acc-01/index
 uc-acc-02/index
 uc-acc-03/index
 uc-acc-04/index
 uc-acc-05/index
 uc-acc-08/index
 uc-acc-09/index

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
