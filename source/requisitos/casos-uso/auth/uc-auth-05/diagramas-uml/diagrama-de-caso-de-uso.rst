8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_all_active_sessions" as ADMINISTRADOR_SISTEMA
 actor "User afectado" as USUARIO_AUTENTICADO <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_05\nGestionar Sesiones" as UC05
   usecase "Listar Sessions" as VistaListado
   usecase "Cerrar Session\nindividual" as CerrarSession
   usecase "Cerrar todas\nlas del User" as CERRAR_SESIONES_USUARIO
   usecase "Notificar\n(opcional)" as NotificacionMailbox
   usecase "AuditEvent\nSESSION_CLOSED" as AuditEmitter
 }

 ADMINISTRADOR_SISTEMA --> UC05
 UC05 ..> LST : <<extend>>
 UC05 ..> CerrarSession : <<extend>>
 UC05 ..> CERRAR_SESIONES_USUARIO : <<extend>>
 CerrarSession ..> EMI : <<include>>
 CERRAR_SESIONES_USUARIO ..> EMI : <<include>>
 CerrarSession ..> NOT : <<extend>>
 CERRAR_SESIONES_USUARIO ..> NOT : <<extend>>
 NOT --> USUARIO_AUTENTICADO
 Sistema --> EMI
 EMI --> view_audit_log

 @enduml

