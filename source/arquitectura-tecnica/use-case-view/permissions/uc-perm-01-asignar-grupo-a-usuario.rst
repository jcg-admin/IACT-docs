.. meta::
 :artefacto: AT_UC_PERM_01_USECASE
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

.. _at_uc_perm_01_asignar_grupo_a_usuario:

============================================================
UC_PERM_01 — Asignar Grupo a Usuario (vista PERM)
============================================================

Vista PERM (governance) de la asignacion de AccessGroup a User. Misma
funcion canonica que UC_ACC_04 (vista ACC operacional):
``assign_function_groups``. ADR-GOB-008 — coexistencia ACC ↔ PERM:
mismo backend, UI distinta por audiencia (operacion diaria vs
compliance review).

.. uml::
 :caption: UC_PERM_01 — vista PERM de UC_ACC_04.

 @startuml

 left to right direction

 actor "assign_function_groups" as assign_function_groups
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "AccessGroupRepo" as AccessGroupRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo a Usuario\n(vista PERM)" as UC_PERM_01
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AccessGroup" as UC_ACC_04
   usecase "Verificar\nassign_function_groups" as VERIFICAR_AGR
   usecase "Validar AccessGroup\nexiste + ACTIVE" as VALIDAR_AGR_ENTITY
   usecase "Expandir funciones\ndel AccessGroup" as EXPANDIR
   usecase "Validar regla de separacion\n(set efectivo CNST-005)" as VALIDAR_SEPARATION_RULES
   usecase "Persistir Assignment\n(target=AccessGroup)" as PERSISTIR
   usecase "Recompute effective_set" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nAGR_ASSIGNED" as AUDITAR
 }

 assign_function_groups --> UC_PERM_01

 UC_PERM_01 ..> UC_ACC_04 : <<include>>
 UC_ACC_04 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_04 ..> VALIDAR_AGR_ENTITY : <<include>>
 UC_ACC_04 ..> EXPANDIR : <<include>>
 UC_ACC_04 ..> VALIDAR_SEPARATION_RULES : <<include>>
 UC_ACC_04 ..> PERSISTIR : <<include>>
 UC_ACC_04 ..> RECALC : <<include>>
 UC_ACC_04 ..> INVALIDAR : <<include>>
 UC_ACC_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_AGR_ENTITY --> AccessGroupRepo
 VALIDAR_SEPARATION_RULES --> RuleValidator
 PERSISTIR --> AssignmentRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 PERSISTIR --> User_destino
 AuditService --> view_audit_log

 note bottom of UC_PERM_01
   ADR-GOB-008: misma funcion canonica
   assign_function_groups que UC_ACC_04.
   UI difiere por audiencia: governance
   (PERM) vs operacion (ACC). Backend
   identico — UC_PERM_01 incluye UC_ACC_04
   como su realizacion completa.
 end note

 note bottom of VALIDAR_SEPARATION_RULES
   BR-007 + CNST-005: separacion se evalua sobre
   FUNCIONES expandidas del AccessGroup,
   no sobre AccessGroup como entidad.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup objetivo.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   funciones expandidas del AGR.
 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   Assignment persistido (target=AccessGroup).
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas de separacion evaluadas (CNST-005).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta validacion de separacion.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute del User destino.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada post-COMMIT.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica assign_function_groups.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AGR_ASSIGNED.
 - :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
   UC backing (operacion completa).
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-01/index` —
   spec textual.
