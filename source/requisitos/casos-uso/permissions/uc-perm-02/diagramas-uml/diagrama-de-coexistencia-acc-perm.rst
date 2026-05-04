8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_02 vista del flujo
           UC_ACC_02 sobre AGR

 @startuml
 left to right direction

 actor "revoke_function_group" as revoke_function_group
 actor "revoke_function_group" as revoke_function_group

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_02\nRevocar\n(generico)" as ACC02
 }
 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar AGR\n(catalogo)" as PERM02
 }
 cloud "Backend compartido" {
   usecase "DELETE /api/users/{id}/\naccess-groups/{agr_id}/" as DeleteApiUsersId
 }

 revoke_function_group --> ACC02
 revoke_function_group --> PERM02
 ACC02 --> DeleteApiUsersId : delega
 PERM02 --> DeleteApiUsersId : delega

 note right of DeleteApiUsersId
   Funcion: revoke_function_group
   AuditEvent: AGR_REVOKED
 end note

 @enduml

