8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_04 — actores y casos asociados

 @startuml
 left to right direction

 actor "assign_function_groups" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR" as UC_ACC_04
   usecase "Validar AGR\nexiste + ACTIVE" as VALIDAR_AGRUPADOR
   usecase "Expandir funciones\ndel AGR" as ExportarDatos
   usecase "Validar separacion\n(set efectivo)" as ValidadorSeparacion
   usecase "registrar Assignment\n(target=AGR)" as RegistrarDatos
   usecase "Invalidar cache" as CACHE_PERMISOS
   usecase "AuditEvent\nAGR_ASSIGNED" as AuditEmitter
 }

 INVOKER --> UC_ACC_04
 UC_ACC_04 ..> VALIDAR_AGRUPADOR : <<include>>
 UC_ACC_04 ..> EXP : <<include>>
 UC_ACC_04 ..> VALIDAR_SEPARATION : <<include>>
 UC_ACC_04 ..> INS : <<include>>
 UC_ACC_04 ..> CACHE_PERMISOS : <<include>>
 UC_ACC_04 ..> EMI : <<include>>
 EMI --> view_audit_log

 note bottom of VALIDAR_SEPARATION
   separacion se evalua sobre FUNCIONES,
   no sobre AGRs como entidad
 end note

 @enduml

