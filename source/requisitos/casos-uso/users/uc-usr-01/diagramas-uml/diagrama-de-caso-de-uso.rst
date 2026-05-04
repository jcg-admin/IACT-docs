8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "create_users" as ADMIN
 actor "Nuevo User" as USER <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UC01
   usecase "Generar username\n(CNST-029)" as GEN
   usecase "Generar password\ntemporal" as PWD
   usecase "Asignar AGR\nopcional" as AGR
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "AuditEvent\nUSER_CREATED" as EMI
 }

 ADMIN --> UC01
 UC01 ..> GEN : <<include>>
 UC01 ..> PWD : <<include>>
 UC01 ..> AGR : <<extend>>
 UC01 ..> NOT : <<include>>
 UC01 ..> EMI : <<include>>
 NOT --> USER : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

