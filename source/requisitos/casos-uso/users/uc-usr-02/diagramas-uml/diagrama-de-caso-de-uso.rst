8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_users" as INVOKER
 actor "User consultado" as TARGET <<pasivo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Users" {
   usecase "UC_USR_02\nConsultar Usuarios" as UC02
   usecase "Listar (paginado)" as LST
   usecase "Ver detalle" as DET
   usecase "Audit selectivo\n(P-16)" as AUDS
 }

 INVOKER --> UC02
 UC02 ..> LST : <<extend>>
 UC02 ..> DET : <<extend>>
 LST ..> AUDS : <<extend (filter user_id)>>
 DET ..> AUDS : <<include>>
 AUDS --> view_audit_log

 note bottom of LST
   list_users (RBAC)
 end note
 note bottom of DET
   view_users (RBAC distinto)
 end note

 @enduml

