.. meta::
 :artefacto: AT_UC_ACC_08_USECASE
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

.. _at_uc_acc_08_permiso_temporal:

==============================
UC_ACC_08 — Permiso Temporal
==============================

Otorga ``ExceptionalPermission`` con ``expires_at`` y ``justification``
obligatorios. Mailbox-or-abort HARD (P-10): sin notificacion al destino,
el grant no se completa. UC_PERM_03 es la vista PERM (governance) que
incluye este UC. Cron de expiracion remueve permisos vencidos.

.. uml::
 :caption: UC_ACC_08 — actores y casos asociados.

 @startuml

 left to right direction

 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Cron expiracion" as Cron_expiracion <<sistema_externo>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExceptionalPermissionRepo" as ExceptionalPermissionRepo <<sistema>>
 actor "ExpirationPolicy" as ExpirationPolicy <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal\n.. extension points ..\nVencimientoAuto" as UC_ACC_08
   usecase "Verificar\ngrant_exceptional_permission" as VERIFICAR_AGR
   usecase "Validar payload\n(justification ≥20\n+ expires_at bounds)" as VALIDAR_PAYLOAD
   usecase "Validar SoD write-time" as VALIDAR_SOD
   usecase "Persistir\nExceptionalPermission" as PERSISTIR
   usecase "Recompute effective_set\n(source=EXCEPTIONAL)" as RECALC
   usecase "InternalMailbox\nOBLIGATORIO (P-10)" as MAILBOX
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nEXCEPTIONAL_*_GRANTED\n(P-39 reforzado)" as AUDITAR
   usecase "Vencimiento automatico\n(cron find_expiring_in)" as EXPIRY
 }

 grant_exceptional_permission --> UC_ACC_08

 UC_ACC_08 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_08 ..> VALIDAR_PAYLOAD : <<include>>
 UC_ACC_08 ..> VALIDAR_SOD : <<include>>
 UC_ACC_08 ..> PERSISTIR : <<include>>
 UC_ACC_08 ..> RECALC : <<include>>
 UC_ACC_08 ..> MAILBOX : <<include>>
 UC_ACC_08 ..> INVALIDAR : <<include>>
 UC_ACC_08 ..> AUDITAR : <<include>>
 EXPIRY ..> UC_ACC_08 : <<extend>> (VencimientoAuto)

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_PAYLOAD --> ExpirationPolicy
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> ExceptionalPermissionRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 MAILBOX --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log
 Cron_expiracion --> EXPIRY

 note bottom of MAILBOX
   P-10 mailbox-or-abort HARD: sin
   notificacion al destino, el grant
   se aborta y rolling-back.
 end note

 note bottom of EXPIRY
   BR-008: expires_at obligatorio
   (1h-30d). Cron consume
   ExpirationPolicy.find_expiring_in
   y remueve permiso al vencer
   + audit EXCEPTIONAL_EXPIRED.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
   entidad persistida.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   repositorio (find_active_grant, find_expiring_in).
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy` —
   bounds + deteccion vencimiento.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta SoD write-time.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   P-10 mailbox-or-abort.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item de notificacion.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute con source=EXCEPTIONAL.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica grant_exceptional_permission.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (P-39 reforzado).
 - :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
   spec textual.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index` —
   vista PERM.
