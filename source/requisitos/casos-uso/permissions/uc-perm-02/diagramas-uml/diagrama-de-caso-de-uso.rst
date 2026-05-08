8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_02 — vista PERM de UC_ACC_02 (sobre AGR)

 @startuml

 left to right direction

 actor "revoke_function_group" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "PermissionCache" as PC <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar Grupo a Usuario\n(vista PERM)" as UC_PERM_02
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Assignment\n(target_type=AccessGroup)" as UC_ACC_02
   usecase "Validar revoke_reason\nobligatoria" as VALIDAR_REASON
   usecase "Validar Assignment\nactivo" as VALIDAR_ASSIGNMENT
   usecase "Idempotencia\n(state=REVOKED → no-op)" as IDEMP
   usecase "Transicionar Assignment\nstate=REVOKED" as PERSISTIR
   usecase "Invalidar PermissionCache" as CACHE_INV
   usecase "Emitir AuditEvent\nAGR_REVOKED" as AUDIT
 }

 INVOKER --> UC_PERM_02
 UC_PERM_02 ..> UC_ACC_02 : <<include>>
 UC_ACC_02 ..> VALIDAR_REASON : <<include>>
 UC_ACC_02 ..> VALIDAR_ASSIGNMENT : <<include>>
 UC_ACC_02 ..> IDEMP : <<include>>
 UC_ACC_02 ..> PERSISTIR : <<include>>
 UC_ACC_02 ..> CACHE_INV : <<include>>
 UC_ACC_02 ..> AUDIT : <<include>>

 CACHE_INV --> PC
 AUDIT --> AS
 AS --> view_audit_log
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

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   entidad Assignment cuya state transita ACTIVE → REVOKED.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio que persiste la transicion.
 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup target del Assignment.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada post-COMMIT.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent AGR_REVOKED.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-025).
 - :doc:`/requisitos/casos-uso/access/uc-acc-02/index` —
   UC backing (operacion completa).
