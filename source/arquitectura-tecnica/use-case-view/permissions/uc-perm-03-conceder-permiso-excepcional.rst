.. meta::
 :artefacto: AT_UC_PERM_03_USECASE
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

.. _at_uc_perm_03_conceder_permiso_excepcional:

============================================================
UC_PERM_03 — Conceder Permiso Excepcional (vista PERM)
============================================================

Vista PERM (governance) del grant de permisos excepcionales. Otorga
funciones temporales con ``expires_at`` y ``justification`` obligatorios.
``grant_exceptional_permission`` distinta de assign_functions /
assign_function_groups (P-15). Mailbox-or-abort HARD (P-10):
sin notificacion al destino el grant no se completa.

.. uml::
 :caption: UC_PERM_03 — vista PERM de UC_ACC_08 (permiso temporal).

 @startuml

 left to right direction

 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExceptionalPermissionRepo" as ExceptionalPermissionRepo <<sistema>>
 actor "ExpirationPolicy" as ExpirationPolicy <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>
 actor "Planificador expiracion" as Planificador_expiracion <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional (vista PERM)" as UC_PERM_03
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal\n.. extension points ..\nVencimientoAuto" as UC_ACC_08
   usecase "Verificar\ngrant_exceptional_permission" as VERIFICAR_AGR
   usecase "Validar payload\n(justification ≥20\n+ expires_at bounds)" as VALIDAR_PAYLOAD
   usecase "Validar SoD write-time\n(CNST-005)" as VALIDAR_SOD
   usecase "Persistir\nExceptionalPermission" as PERSISTIR
   usecase "Recompute effective_set\n(source=EXCEPTIONAL)" as RECALC
   usecase "InternalMailbox\nOBLIGATORIO (P-10)" as MAILBOX
   usecase "Emitir AuditEvent\nEXCEPTIONAL_*_GRANTED\n(P-39 reforzado)" as AUDITAR
   usecase "Vencimiento automatico" as EXPIRY
 }

 grant_exceptional_permission --> UC_PERM_03

 UC_PERM_03 ..> UC_ACC_08 : <<include>>
 UC_ACC_08 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_08 ..> VALIDAR_PAYLOAD : <<include>>
 UC_ACC_08 ..> VALIDAR_SOD : <<include>>
 UC_ACC_08 ..> PERSISTIR : <<include>>
 UC_ACC_08 ..> RECALC : <<include>>
 UC_ACC_08 ..> MAILBOX : <<include>>
 UC_ACC_08 ..> AUDITAR : <<include>>
 EXPIRY ..> UC_ACC_08 : <<extend>> (VencimientoAuto)

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_PAYLOAD --> ExpirationPolicy
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> ExceptionalPermissionRepo
 RECALC --> EffectivePermissionsAggregator
 MAILBOX --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log
 Planificador_expiracion --> EXPIRY

 note bottom of UC_PERM_03
   ADR-GOB-008: vista PERM con audiencia
   governance/compliance. Funcion canonica
   grant_exceptional_permission distinta
   de assign_functions / assign_function_groups.
 end note

 note bottom of MAILBOX
   Mailbox-or-abort HARD (P-10):
   sin notificacion al destino, el
   grant no se completa.
 end note

 note bottom of EXPIRY
   BR-008: expires_at obligatorio
   (1h-30d). Planificador consume
   ExpirationPolicy.find_expiring_in
   y remueve permiso al vencer.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
   entidad persistida.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   repositorio (find_active_grant, find_expiring_in para
   el Planificador de Tareas).
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy` —
   bounds + deteccion vencimiento.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD evaluadas.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta SoD write-time.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   P-10 mailbox-or-abort HARD.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item de notificacion al destino.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute con source=EXCEPTIONAL.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada al grant y al expiry.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica grant_exceptional_permission.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor EXCEPTIONAL_*_GRANTED (P-39 reforzado).
 - :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
   UC backing.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index` —
   spec textual.
