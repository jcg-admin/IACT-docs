8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "deactivate_users" as INVOKER
 actor "User eliminado" as USUARIO_AUTENTICADO <<receptor>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as UC_USR_04
   usecase "Validar P-11\nanti-self-elimination" as VALIDAR_ANTI_SELF
   usecase "Transitar User\na ELIMINATED" as EliminarEntidad
   usecase "Revocar\nAssignments" as RevocarAsignacion
   usecase "Cerrar Sessions\n+ blacklist tokens" as CerrarSesiones
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "AuditEvent\nUSER_ELIMINATED" as AuditEmitter
 }

 INVOKER --> UC_USR_04
 UC_USR_04 ..> VALIDAR_ANTI_SELF : <<include>>
 UC_USR_04 ..> ELI : <<include>>
 UC_USR_04 ..> REV : <<include>>
 UC_USR_04 ..> CSE : <<include>>
 UC_USR_04 ..> NOT : <<extend (politica notify)>>
 UC_USR_04 ..> EMI : <<include>>
 NOT --> USUARIO_AUTENTICADO
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of ELI
   BR-009: baja LOGICA, no DELETE fisico
 end note
 note bottom of VALIDAR_ANTI_SELF
   admin no puede auto-eliminarse
 end note

 @enduml

