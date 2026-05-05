8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "assign_functions_to_group" as F_ASSIGN
 actor "view_system_groups" as F_VIEW <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "RuleValidator" as RV <<sistema>>
 actor "PermissionService" as PS <<sistema>>
 actor "PermissionCache" as PC <<sistema>>
 actor "EvaluatorReloader" as EE <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_03\nGestionar Catalogo de\nAgrupadores del Sistema" as UC_ADM_03
   usecase "Verificar\nis_system=True" as VERIFY_SYS
   usecase "Validar funcion en\ncatalogo (UC_ADM_02)" as VALIDAR_FUNCION
   usecase "Validar SoD\n(UC_ADM_01, CNST-005)" as VALIDAR_SOD
   usecase "Validar idempotencia\n(funcion no ya asignada)" as IDEMP
   usecase "Persistir\nAccessGroupFunction" as PERSISTIR
   usecase "Emitir AuditEvent\nAGR_FUNCTION_*" as AUDIT
   usecase "Invalidar cache\npermisos" as INVALIDAR
   usecase "EvaluatorReloader\n.recalculate(agr_id)" as RECALC
   usecase "Vista de impacto\n(que usuarios cambian)" as IMPACT
 }

 F_ASSIGN --> UC_ADM_03
 F_VIEW --> UC_ADM_03

 UC_ADM_03 ..> VERIFY_SYS : <<include>>
 UC_ADM_03 ..> VALIDAR_FUNCION : <<include>>
 UC_ADM_03 ..> VALIDAR_SOD : <<include>>
 UC_ADM_03 ..> IDEMP : <<include>>
 UC_ADM_03 ..> PERSISTIR : <<include>>
 UC_ADM_03 ..> AUDIT : <<include>>
 UC_ADM_03 ..> INVALIDAR : <<include>>
 UC_ADM_03 ..> RECALC : <<include>>
 IMPACT ..> UC_ADM_03 : <<extend>>

 VALIDAR_SOD --> RV
 INVALIDAR --> PC
 RECALC --> EE
 RECALC --> PS
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VERIFY_SYS
   AGR-001..012 son del sistema.
   UC_PERM_05 cubre AGR custom.
 end note

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005: agregar
   funcion no debe romper reglas
   SoD de los usuarios que ya
   tienen el AGR.
 end note

 note bottom of RECALC
   Cambio en composicion afecta
   effective_set de TODOS los
   usuarios con AGR-N asignado.
   Invalidacion en cascada.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup (AGR-001..012 con is_system=True).
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   tabla de asociacion M:N persistida por este UC.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   Function validada en VALIDAR_FUNCION (catalogo UC_ADM_02).
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD evaluadas en VALIDAR_SOD (CNST-005).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que ejecuta validaciones de SoD.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidado tras cambio de composicion AGR.
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   recalcula effective_set de usuarios afectados.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   coordinador del recalculo en cascada.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent AGR_FUNCTION_*.
