.. meta::
 :artefacto: AT_UC_LOG_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_log_03_buscar_logs:

==============================
UC_LOG_03 — Buscar Logs (FTS)
==============================

FTS bounded sobre ApplicationLog. ``search_logs``. Range obligatorio
≤ 7 dias para limitar costo de FTS bounded. Para periodos mayores
usar export (UC_LOG_04).

.. uml::
 :caption: UC_LOG_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "search_logs" as search_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FilterValidator" as FilterValidator <<sistema>>
 actor "ApplicationLog" as ApplicationLog <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_03\nBuscar Logs (FTS)" as UC_LOG_03
   usecase "Verificar\nsearch_logs" as VERIFICAR_AGR
   usecase "Validar query\nno vacia" as VALIDAR_QUERY
   usecase "Validar range\n(max 7 dias)" as VALIDAR_RANGE
   usecase "Aplicar filtros\nestructurados" as FILTROS
   usecase "Ejecutar bounded FTS" as FTS_QUERY
   usecase "Cursor pagination" as PAGINACION
 }

 search_logs --> UC_LOG_03

 UC_LOG_03 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_03 ..> VALIDAR_QUERY : <<include>>
 UC_LOG_03 ..> VALIDAR_RANGE : <<include>>
 UC_LOG_03 ..> FILTROS : <<include>>
 UC_LOG_03 ..> FTS_QUERY : <<include>>
 UC_LOG_03 ..> PAGINACION : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_QUERY --> FilterValidator
 VALIDAR_RANGE --> FilterValidator
 FILTROS --> FilterValidator
 FTS_QUERY --> ApplicationLog
 PAGINACION --> CursorEncoder

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   storage indexado para FTS.
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator` —
   validacion query/range/filtros.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   BoundedDateRangeSpec.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-03/index` —
   spec textual.
