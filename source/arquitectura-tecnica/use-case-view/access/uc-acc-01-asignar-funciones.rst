.. meta::
 :artefacto: AT_UC_ACC_01_USECASE
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

.. _at_uc_acc_01_asignar_funciones:

==============================
UC_ACC_01 — Asignar Funciones
==============================

Asigna ``Function`` directas a un User (target_type=Function en
Assignment). Validaciones: User destino existe + state ACTIVE,
funciones existen + ACTIVE en catalogo, idempotencia (skip funciones
ya asignadas), separation write-time (BR-007 + CNST-005). Notificacion al
destino + AuditEvent ``FUNCTIONS_ASSIGNED``.

.. uml::
 :caption: UC_ACC_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "assign_functions" as assign_functions
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "IdempotencyPolicy" as IdempotencyPolicy <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones" as UC_ACC_01
   usecase "Verificar\nassign_functions" as VERIFICAR_AGR
   usecase "Validar User destino" as VALIDAR_USR
   usecase "Validar funciones\nactivas" as VALIDAR_FUNCION
   usecase "Filtrar idempotente\n(skip ya asignadas)" as IDEMP
   usecase "Validar regla de separacion\n(CNST-005)" as VALIDAR_SEPARATION_RULES
   usecase "Persistir Assignments\n(target=Function)" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Notificar destino" as NOTIFICAR
   usecase "Emitir AuditEvent\nFUNCTIONS_ASSIGNED" as AUDITAR
 }

 assign_functions --> UC_ACC_01

 UC_ACC_01 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_01 ..> VALIDAR_USR : <<include>>
 UC_ACC_01 ..> VALIDAR_FUNCION : <<include>>
 UC_ACC_01 ..> IDEMP : <<include>>
 UC_ACC_01 ..> VALIDAR_SEPARATION_RULES : <<include>>
 UC_ACC_01 ..> PERSISTIR : <<include>>
 UC_ACC_01 ..> RECALC : <<include>>
 UC_ACC_01 ..> INVALIDAR : <<include>>
 UC_ACC_01 ..> NOTIFICAR : <<include>>
 UC_ACC_01 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_USR --> UserRepo
 VALIDAR_FUNCION --> FunctionRepo
 IDEMP --> IdempotencyPolicy
 VALIDAR_SEPARATION_RULES --> RuleValidator
 PERSISTIR --> AssignmentRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 NOTIFICAR --> InternalMailbox
 InternalMailbox --> User_destino
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_SEPARATION_RULES
   BR-007 + CNST-005: separation write-time
   sobre conjunto efectivo (existing
   + new). All-or-nothing si viola.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   entity persistida (target=Function).
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   funciones validadas.
 - :doc:`/arquitectura-tecnica/domain-model/function-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   destino.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   verificacion.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas de separacion.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta validacion de separacion.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/idempotency-policy` —
   filter idempotente.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica destino.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica assign_functions.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor FUNCTIONS_ASSIGNED.
 - :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
   spec textual.
