.. meta::
 :artefacto: AT_UC_ADM_01_USECASE
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

.. _at_uc_adm_01_gestionar_ciclo_de_vida_de_reglas_de_separacion:

============================================================
UC_ADM_01 — Gestionar Ciclo de Vida de Reglas de Separacion
============================================================

Administra el ciclo de vida completo de las **reglas de separacion
de deberes** (Separation of Duties): crear, actualizar parametros,
activar/desactivar y consultar. Mecanismo formal para agregar reglas
de separacion desde la aplicacion (las 3 reglas estaticas
SOD-001..003 fueron definidas en migraciones por CNST-030; los
codigos preservan la convencion historica del catalogo en BD).

.. uml::
 :caption: UC_ADM_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "create_separation_rule" as create_separation_rule
 actor "update_separation_rule" as update_separation_rule
 actor "disable_separation_rule" as disable_separation_rule
 actor "view_separation_rules" as view_separation_rules <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nGestionar Ciclo de Vida\nde Reglas de Separacion\n.. extension points ..\nValidacionFunciones\nValidacionConjuntos" as UC_ADM_01
   usecase "Verificar AGR-010\n(autorizacion)" as VERIFICAR_AGR
   usecase "Validar conjuntos\ndisjuntos (CNST-030)" as VALIDAR_CONJUNTOS
   usecase "Validar funciones\nen catalogo activo" as VALIDAR_FUNCIONES
   usecase "Validar nombre\nunico" as VALIDAR_NOMBRE
   usecase "Persistir SeparationRule\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nSEPARATION_RULE_*" as AUDITAR
   usecase "Recargar reglas\nactivas" as RECARGAR
   usecase "Reactivar regla\ninactiva" as REACTIVAR
 }

 create_separation_rule --> UC_ADM_01
 update_separation_rule --> UC_ADM_01
 disable_separation_rule --> UC_ADM_01
 view_separation_rules --> UC_ADM_01

 UC_ADM_01 ..> VERIFICAR_AGR : <<include>>
 UC_ADM_01 ..> VALIDAR_CONJUNTOS : <<include>>
 UC_ADM_01 ..> VALIDAR_FUNCIONES : <<include>>
 UC_ADM_01 ..> VALIDAR_NOMBRE : <<include>>
 UC_ADM_01 ..> PERSISTIR : <<include>>
 UC_ADM_01 ..> AUDITAR : <<include>>
 UC_ADM_01 ..> RECARGAR : <<include>>
 REACTIVAR ..> UC_ADM_01 : <<extend>> (ValidacionFunciones)

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_CONJUNTOS --> RuleValidator
 VALIDAR_FUNCIONES --> RuleValidator
 PERSISTIR --> SeparationRuleRepo
 AUDITAR --> AuditService
 AuditService --> view_audit_log
 RECARGAR --> EvaluatorReloader

 note bottom of VALIDAR_CONJUNTOS
   CNST-030: group_a y group_b
   disjuntos. Funcion en ambos
   grupos rechaza 400 (FA-02).
 end note

 note bottom of AUDITAR
   SEPARATION_RULE_CREATED / UPDATED /
   DISABLED. CNST-025 alta criticidad
   — cambios al modelo RBAC.
 end note

 note right of view_separation_rules
   AGR-010 system_admin agrupa
   las 4 funciones. view_separation_rules
   read-only reutilizada desde UC_ACC_05.
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   SeparationRule entity persistida (CNST-030).
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo` —
   repositorio CRUD + queries de reglas de separacion activas.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   catalogo validado en VALIDAR_FUNCIONES.
 - :doc:`/arquitectura-tecnica/domain-model/function-repo` —
   exists_codename para validar funciones existen.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que ejecuta VALIDAR_CONJUNTOS / VALIDAR_FUNCIONES.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica AGR-010 antes de acceder a este UC.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   notificado en RECARGAR para refrescar reglas activas.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent SEPARATION_RULE_*.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-025).
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   SeparationRuleViolationSpec consumida por RuleValidator.

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` — Parte 1-12.
