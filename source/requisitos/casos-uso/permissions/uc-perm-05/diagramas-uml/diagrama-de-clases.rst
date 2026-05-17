8.4 Diagrama de clases
======================

.. uml::
 :caption: AccessGroup + relaciones

 @startuml

 class AccessGroup {
   id, code, display_name, description,
   severity, is_predefined, state,
   created_at, retired_at...
 }

 class AccessGroupFunction {
   access_group_id, function_id
 }

 class Function {
   id, code, display_name, state
 }

 class Assignment {
   user_id, target_type, target_id
 }

 AccessGroup "1" -- "*" AccessGroupFunction
 AccessGroupFunction "*" -- "1" Function
 AccessGroup "1" -- "*" Assignment

 note right of AccessGroupFunction
   UC_PERM_06 maneja esta tabla
   (composicion del AGR)
 end note

 @enduml
