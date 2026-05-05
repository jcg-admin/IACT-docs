8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "reset_password" as ADMINISTRADOR_SISTEMA
 actor "User afectado" as USUARIO_AUTENTICADO <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_03\nRecuperar Contrasena" as UC_AUTH_03
   usecase "Generar password\ntemporal" as GenerarDato
   usecase "Cerrar Sessions\ndel User" as CerrarSesiones
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "Emitir AuditEvent\nPASSWORD_RESET" as AuditEmitter
 }

 ADMINISTRADOR_SISTEMA --> UC_AUTH_03
 UC_AUTH_03 ..> GEN : <<include>>
 UC_AUTH_03 ..> CSE : <<include>>
 UC_AUTH_03 ..> NOT : <<include>>
 UC_AUTH_03 ..> EMI : <<include>>
 NOT --> USUARIO_AUTENTICADO : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log : (consume\nUC_AUD_*)

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

