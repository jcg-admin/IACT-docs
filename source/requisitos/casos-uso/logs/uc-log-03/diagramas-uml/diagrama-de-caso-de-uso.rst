8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "search_logs" as INVOKER
 actor "ApplicationLog" as LOG <<sistema>>
 actor "FilterValidator" as FV <<sistema>>
 actor "CursorEncoder" as CE <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_03\nBuscar Logs (FTS)" as UC_LOG_03
   usecase "Validar query\nno vacia" as VALIDAR_QUERY
   usecase "Validar range\n(max 7 dias)" as VALIDAR_RANGE
   usecase "Aplicar filtros\nestructurados" as FILTROS
   usecase "Ejecutar bounded\nFTS" as FTS_QUERY
   usecase "Cursor-based\npagination" as PAGINACION
 }

 INVOKER --> UC_LOG_03
 UC_LOG_03 ..> VALIDAR_QUERY : <<include>>
 UC_LOG_03 ..> VALIDAR_RANGE : <<include>>
 UC_LOG_03 ..> FILTROS : <<include>>
 UC_LOG_03 ..> FTS_QUERY : <<include>>
 UC_LOG_03 ..> PAGINACION : <<include>>

 VALIDAR_QUERY --> FV
 VALIDAR_RANGE --> FV
 FILTROS --> FV
 FTS_QUERY --> LOG
 PAGINACION --> CE

 note bottom of VALIDAR_RANGE
   Range obligatorio ≤ 7 dias para
   limitar costo de FTS bounded.
   Para rangos mayores: export
   (UC_LOG_04).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   storage indexado para FTS.
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator` —
   componente de validacion query/range/filtros.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   codificacion de cursor de paginacion.
