.. meta::
 :artefacto: AT_UC_PERM_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_perm_02_revocar_grupo_a_usuario:

============================================================
UC_PERM_02 — Revocar Grupo a Usuario (vista PERM)
============================================================

Vista PERM (governance) del revoke de AccessGroup. ``Assignment.state``
transita ACTIVE → REVOKED preservando historial (BR-009 soft-delete).
P-15 RBAC granular: ``revoke_function_group`` distinta de
``assign_function_groups``. ADR-GOB-008.

.. uml::
 :caption: UC_PERM_02 — vista PERM de UC_ACC_02 (sobre AccessGroup).

 @startuml

 left to right direction

 actor "revoke_function_group" as revoke_function_group
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar Grupo a Usuario\n(vista PERM)" as UC_PERM_02
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Assignment\n(target=AccessGroup)" as UC_ACC_02
   usecase "Verificar\nrevoke_function_group" as VERIFICAR_AGR
   usecase "Validar revoke_reason\nobligatoria (≥10)" as VALIDAR_REASON
   usecase "Validar Assignment activo" as VALIDAR_ASSIGNMENT
   usecase "Idempotencia\n(REVOKED → no-op)" as IDEMP
   usecase "Transicionar\nstate=REVOKED" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nAGR_REVOKED" as AUDITAR
 }

 revoke_function_group --> UC_PERM_02

 UC_PERM_02 ..> UC_ACC_02 : <<include>>
 UC_ACC_02 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_02 ..> VALIDAR_REASON : <<include>>
 UC_ACC_02 ..> VALIDAR_ASSIGNMENT : <<include>>
 UC_ACC_02 ..> IDEMP : <<include>>
 UC_ACC_02 ..> PERSISTIR : <<include>>
 UC_ACC_02 ..> RECALC : <<include>>
 UC_ACC_02 ..> INVALIDAR : <<include>>
 UC_ACC_02 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 PERSISTIR --> AssignmentRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 PERSISTIR --> User_destino
 AuditService --> view_audit_log

 note bottom of PERSISTIR
   BR-009 soft-delete: state=REVOKED,
   no DELETE. Historial preservado
   para auditoria.
 end note

 note bottom of UC_PERM_02
   ADR-GOB-008: vista PERM con audiencia
   governance/compliance. P-15 — funcion
   distinta de assign_function_groups
   aunque ambas operan sobre Assignment.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   Assignment con state=ACTIVE → REVOKED.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup target.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica revoke_function_group.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AGR_REVOKED.
 - :doc:`/requisitos/casos-uso/access/uc-acc-02/index` —
   UC backing.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-02/index` —
   spec textual.
