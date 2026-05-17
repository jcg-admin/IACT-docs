8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_08 — actores y casos asociados

 @startuml
 left to right direction

 actor "grant_exceptional_permission" as INVOKER
 actor "User destino" as TARGET
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal" as UC_ACC_08
   usecase "Validar payload\n(justification +\nexpires_at bounds)" as VistaPipeline
   usecase "Validar separacion\nwrite-time" as VALIDAR_SEPARATION_RULES
   usecase "registrar\nExceptionalPermissions" as RegistrarDatos
   usecase "Notificar via\nInternalMailbox\n(OBLIGATORIO)" as NotificacionMailbox
   usecase "AuditEvent\nGRANTED reforzado" as AuditEmitter
 }

 INVOKER --> UC_ACC_08
 UC_ACC_08 ..> VPL : <<include>>
 UC_ACC_08 ..> VALIDAR_SEPARATION_RULES : <<include>>
 UC_ACC_08 ..> INS : <<include>>
 UC_ACC_08 ..> NOT : <<include>>
 UC_ACC_08 ..> EMI : <<include>>
 NOT --> TARGET
 EMI --> view_audit_log

 note bottom of NOT
   Mailbox-or-abort HARD
   (P-10) — sin notificacion
   no se completa
 end note
 note bottom of UC_ACC_08
   Trazabilidad reforzada:
   justification + expires_at
   + ticket_reference
 end note

 @enduml

