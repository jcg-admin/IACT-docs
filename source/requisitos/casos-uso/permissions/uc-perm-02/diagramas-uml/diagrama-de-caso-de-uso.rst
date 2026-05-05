8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_02 — vista PERM de UC_ACC_02 (sobre AGR)

 @startuml

 left to right direction

 actor "revoke_function_group" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar Grupo a Usuario\n(vista PERM)" as UC_PERM_02
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Assignment\n(target_type=AGR)" as UC_ACC_02
   usecase "Validar revoke_reason\nobligatoria" as VALIDAR_REASON
   usecase "Validar Assignment\nactivo" as VALIDAR_ASSIGNMENT
   usecase "Idempotencia\n(state=REVOKED → no-op)" as IDEMP
   usecase "Transicionar\nstate=REVOKED" as PERSISTIR
   usecase "Invalidar cache\npermisos" as CACHE_PERMISOS
   usecase "AuditEvent\nAGR_REVOKED" as AUDIT
 }

 INVOKER --> UC_PERM_02
 UC_PERM_02 ..> UC_ACC_02 : <<include>>
 UC_ACC_02 ..> VALIDAR_REASON : <<include>>
 UC_ACC_02 ..> VALIDAR_ASSIGNMENT : <<include>>
 UC_ACC_02 ..> IDEMP : <<include>>
 UC_ACC_02 ..> PERSISTIR : <<include>>
 UC_ACC_02 ..> CACHE_PERMISOS : <<include>>
 UC_ACC_02 ..> AUDIT : <<include>>

 AUDIT --> view_audit_log
 PERSISTIR --> TARGET

 note bottom of UC_PERM_02
   ADR-GOB-008: vista PERM con audiencia
   governance/compliance. P-15 RBAC granular —
   revoke_function_group es funcion canonica
   distinta de assign_function_groups, aunque
   ambas operan sobre el mismo Assignment.
 end note

 note bottom of PERSISTIR
   BR-009 soft-delete: Assignment
   transita ACTIVE → REVOKED, no DELETE.
   Historial preservado para auditoria.
 end note

 @enduml
