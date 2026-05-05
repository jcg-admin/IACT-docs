8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_09 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_own_call_history" as INVOKER
 actor "CallSessionRepo" as REPO <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_09\nVer Propio Historial\nde Llamadas" as UC_OPR_09
   usecase "Validar period\n(default last_7d)" as VALIDAR_PERIOD
   usecase "Filtrar por\ndisposition" as FILTRAR
   usecase "Cargar caller_hash\n(sin PII)" as HASH
   usecase "Devolver entries\n(disposition + duracion + tags)" as DEVOLVER
   usecase "Cursor pagination" as PAGINACION
 }

 INVOKER --> UC_OPR_09
 UC_OPR_09 ..> VALIDAR_PERIOD : <<include>>
 UC_OPR_09 ..> FILTRAR : <<include>>
 UC_OPR_09 ..> HASH : <<include>>
 UC_OPR_09 ..> DEVOLVER : <<include>>
 UC_OPR_09 ..> PAGINACION : <<include>>

 FILTRAR --> REPO
 DEVOLVER --> REPO

 note bottom of UC_OPR_09
   BReq-007. Vista PROPIA del agente.
   Util para self-coaching, recordar
   casos pendientes, dar follow-up.
 end note

 note bottom of HASH
   CNST-026 sin PII: caller_hash
   se devuelve, NUNCA caller_id
   en limpio.
 end note

 @enduml
