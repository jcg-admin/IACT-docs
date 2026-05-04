8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "deactivate_users" as INVOKER
 actor "User eliminado" as USER <<receptor>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as UC04
   usecase "Validar P-11\nanti-self-elimination" as VALIDAR_ANTI_SELF
   usecase "Transitar User\na ELIMINATED" as EliminarEntidad
   usecase "Revocar\nAssignments" as RevocarAsignacion
   usecase "Cerrar Sessions\n+ blacklist tokens" as CerrarSesiones
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "AuditEvent\nUSER_ELIMINATED" as AuditEmitter
 }

 INVOKER --> UC04
 UC04 ..> VALIDAR_ANTI_SELF : <<include>>
 UC04 ..> ELI : <<include>>
 UC04 ..> REV : <<include>>
 UC04 ..> CSE : <<include>>
 UC04 ..> NOT : <<extend (politica notify)>>
 UC04 ..> EMI : <<include>>
 NOT --> USER
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of ELI
   BR-009: baja LOGICA, no DELETE fisico
 end note
 note bottom of VALIDAR_ANTI_SELF
   admin no puede auto-eliminarse
 end note

 @enduml

