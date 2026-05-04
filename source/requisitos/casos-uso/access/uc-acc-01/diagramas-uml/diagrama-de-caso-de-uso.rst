8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "assign_functions" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones" as UC01
   usecase "Validar User destino" as VUSER
   usecase "Validar funciones\n(existen + activas)" as VFUN
   usecase "Filtrar idempotente" as IDEM
   usecase "Validar SoD\n(CNST-005)" as VSOD
   usecase "registrar N Assignments" as INS
   usecase "Invalidar cache\npermisos" as CACHE
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "AuditEvent\nFUNCTIONS_ASSIGNED" as EMI
 }

 INVOKER --> UC01
 UC01 ..> VUSER : <<include>>
 UC01 ..> VFUN : <<include>>
 UC01 ..> IDEM : <<include>>
 UC01 ..> VSOD : <<include>>
 UC01 ..> INS : <<include>>
 UC01 ..> CACHE : <<include>>
 UC01 ..> NOT : <<extend>>
 UC01 ..> EMI : <<include>>
 NOT --> TARGET
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of VSOD
   BR-007 + CNST-005:
   all-or-nothing — SoD violation
   bloquea TODA la asignacion
 end note
 note bottom of VFUN
   P-15 RBAC granular:
   funcion canonica, no AGR
 end note

 @enduml

