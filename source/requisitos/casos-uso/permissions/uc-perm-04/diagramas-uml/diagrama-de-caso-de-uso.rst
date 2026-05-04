8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_04 — actores

 @startuml
 left to right direction

 actor "revoke_exceptional_permission" as INVOKER
 actor "User destino" as TARGET
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_04\nRevocar\nExceptional" as UC04
   usecase "actualizar state\nREVOKED" as UPD
   usecase "Notificar\nObligatorio" as NOT
   usecase "AuditEvent\nREVOKED" as EMI
 }

 INVOKER --> UC04
 UC04 ..> UPD : <<include>>
 UC04 ..> NOT : <<include>>
 UC04 ..> EMI : <<include>>
 NOT --> TARGET
 EMI --> view_audit_log

 note bottom of NOT
   Mailbox-or-abort HARD
 end note

 @enduml

