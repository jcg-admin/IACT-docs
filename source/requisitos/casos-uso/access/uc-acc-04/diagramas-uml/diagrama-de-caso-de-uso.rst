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
   usecase "UC_ACC_04\nAsignar AGR" as UC04
   usecase "Validar AGR\nexiste + ACTIVE" as VAGR
   usecase "Expandir funciones\ndel AGR" as ExportarDatos
   usecase "Validar SoD\n(set efectivo)" as ValidadorSoD
   usecase "registrar Assignment\n(target=AGR)" as RegistrarDatos
   usecase "Invalidar cache" as CACHE
   usecase "AuditEvent\nAGR_ASSIGNED" as AuditEmitter
 }

 INVOKER --> UC04
 UC04 ..> VAGR : <<include>>
 UC04 ..> EXP : <<include>>
 UC04 ..> SOD : <<include>>
 UC04 ..> INS : <<include>>
 UC04 ..> CACHE : <<include>>
 UC04 ..> EMI : <<include>>
 EMI --> view_audit_log

 note bottom of SOD
   SoD se evalua sobre FUNCIONES,
   no sobre AGRs como entidad
 end note

 @enduml

