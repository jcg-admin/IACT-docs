8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_02 — vista de actores y casos asociados

 @startuml

 left to right direction

 actor "User" as USER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_02\nCerrar Sesion" as UC02
   usecase "Validar token" as VTK
   usecase "Cerrar Session" as CSE
   usecase "Blacklist tokens" as BLK
   usecase "Emitir AuditEvent\nLOGOUT" as EMI
 }

 USER --> UC02
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

