8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_01 — vista PERM de UC_ACC_04

 @startuml

 left to right direction

 actor "assign_function_groups" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo a Usuario\n(vista PERM)" as UC_PERM_01
 }

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR" as UC_ACC_04
   usecase "Validar AGR\nexiste + ACTIVE" as VALIDAR_AGRUPADOR
   usecase "Expandir funciones\ndel AGR" as EXPANDIR
   usecase "Validar SoD\n(set efectivo)" as VALIDAR_SOD
   usecase "Persistir Assignment\n(target=AGR)" as PERSISTIR
   usecase "Invalidar cache\npermisos" as CACHE_PERMISOS
   usecase "AuditEvent\nAGR_ASSIGNED" as AUDIT
 }

 INVOKER --> UC_PERM_01
 UC_PERM_01 ..> UC_ACC_04 : <<include>>
 UC_ACC_04 ..> VALIDAR_AGRUPADOR : <<include>>
 UC_ACC_04 ..> EXPANDIR : <<include>>
 UC_ACC_04 ..> VALIDAR_SOD : <<include>>
 UC_ACC_04 ..> PERSISTIR : <<include>>
 UC_ACC_04 ..> CACHE_PERMISOS : <<include>>
 UC_ACC_04 ..> AUDIT : <<include>>

 AUDIT --> view_audit_log
 PERSISTIR --> TARGET

 note bottom of UC_PERM_01
   ADR-GOB-008: vista PERM y vista
   ACC comparten misma funcion canonica
   `assign_function_groups`. UI difiere
   por audiencia (governance vs operacion);
   backend identico — UC_PERM_01 incluye
   UC_ACC_04 como su realizacion completa.
 end note

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005: SoD se evalua
   sobre FUNCIONES expandidas del AGR,
   no sobre AGR como entidad.
 end note

 @enduml
