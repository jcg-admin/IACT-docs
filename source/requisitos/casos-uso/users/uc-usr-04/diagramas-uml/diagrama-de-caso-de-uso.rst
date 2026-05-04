8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "deactivate_users" as INVOKER
 actor "User eliminado" as USER <<receptor>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as UC04
   usecase "Validar P-11\nanti-self-elimination" as P11
   usecase "Transitar User\na ELIMINATED" as ELI
   usecase "Revocar\nAssignments" as REV
   usecase "Cerrar Sessions\n+ blacklist tokens" as CSE
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "AuditEvent\nUSER_ELIMINATED" as EMI
 }

 INVOKER --> UC04
 UC04 ..> P11 : <<include>>
 UC04 ..> ELI : <<include>>
 UC04 ..> REV : <<include>>
 UC04 ..> CSE : <<include>>
 UC04 ..> NOT : <<extend (politica notify)>>
 UC04 ..> EMI : <<include>>
 NOT --> USER
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of ELI
   BR-009: baja LOGICA, no DELETE fisico
 end note
 note bottom of P11
   admin no puede auto-eliminarse
 end note

 @enduml

