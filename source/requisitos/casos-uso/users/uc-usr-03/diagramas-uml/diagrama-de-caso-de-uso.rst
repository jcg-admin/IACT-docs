8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "update_users" as ADMINISTRADOR_SISTEMA
 actor "User modificado" as USUARIO_AUTENTICADO <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_03\nModificar Usuario" as UC_USR_03
   usecase "Validar transicion\nde state" as ValidarTransicion
   usecase "Validar email\nunico" as ValidarEmail
   usecase "actualizar User\nparcial" as ActualizarEntidad
   usecase "Cerrar Sessions\nactivas" as CerrarSesiones
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "AuditEvent\nUSER_MODIFIED" as AuditEmitter
 }

 ADMINISTRADOR_SISTEMA --> UC_USR_03
 UC_USR_03 ..> ValidarTransicion : <<include>>
 UC_USR_03 ..> ValidarEmail : <<extend (si email cambia)>>
 UC_USR_03 ..> UPD : <<include>>
 UC_USR_03 ..> CSE : <<extend (si state→BLOCKED)>>
 UC_USR_03 ..> NOT : <<extend (politica)>>
 UC_USR_03 ..> EMI : <<include>>
 NOT --> USUARIO_AUTENTICADO
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of ValidarTransicion
   P-11 anti-self-state-change
 end note
 note bottom of CSE
   side-effect: invalida tokens activos
 end note

 @enduml

