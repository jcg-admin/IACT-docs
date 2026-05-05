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
 actor "InternalMailbox" as MB <<sistema>>
 actor "RuleValidator" as RV <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional (vista PERM)" as UC_PERM_03
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal" as UC_ACC_08
   usecase "Validar payload\n(justification + expires_at)" as VALIDAR_PAYLOAD
   usecase "Validar SoD\nwrite-time (CNST-005)" as VALIDAR_SOD
   usecase "Persistir\nExceptionalPermission" as PERSISTIR
   usecase "Notificar via\nInternalMailbox (P-10)" as MAILBOX
   usecase "Emitir AuditEvent\nEXCEPTIONAL_*_GRANTED" as AUDIT
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

 VALIDAR_SOD --> RV
 MAILBOX --> MB
 MB --> TARGET
 AUDIT --> AS
 AS --> view_audit_log
 CRON --> EXPIRY

 note bottom of UC_PERM_03
   ADR-GOB-008: vista PERM con audiencia
   governance/compliance. Funcion canonica
   grant_exceptional_permission distinta de
   assign_functions / assign_function_groups
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

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
   entidad ExceptionalPermission persistida (con expires_at).
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   repositorio (find_active_grant, find_expiring_in para cron).
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD evaluadas en VALIDAR_SOD (CNST-005).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que ejecuta validacion SoD write-time.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   MailboxService (P-10 mailbox-or-abort HARD).
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada al grant y al expiry.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent EXCEPTIONAL_*_GRANTED (P-39 reforzado).
 - :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
   UC backing (operacion completa).
