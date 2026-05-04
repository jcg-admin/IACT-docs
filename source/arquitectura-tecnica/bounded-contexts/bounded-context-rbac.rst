.. meta::
 :artefacto: AT_DOMINIO_02_RBAC
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_rbac:

========================================
Modelo de Dominio — Bounded Context RBAC
========================================

4.2 RBAC (subsume PERM)
-----------------------

Seis clases: ``Function``, ``FunctionGroup``, ``AccessGroup``,
``Assignment``, ``ExceptionalPermission`` y ``SeparationRule``. Por
ADR-GOB-008 el cluster PERM es una vista tecnica sobre estas
mismas entidades; no introduce clases adicionales.

.. uml::
 :caption: Bounded context RBAC — modelo de control de acceso
           basado en funciones atomicas.

 @startuml

 class Function {
   + name : String          <<p.ej. view_reports>>
   + description : String
   + module : Module
   --
   + register()             <<sistema>>
   + view()                 <<view_assignments>>
 }

 class FunctionGroup {
   + group_id : UUID
   + name : String
   + description : String
   --
   + create_function_group()       <<create_function_group>>
   + assign_functions_to_group()   <<assign_functions_to_group>>
   + revoke_function_group()       <<revoke_function_group>>
 }

 class AccessGroup {
   + agr_id : String          <<AGR-001..012>>
   + name : String            <<p.ej. agr_supervisor>>
   + profile_description : String
   --
   + assign_to_user()        <<assign_function_groups>>
   + revoke_from_user()
 }

 class Assignment {
   + assignment_id : UUID
   + user_id : UUID
   + group_ref : String       <<FunctionGroup o AccessGroup>>
   + assigned_by : UUID
   + assigned_at : DateTime
   + expires_at : DateTime
   + state : AssignmentState
   --
   + create()
   + revoke()
 }

 class ExceptionalPermission {
   + permission_id : UUID
   + user_id : UUID
   + function_id : String
   + granted_by : UUID
   + granted_at : DateTime
   + expires_at : DateTime
   + justification : String
   + state : PermissionState
   --
   + grant()           <<grant_exceptional_permission>>
   + revoke()          <<revoke_exceptional_permission>>
 }

 class SeparationRule {
   + rule_id : UUID
   + name : String
   + conflicting_functions : List<String>
   + rule_group : String
   + state : RuleState
   --
   + create()                  <<create_separation_rule>>
   + view()                    <<view_separation_rules>>
   + update_separation_rule()  <<update_separation_rule>>
   + disable_separation_rule() <<disable_separation_rule>>
 }

 enum Module {
   AUTH
   USR
   ACC
   PIP
   RPT
   ALR
   AUD
   LOG
 }

 enum AssignmentState {
   ACTIVE
   EXPIRED
   REVOKED
 }
 enum PermissionState {
   ACTIVE
   EXPIRED
   REVOKED
 }
 enum RuleState {
   ENABLED
   DISABLED
 }

 FunctionGroup "*" -- "*" Function : contiene
 Assignment "*" -- "1" FunctionGroup : (cuando group_ref = grupo)
 Assignment "*" -- "1" AccessGroup   : (cuando group_ref = AGR)
 ExceptionalPermission "*" -- "1" Function
 SeparationRule "1" -- "*" Function : (lista funciones en conflicto)
 Function -- Module

 note right of SeparationRule
   BR-009 v2.0.0: desactivar, no eliminar.
   CNST-030: enforcement SoD.
 end note

 note right of ExceptionalPermission
   CNST-031: rango temporal
   (granted_at .. expires_at).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
