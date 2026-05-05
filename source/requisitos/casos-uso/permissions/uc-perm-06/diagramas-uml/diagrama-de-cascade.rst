8.3 Diagrama de cascade
=======================

.. uml::
 :caption: Cascade — un cambio en AGR
           afecta N Users

 @startuml

 class AccessGroup {
   agr_id : String
   name : String
 }

 class FunctionGroup {
   group_id : UUID
   name : String
   --
   create_function_group()
   assign_functions()
 }

 class Function {
   name : String
   module : Module
 }

 class Assignment {
   assignment_id : UUID
   user_id : UUID
   group_ref : String
   state : AssignmentState
 }

 class User {
   user_id : UUID
   username : String
 }

 AccessGroup "1" -- "*" FunctionGroup : agrupa
 FunctionGroup "*" -- "*" Function : contiene
 AccessGroup "1" -- "*" Assignment : asignada via
 Assignment "*" -- "1" User

 note right of FunctionGroup
   UC_PERM_06 modifica FunctionGroup→Function.
   AccessGroup agrupa FunctionGroups.
   Cascade: cambio en FunctionGroup afecta
   todos los Users con ese AccessGroup via Assignment.
   No existe AccessGroupFunction como clase de dominio.
 end note

 @enduml

