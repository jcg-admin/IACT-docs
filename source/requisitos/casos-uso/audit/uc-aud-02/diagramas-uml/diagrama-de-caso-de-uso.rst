8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "search_audit_log" as INVOKER
 actor "AuditSearchEngine" as FTS <<sistema>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar Auditoria\n(FTS)" as UC_AUD_02
   usecase "Validar query\nno vacia" as VALIDAR_QUERY
   usecase "Validar date_range\nobligatorio (max 90d)" as VALIDAR_RANGE
   usecase "Aplicar filtros\nestructurados" as FILTROS
   usecase "Ejecutar full-text\nsearch" as FTS_QUERY
   usecase "Cursor-based\npagination" as PAGINACION
   usecase "Meta-audit\nAUDIT_SEARCHED" as METAAUDIT
 }

 INVOKER --> UC_AUD_02
 UC_AUD_02 ..> VALIDAR_QUERY : <<include>>
 UC_AUD_02 ..> VALIDAR_RANGE : <<include>>
 UC_AUD_02 ..> FILTROS : <<include>>
 UC_AUD_02 ..> FTS_QUERY : <<include>>
 UC_AUD_02 ..> PAGINACION : <<include>>
 UC_AUD_02 ..> METAAUDIT : <<include>>

 FTS_QUERY --> FTS
 Sistema --> METAAUDIT

 note bottom of VALIDAR_RANGE
   date_range obligatorio para
   evitar full table scans.
   Maximo 90 dias por consulta.
 end note

 note bottom of UC_AUD_02
   CNST-008/009/025/026.
   Out of scope: timeline UC_AUD_01,
   exportacion UC_AUD_03.
 end note

 @enduml
