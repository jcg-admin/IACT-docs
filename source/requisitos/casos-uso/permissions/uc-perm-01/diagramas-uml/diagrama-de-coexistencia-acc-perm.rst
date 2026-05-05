8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_01 vs UC_ACC_04 — vistas
           del mismo flujo

 @startuml
 left to right direction

 actor "assign_function_groups" as assign_function_groups
 actor "assign_function_groups" as assign_function_groups

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR\n(desde User)" as UC_ACC_04
 }

 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo\n(desde catalogo AGR)" as PERM01
 }

 cloud "Backend compartido" {
   usecase "POST /api/users/\n{id}/access-groups/" as PostApiUsers
   note bottom: Funcion: assign_function_groups
 }

 assign_function_groups --> UC_ACC_04
 assign_function_groups --> PERM01
 UC_ACC_04 --> PostApiUsers : delega
 PERM01 --> PostApiUsers : delega

 note right of PostApiUsers
   Implementacion comun (UC_ACC_04 backing).
   AuditEvent AGR_ASSIGNED no distingue
   origen UI.
 end note

 @enduml

