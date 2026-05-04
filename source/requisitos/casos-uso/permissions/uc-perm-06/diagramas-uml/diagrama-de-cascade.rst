8.3 Diagrama de cascade
=======================

.. uml::
 :caption: Cascade — un cambio en AGR
           afecta N Users

 @startuml

 class AccessGroup {
   id, code, state
 }

 class AccessGroupFunction {
   access_group_id
   function_id
 }

 class Function {
   id, code
 }

 class Assignment {
   user_id
   target_type=AccessGroup
   target_id
 }

 class User {
   id, username
 }

 AccessGroup "1" -- "*" AccessGroupFunction : composicion
 AccessGroupFunction "*" -- "1" Function
 AccessGroup "1" -- "*" Assignment
 Assignment "*" -- "1" User

 note right of AccessGroupFunction
   UC_PERM_06 modifica esta tabla.
   Effect cascade sobre todos los Users
   con AGR via Assignment.
 end note

 @enduml

