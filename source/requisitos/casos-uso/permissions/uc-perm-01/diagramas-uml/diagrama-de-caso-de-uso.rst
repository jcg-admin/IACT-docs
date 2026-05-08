8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_01 — vista PERM de UC_ACC_04

 @startuml

 left to right direction

 actor "assign_function_groups" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "RuleValidator" as RV <<sistema>>
 actor "PermissionCache" as PC <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo a Usuario\n(vista PERM)" as UC_PERM_01
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR" as UC_ACC_04
   usecase "Validar AccessGroup\nexiste + ACTIVE" as VALIDAR_AGRUPADOR
   usecase "Expandir funciones\ndel AccessGroup" as EXPANDIR
   usecase "Validar separacion\n(set efectivo)" as VALIDAR_SEPARATION_RULES
   usecase "Persistir Assignment\n(target=AccessGroup)" as PERSISTIR
   usecase "Invalidar PermissionCache" as CACHE_INV
   usecase "Emitir AuditEvent\nAGR_ASSIGNED" as AUDIT
 }

 INVOKER --> UC_PERM_01
 UC_PERM_01 ..> UC_ACC_04 : <<include>>
 UC_ACC_04 ..> VALIDAR_AGRUPADOR : <<include>>
 UC_ACC_04 ..> EXPANDIR : <<include>>
 UC_ACC_04 ..> VALIDAR_SEPARATION_RULES : <<include>>
 UC_ACC_04 ..> PERSISTIR : <<include>>
 UC_ACC_04 ..> CACHE_INV : <<include>>
 UC_ACC_04 ..> AUDIT : <<include>>

 VALIDAR_SEPARATION_RULES --> RV
 CACHE_INV --> PC
 AUDIT --> AS
 AS --> view_audit_log
 PERSISTIR --> TARGET

 note bottom of UC_PERM_01
   ADR-GOB-008: vista PERM y vista
   ACC comparten misma funcion canonica
   `assign_function_groups`. UI difiere
   por audiencia (governance vs operacion);
   backend identico — UC_PERM_01 incluye
   UC_ACC_04 como su realizacion completa.
 end note

 note bottom of VALIDAR_SEPARATION_RULES
   BR-007 + CNST-005: separacion se evalua
   sobre FUNCIONES expandidas del AGR,
   no sobre AGR como entidad.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup objetivo (validado en VALIDAR_AGRUPADOR).
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   funciones del AccessGroup expandidas en EXPANDIR.
 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   entidad Assignment persistida con target=AccessGroup.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   repositorio que persiste el Assignment.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas de separacion evaluadas en VALIDAR_SEPARATION_RULES (CNST-005).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que ejecuta validacion de separacion.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada post-COMMIT.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent AGR_ASSIGNED.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-025).
 - :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
   UC backing (operacion completa).
