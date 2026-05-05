8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "create_users" as ADMINISTRADOR_SISTEMA
 actor "Nuevo User" as USUARIO_AUTENTICADO <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UC_USR_01
   usecase "Generar username\n(CNST-029)" as GenerarDato
   usecase "Generar password\ntemporal" as GenerarPassword
   usecase "Asignar AGR\nopcional" as GrupoAcceso
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "AuditEvent\nUSER_CREATED" as AuditEmitter
 }

 ADMINISTRADOR_SISTEMA --> UC_USR_01
 UC_USR_01 ..> GEN : <<include>>
 UC_USR_01 ..> PWD : <<include>>
 UC_USR_01 ..> AGR : <<extend>>
 UC_USR_01 ..> NOT : <<include>>
 UC_USR_01 ..> EMI : <<include>>
 NOT --> USUARIO_AUTENTICADO : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

