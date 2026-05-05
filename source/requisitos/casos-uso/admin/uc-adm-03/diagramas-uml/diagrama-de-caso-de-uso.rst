8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "assign_functions_to_group" as F_ASSIGN
 actor "view_system_groups" as F_VIEW <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "PermissionsEngine" as PE <<sistema>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_03\nGestionar Catalogo de\nAgrupadores del Sistema" as UC_ADM_03
   usecase "Verificar\nis_system=True" as VERIFY_SYS
   usecase "Validar funcion en\ncatalogo (UC_ADM_02)" as VALIDAR_FUNCION
   usecase "Validar SoD\n(UC_ADM_01, CNST-005)" as VALIDAR_SOD
   usecase "Validar idempotencia\n(funcion no ya asignada)" as IDEMP
   usecase "Persistir\nGroupFunction" as PERSISTIR
   usecase "AuditEvent\nAGR_FUNCTION_*" as AUDIT
   usecase "PermissionsEngine\n.recalculate(agr_id)" as RECALC
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
 UC_ADM_03 ..> RECALC : <<include>>
 IMPACT ..> UC_ADM_03 : <<extend>>

 Sistema --> AUDIT
 Sistema --> RECALC
 AUDIT --> view_audit_log
 RECALC --> PE

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
