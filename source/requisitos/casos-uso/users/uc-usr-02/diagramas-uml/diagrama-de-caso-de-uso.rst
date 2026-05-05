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
   usecase "Listar (paginado)" as VistaListado
   usecase "Ver detalle" as VistaDetalle
   usecase "Audit selectivo\n(P-16)" as AUDITORIA_SELECTIVA
 }

 INVOKER --> UC02
 UC02 ..> LST : <<extend>>
 UC02 ..> DET : <<extend>>
 LST ..> AUDITORIA_SELECTIVA : <<extend (filter user_id)>>
 DET ..> AUDITORIA_SELECTIVA : <<include>>
 AUDITORIA_SELECTIVA --> view_audit_log

 note bottom of LST
   list_users (RBAC)
 end note
 note bottom of DET
   view_users (RBAC distinto)
 end note

 @enduml

