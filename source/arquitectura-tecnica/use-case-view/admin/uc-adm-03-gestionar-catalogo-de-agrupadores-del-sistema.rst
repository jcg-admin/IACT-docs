.. meta::
 :artefacto: AT_UC_ADM_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_adm_03_gestionar_catalogo_de_agrupadores_del_sistema:

==================================================
UC_ADM_03 — Gestionar Catalogo Agrupadores Sistema
==================================================

Modifica la composicion de los **12 agrupadores predefinidos del
sistema** (AGR-001..012, ``is_system=True``) — inmutables para
operadores, mutables solo por ``admin_sistema``. Diferente de
UC_PERM_05 que gestiona AGRs custom. Cambio en composicion dispara
recompute en cascada del effective_set de TODOS los Users con AGR
asignado.

.. uml::
 :caption: UC_ADM_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "view_system_groups" as view_system_groups <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FunctionGroupRepo" as FunctionGroupRepo <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_03\nGestionar Catalogo\nAgrupadores Sistema\n.. extension points ..\nVistaImpacto" as UC_ADM_03
   usecase "Verificar AGR-009" as VERIFICAR_AGR
   usecase "Verificar\nis_system=True" as VERIFICAR_SYS
   usecase "Validar funcion en\ncatalogo (UC_ADM_02)" as VALIDAR_FUNCION
   usecase "Validar SoD sobre\nUsers con AGR (CNST-005)" as VALIDAR_SOD
   usecase "Validar idempotencia\n(funcion no asignada)" as IDEMP
   usecase "Persistir\nAccessGroupFunction" as PERSISTIR
   usecase "Recompute effective_set\nen cascada" as RECALC
   usecase "Invalidar\nPermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nAGR_FUNCTION_*" as AUDITAR
   usecase "Vista de impacto\n(que Users cambian)" as IMPACT
 }

 assign_functions_to_group --> UC_ADM_03
 view_system_groups --> UC_ADM_03

 UC_ADM_03 ..> VERIFICAR_AGR : <<include>>
 UC_ADM_03 ..> VERIFICAR_SYS : <<include>>
 UC_ADM_03 ..> VALIDAR_FUNCION : <<include>>
 UC_ADM_03 ..> VALIDAR_SOD : <<include>>
 UC_ADM_03 ..> IDEMP : <<include>>
 UC_ADM_03 ..> PERSISTIR : <<include>>
 UC_ADM_03 ..> RECALC : <<include>>
 UC_ADM_03 ..> INVALIDAR : <<include>>
 UC_ADM_03 ..> AUDITAR : <<include>>
 IMPACT ..> UC_ADM_03 : <<extend>> (VistaImpacto)

 VERIFICAR_AGR --> AuthorizationGuard
 VERIFICAR_SYS --> FunctionGroupRepo
 VALIDAR_FUNCION --> FunctionRepo
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> FunctionGroupRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 RECALC --> EvaluatorReloader
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFICAR_SYS
   AGR-001..012: is_system=True
   (mutable solo por este UC).
   UC_PERM_05 gestiona AGRs custom.
 end note

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005: agregar funcion
   no debe romper SoD de Users que ya
   tienen el AGR asignado. Bloqueo
   write-time.
 end note

 note bottom of RECALC
   Cambio composicion afecta
   effective_set de TODOS los Users
   con AGR-N asignado. Invalidacion
   en cascada via Aggregator.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup AGR-001..012 con is_system=True.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   tabla M:N persistida.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   funciones validadas en catalogo activo.
 - :doc:`/arquitectura-tecnica/domain-model/function-group-repo` —
   repositorio que gestiona la composicion.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD evaluadas en VALIDAR_SOD.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta validacion SoD write-time.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute cascada de Users afectados.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   coordinador del recompute.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica AGR-009.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor AGR_FUNCTION_*.
 - :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` — Parte 1-12.
