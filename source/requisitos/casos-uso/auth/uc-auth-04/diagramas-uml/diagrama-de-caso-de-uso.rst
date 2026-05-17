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
   usecase "UC_AUTH_04\nCambiar Contrasena" as UC_AUTH_04
   usecase "Validar password\nactual" as ValidarDato
   usecase "Validar complejidad" as VALIDAR_COMPLEJIDAD
   usecase "Verificar historial\n(no reuso)" as HISTORICO_IVR
   usecase "Cerrar otras\nSessions" as CerrarSesiones
   usecase "Emitir AuditEvent\nPASSWORD_CHANGED" as AuditEmitter
 }

 USUARIO_AUTENTICADO --> UC_AUTH_04
 UC_AUTH_04 ..> VAL : <<include>>
 UC_AUTH_04 ..> VALIDAR_COMPLEJIDAD : <<include>>
 UC_AUTH_04 ..> HISTORICO_IVR : <<include>>
 UC_AUTH_04 ..> CSE : <<include>>
 UC_AUTH_04 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of HISTORICO_IVR
   N=5 ultimas hashes (BR-AUTH-32)
 end note

 @enduml

