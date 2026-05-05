8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_02 — vista de actores y casos asociados

 @startuml

 left to right direction

 actor "User" as USUARIO_AUTENTICADO
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_02\nCerrar Sesion" as UC02
   usecase "Validar token" as VistaToken
   usecase "Cerrar Session" as CerrarSesiones
   usecase "Blacklist tokens" as TokensRevocados
   usecase "Emitir AuditEvent\nLOGOUT" as AuditEmitter
 }

 USUARIO_AUTENTICADO --> UC02
 UC02 ..> VTK : <<include>>
 UC02 ..> CSE : <<include>>
 UC02 ..> BLK : <<include>>
 UC02 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log : (consume\nUC_AUD_*)

 note bottom of UC02
   CNST-009 autenticacion
   CNST-013 manejo estandar
   CNST-025 auditoria inmutable
 end note

 @enduml

