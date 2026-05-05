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
   usecase "UC_PERM_04\nRevocar\nExceptional" as UC_PERM_04
   usecase "actualizar state\nREVOKED" as ActualizarEntidad
   usecase "Notificar\nObligatorio" as NotificacionMailbox
   usecase "AuditEvent\nREVOKED" as AuditEmitter
 }

 INVOKER --> UC_PERM_04
 UC_PERM_04 ..> UPD : <<include>>
 UC_PERM_04 ..> NOT : <<include>>
 UC_PERM_04 ..> EMI : <<include>>
 NOT --> TARGET
 EMI --> view_audit_log

 note bottom of NOT
   Mailbox-or-abort HARD
 end note

 @enduml

