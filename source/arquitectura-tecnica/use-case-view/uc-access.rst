.. meta::
 :artefacto: AT_UC_MOD_ACCESS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_access:

=================================================
MOD_Access — Asignacion de Accesos: UC por Modulo
=================================================

MOD_Access — Asignacion de Accesos
=====================================

Vista funcional del RBAC: asignar y revocar funciones individuales,
gestionar agrupadores y reglas SoD. Coexiste con MOD_Permissions
(Hipotesis 1 — decision arquitectonica aprobada).

.. uml::
 :caption: Figura 18 — MOD_Access: casos de uso

 @startuml
 left to right direction

 actor "assign_functions" as assign_functions
 actor "revoke_functions" as revoke_functions
 actor "view_assignments" as view_assignments
 actor "assign_function_groups" as assign_function_groups
 actor "view_separation_rules" as view_separation_rules
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones\na Usuario" as UC_ACC_01
   usecase "UC_ACC_02\nRevocar Funciones\nde Usuario" as UC_ACC_02
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos" as UC_ACC_03
   usecase "UC_ACC_04\nAsignar Agrupador\na Usuario" as UC_ACC_04
   usecase "UC_ACC_05\nGestionar Reglas SoD" as UC_ACC_05
   usecase "UC_ACC_08\nOtorgar Permiso\nTemporal Excepcional" as UC_ACC_08
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as UC_ACC_09
 }

 assign_functions --> UC_ACC_01
 assign_functions --> UC_ACC_08
 revoke_functions --> UC_ACC_02
 view_assignments --> UC_ACC_03
 assign_function_groups --> UC_ACC_04
 view_separation_rules --> UC_ACC_05
 view_audit_log --> UC_ACC_09
 view_assignments --> UC_ACC_09

 UC_ACC_08 ..> UC_ACC_01 : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
