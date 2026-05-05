.. meta::
 :artefacto: AT_UC_ACC_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_acc_02_revocar_funciones:

==============================
UC_ACC_02 — Revocar Funciones
==============================

Revoca ``Assignment`` activos del User (target_type=Function o
AccessGroup). ``state`` transita ACTIVE → REVOKED (BR-009 soft-delete).
Validacion LastHolderSpec previene orfandad de funciones criticas
(409 Conflict si el revoke deja sin holder a una funcion critica).

.. uml::
 :caption: UC_ACC_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "revoke_functions" as revoke_functions
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Funciones" as UC_ACC_02
   usecase "Verificar\nrevoke_functions" as VERIFICAR_AGR
   usecase "Validar revoke_reason\n(≥10)" as VALIDAR_REASON
   usecase "Validar Assignment\nactivo" as VALIDAR_ACTIVE
   usecase "Validar LastHolderSpec\n(funciones criticas)" as VALIDAR_LAST
   usecase "Idempotencia\n(REVOKED → no-op)" as IDEMP
   usecase "Transicionar\nstate=REVOKED" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Notificar destino" as NOTIFICAR
   usecase "Emitir AuditEvent\nFUNCTIONS_REVOKED" as AUDITAR
 }

 revoke_functions --> UC_ACC_02

 UC_ACC_02 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_02 ..> VALIDAR_REASON : <<include>>
 UC_ACC_02 ..> VALIDAR_ACTIVE : <<include>>
 UC_ACC_02 ..> VALIDAR_LAST : <<include>>
 UC_ACC_02 ..> IDEMP : <<include>>
 UC_ACC_02 ..> PERSISTIR : <<include>>
 UC_ACC_02 ..> RECALC : <<include>>
 UC_ACC_02 ..> INVALIDAR : <<include>>
 UC_ACC_02 ..> NOTIFICAR : <<include>>
 UC_ACC_02 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_LAST --> RuleValidator
 PERSISTIR --> AssignmentRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 NOTIFICAR --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_LAST
   LastHolderSpec: bloquea revoke
   si User es ultimo holder de
   funcion critica. Devuelve 409.
 end note

 note bottom of PERSISTIR
   BR-009 soft-delete: state=REVOKED.
   Historial preservado.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   entity con state=REVOKED.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   LastHolderSpec, ActiveAssignmentSpec.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta specs.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica destino.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica revoke_functions.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor FUNCTIONS_REVOKED.
 - :doc:`/requisitos/casos-uso/access/uc-acc-02/index` —
   spec textual.
