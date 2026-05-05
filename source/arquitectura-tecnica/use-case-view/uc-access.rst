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

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
