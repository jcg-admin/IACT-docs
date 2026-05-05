8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_03 vs UC_ACC_08

 @startuml
 left to right direction

 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "view_audit_log" as view_audit_log

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_08\nGrant excepcional" as UC_ACC_08
 }
 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_03\nGrant excepcional" as PERM03
 }
 rectangle "Backend compartido" {
   usecase "POST exceptional-permissions" as PostExceptionalPermissions
 }

 grant_exceptional_permission --> UC_ACC_08
 grant_exceptional_permission --> PERM03
 UC_ACC_08 --> PostExceptionalPermissions : delega
 PERM03 --> PostExceptionalPermissions : delega
 PostExceptionalPermissions --> view_audit_log : AuditEvent\nhigh-priority

 note bottom of PostExceptionalPermissions
   Funcion: grant_exceptional_permission
   Mailbox HARD, justification + expires_at
   obligatorios, audit reforzado.
 end note

 @enduml

