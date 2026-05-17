8.4 Diagrama de clases — fuentes de permisos
============================================

.. uml::
 :caption: 3 fuentes que UC_ACC_03 consolida

 @startuml

 class User {
   id: int
   username: string
   state: enum
 }

 class Assignment {
   id: int
   user_id: int
   target_type: enum {Function, AccessGroup}
   target_id: int
   state: enum {ACTIVE, REVOKED, EXPIRED}
   granted_at: timestamp
   expires_at: opt[timestamp]
 }

 class AccessGroup {
   id: int
   code: string
   display_name: string
   state: enum
 }

 class Function {
   id: int
   code: string
   display_name: string
   state: enum
 }

 class AccessGroupFunction {
   access_group_id: int
   function_id: int
 }

 class ExceptionalPermission {
   id: int
   user_id: int
   function_id: int
   state: enum
   expires_at: timestamp
   granted_reason: string
 }

 User "1" -- "*" Assignment
 Assignment "*" -- "1" AccessGroup : (target_type=AGR)
 Assignment "*" -- "1" Function : (target_type=Function)
 AccessGroup "1" -- "*" AccessGroupFunction
 AccessGroupFunction "*" -- "1" Function
 User "1" -- "*" ExceptionalPermission
 ExceptionalPermission "*" -- "1" Function

 note right of Assignment
   3 fuentes de Function efectiva:
   1) Assignment (target=Function): direct
   2) Assignment (target=AGR) -> AGR.functions: via_agr
   3) ExceptionalPermission: exceptional
 end note

 @enduml
