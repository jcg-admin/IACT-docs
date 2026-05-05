.. meta::
 :artefacto: AT_UC_ACC_04_USECASE
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

.. _at_uc_acc_04_asignar_agrupador:

==============================
UC_ACC_04 — Asignar Agrupador
==============================

Asigna un ``AccessGroup`` (AGR-001..012 del sistema o custom) a un User
via ``Assignment.target_type=AccessGroup``. Validacion SoD se evalua
sobre las **funciones expandidas** del AGR (CNST-005). UC_PERM_01 es
la vista PERM (governance) que incluye este UC.

.. uml::
 :caption: UC_ACC_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "assign_function_groups" as assign_function_groups
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AccessGroupRepo" as AccessGroupRepo <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AccessGroup" as UC_ACC_04
   usecase "Verificar\nassign_function_groups" as VERIFICAR_AGR
   usecase "Validar AccessGroup\nexiste + ACTIVE" as VALIDAR_AGR_ENTITY
   usecase "Expandir funciones\ndel AccessGroup" as EXPANDIR
   usecase "Validar SoD\nsobre set efectivo" as VALIDAR_SOD
   usecase "Persistir Assignment\n(target=AccessGroup)" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Notificar destino" as NOTIFICAR
   usecase "Emitir AuditEvent\nAGR_ASSIGNED" as AUDITAR
 }

 assign_function_groups --> UC_ACC_04

 UC_ACC_04 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_04 ..> VALIDAR_AGR_ENTITY : <<include>>
 UC_ACC_04 ..> EXPANDIR : <<include>>
 UC_ACC_04 ..> VALIDAR_SOD : <<include>>
 UC_ACC_04 ..> PERSISTIR : <<include>>
 UC_ACC_04 ..> RECALC : <<include>>
 UC_ACC_04 ..> INVALIDAR : <<include>>
 UC_ACC_04 ..> NOTIFICAR : <<include>>
 UC_ACC_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_AGR_ENTITY --> AccessGroupRepo
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> AssignmentRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 NOTIFICAR --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005: SoD sobre
   FUNCIONES expandidas del AGR,
   no sobre AGR como entidad.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup target.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   funciones expandidas.
 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   Assignment con target=AccessGroup.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD evaluadas.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta SoD.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica destino.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica assign_function_groups.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor AGR_ASSIGNED.
 - :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
   spec textual.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-01/index` —
   vista PERM (governance).
