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
   usecase "UC_ACC_01\nAsignar Funciones\na Usuario" as AC01
   usecase "UC_ACC_02\nRevocar Funciones\nde Usuario" as AC02
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos" as AC03
   usecase "UC_ACC_04\nAsignar Agrupador\na Usuario" as AC04
   usecase "UC_ACC_05\nGestionar Reglas SoD" as AC05
   usecase "UC_ACC_08\nOtorgar Permiso\nTemporal Excepcional" as AC08
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as AC09
 }

 assign_functions --> AC01
 assign_functions --> AC08
 revoke_functions --> AC02
 view_assignments --> AC03
 assign_function_groups --> AC04
 view_separation_rules --> AC05
 view_audit_log --> AC09
 view_assignments --> AC09

 AC08 ..> AC01 : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
