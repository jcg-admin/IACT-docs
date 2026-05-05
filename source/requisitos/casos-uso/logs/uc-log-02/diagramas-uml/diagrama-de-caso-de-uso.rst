8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_pipeline_logs" as INVOKER
 actor "PipelineLog" as PL <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs\ndel Pipeline" as UC_LOG_02
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Forzar service ∈\n{etl-runner,\netl-validator, ...}" as FORZAR_SERVICE
   usecase "Filtrar por\npipeline_id" as FILTRAR_PIP
   usecase "Devolver entries" as DEVOLVER
 }

 INVOKER --> UC_LOG_02
 UC_LOG_02 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_02 ..> FORZAR_SERVICE : <<include>>
 UC_LOG_02 ..> FILTRAR_PIP : <<include>>
 UC_LOG_02 ..> DEVOLVER : <<include>>

 FORZAR_SERVICE --> PL
 FILTRAR_PIP --> PL
 DEVOLVER --> PL

 note bottom of UC_LOG_02
   Variante de UC_LOG_01 con scope
   Pipeline forzado. Funcion separada
   para granular: data engineers
   ven Pipeline logs sin acceder
   al sistema general.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   entidad PipelineLog (logs especificos del Pipeline).
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   PipelineExecution referenciado por pipeline_id.
 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   storage compartido (subset filtrado por service).
