8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "User\nautenticado" as USER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_04\nCambiar Contrasena" as UC04
   usecase "Validar password\nactual" as ValidarDato
   usecase "Validar complejidad" as COMP
   usecase "Verificar historial\n(no reuso)" as HIST
   usecase "Cerrar otras\nSessions" as CerrarSesiones
   usecase "Emitir AuditEvent\nPASSWORD_CHANGED" as AuditEmitter
 }

 USER --> UC04
 UC04 ..> VAL : <<include>>
 UC04 ..> COMP : <<include>>
 UC04 ..> HIST : <<include>>
 UC04 ..> CSE : <<include>>
 UC04 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of HIST
   N=5 ultimas hashes (BR-AUTH-32)
 end note

 @enduml

