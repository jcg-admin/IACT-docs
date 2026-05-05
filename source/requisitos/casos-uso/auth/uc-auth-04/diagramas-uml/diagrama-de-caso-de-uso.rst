8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "User\nautenticado" as USUARIO_AUTENTICADO
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_04\nCambiar Contrasena" as UC04
   usecase "Validar password\nactual" as ValidarDato
   usecase "Validar complejidad" as VALIDAR_COMPLEJIDAD
   usecase "Verificar historial\n(no reuso)" as HISTORICO_IVR
   usecase "Cerrar otras\nSessions" as CerrarSesiones
   usecase "Emitir AuditEvent\nPASSWORD_CHANGED" as AuditEmitter
 }

 USUARIO_AUTENTICADO --> UC04
 UC04 ..> VAL : <<include>>
 UC04 ..> VALIDAR_COMPLEJIDAD : <<include>>
 UC04 ..> HISTORICO_IVR : <<include>>
 UC04 ..> CSE : <<include>>
 UC04 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of HISTORICO_IVR
   N=5 ultimas hashes (BR-AUTH-32)
 end note

 @enduml

