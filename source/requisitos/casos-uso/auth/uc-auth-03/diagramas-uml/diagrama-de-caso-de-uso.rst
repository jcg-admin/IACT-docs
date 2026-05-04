8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "reset_password" as ADMIN
 actor "User afectado" as USER <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_03\nRecuperar Contrasena" as UC03
   usecase "Generar password\ntemporal" as GEN
   usecase "Cerrar Sessions\ndel User" as CSE
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "Emitir AuditEvent\nPASSWORD_RESET" as EMI
 }

 ADMIN --> UC03
 UC03 ..> GEN : <<include>>
 UC03 ..> CSE : <<include>>
 UC03 ..> NOT : <<include>>
 UC03 ..> EMI : <<include>>
 NOT --> USER : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log : (consume\nUC_AUD_*)

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

