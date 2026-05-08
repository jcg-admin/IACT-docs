.. meta::
 :artefacto: AT_UC_PERM_04_USECASE
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

.. _at_uc_perm_04_revocar_permiso_excepcional:

==============================================
UC_PERM_04 — Revocar Permiso Excepcional
==============================================

Revoca un ExceptionalPermission antes de ``expires_at`` (revocacion
forzada). ``Assignment.state`` transita ACTIVE → REVOKED. Mailbox
notifica al destino. Audit reforzado P-39.

.. uml::
 :caption: UC_PERM_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "revoke_exceptional_permission" as revoke_exceptional_permission
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExceptionalPermissionRepo" as ExceptionalPermissionRepo <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_04\nRevocar Permiso\nExcepcional" as UC_PERM_04
   usecase "Verificar\nrevoke_exceptional_permission" as VERIFICAR_AGR
   usecase "Validar reason\n(≥10 chars)" as VALIDAR_REASON
   usecase "Validar permiso activo" as VALIDAR_ACTIVE
   usecase "Idempotencia\n(REVOKED → no-op)" as IDEMP
   usecase "Transicionar\nstate=REVOKED" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Notificar via\nInternalMailbox" as MAILBOX
   usecase "Emitir AuditEvent\nEXCEPTIONAL_*_REVOKED\n(P-39)" as AUDITAR
 }

 revoke_exceptional_permission --> UC_PERM_04

 UC_PERM_04 ..> VERIFICAR_AGR : <<include>>
 UC_PERM_04 ..> VALIDAR_REASON : <<include>>
 UC_PERM_04 ..> VALIDAR_ACTIVE : <<include>>
 UC_PERM_04 ..> IDEMP : <<include>>
 UC_PERM_04 ..> PERSISTIR : <<include>>
 UC_PERM_04 ..> RECALC : <<include>>
 UC_PERM_04 ..> INVALIDAR : <<include>>
 UC_PERM_04 ..> MAILBOX : <<include>>
 UC_PERM_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 PERSISTIR --> ExceptionalPermissionRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 MAILBOX --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of PERSISTIR
   BR-009 soft-delete: state=REVOKED.
   Reason obligatoria para auditoria.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
   entity revocada.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica destino.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica revoke_exceptional_permission.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (P-39 reforzado).
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-04/index` —
   spec textual.
