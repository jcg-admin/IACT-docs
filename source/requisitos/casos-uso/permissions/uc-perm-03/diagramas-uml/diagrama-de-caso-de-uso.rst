8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_03 — vista PERM de UC_ACC_08

 @startuml

 left to right direction

 actor "grant_exceptional_permission" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Cron expiracion" as CRON <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional (vista PERM)" as UC_PERM_03
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal" as UC_ACC_08
   usecase "Validar payload\n(justification + expires_at)" as VALIDAR_PAYLOAD
   usecase "Validar SoD\nwrite-time (CNST-005)" as VALIDAR_SOD
   usecase "Persistir\nExceptionalPermission" as PERSISTIR
   usecase "InternalMailbox\nOBLIGATORIO (P-10)" as MAILBOX
   usecase "AuditEvent\nEXCEPTIONAL_*_GRANTED" as AUDIT
   usecase "Vencimiento\nautomatico" as EXPIRY <<extend>>
 }

 INVOKER --> UC_PERM_03
 UC_PERM_03 ..> UC_ACC_08 : <<include>>
 UC_ACC_08 ..> VALIDAR_PAYLOAD : <<include>>
 UC_ACC_08 ..> VALIDAR_SOD : <<include>>
 UC_ACC_08 ..> PERSISTIR : <<include>>
 UC_ACC_08 ..> MAILBOX : <<include>>
 UC_ACC_08 ..> AUDIT : <<include>>
 EXPIRY ..> UC_ACC_08 : <<extend>>

 MAILBOX --> TARGET
 AUDIT --> view_audit_log
 CRON --> EXPIRY

 note bottom of UC_PERM_03
   ADR-GOB-008: vista PERM con audiencia
   governance/compliance.
   Funcion canonica grant_exceptional_permission
   distinta de assign_functions / assign_function_groups
   (P-15 RBAC granular).
 end note

 note bottom of MAILBOX
   Mailbox-or-abort HARD (P-10):
   sin notificacion al destino el
   grant no se completa.
 end note

 note bottom of EXPIRY
   BR-008: expires_at obligatorio
   (1h-30d). Cron remueve permiso
   al alcanzar vencimiento.
 end note

 @enduml
