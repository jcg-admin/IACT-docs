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
   usecase "Validar User destino" as VALIDAR_USUARIO_DESTINO
   usecase "Validar funciones\n(existen + activas)" as VALIDAR_FUNCIONES
   usecase "Filtrar idempotente" as FILTRO_IDEMPOTENTE
   usecase "Validar SoD\n(CNST-005)" as VALIDAR_SOD
   usecase "registrar N Assignments" as RegistrarDatos
   usecase "Invalidar cache\npermisos" as CACHE_PERMISOS
   usecase "Notificar via\nInternalMailbox" as NotificacionMailbox
   usecase "AuditEvent\nFUNCTIONS_ASSIGNED" as AuditEmitter
 }

 INVOKER --> UC01
 UC01 ..> VALIDAR_USUARIO_DESTINO : <<include>>
 UC01 ..> VALIDAR_FUNCIONES : <<include>>
 UC01 ..> FILTRO_IDEMPOTENTE : <<include>>
 UC01 ..> VALIDAR_SOD : <<include>>
 UC01 ..> INS : <<include>>
 UC01 ..> CACHE_PERMISOS : <<include>>
 UC01 ..> NOT : <<extend>>
 UC01 ..> EMI : <<include>>
 NOT --> TARGET
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005:
   all-or-nothing — SoD violation
   bloquea TODA la asignacion
 end note
 note bottom of VALIDAR_FUNCIONES
   P-15 RBAC granular:
   funcion canonica, no AGR
 end note

 @enduml

