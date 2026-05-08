8.4 Diagrama AGR como agregacion
================================

.. uml::
 :caption: AGR contiene funciones — UC_ACC_04 asigna el AGR

 @startuml

 class User {
   id, username
 }

 class Assignment {
   id, user_id
   target_type: AccessGroup
   target_id: int (= agr.id)
   state, granted_at,
   expires_at?
 }

 class AccessGroup {
   id, code, display_name
   state
 }

 class AccessGroupFunction {
   access_group_id
   function_id
 }

 class Function {
   id, code, display_name
 }

 User "1" --> "*" Assignment
 Assignment "*" --> "1" AccessGroup : (target=AGR)
 AccessGroup "1" -- "*" AccessGroupFunction
 AccessGroupFunction "*" -- "1" Function

 note right of Assignment
   UC_ACC_04 crea ESTE Assignment
   con target_type='AccessGroup'
 end note

 note right of AccessGroupFunction
   UC_PERM_06 manipula esta tabla
   (composicion del AGR)
 end note

 @enduml
