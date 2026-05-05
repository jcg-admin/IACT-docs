8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_pipeline_errors" as INVOKER
 actor "PipelineLog" as PL <<sistema>>
 actor "PipelineExecution" as PE <<sistema>>
 actor "PIIScanner" as PII <<sistema>>
 actor "Sanitizer" as SAN <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nConsultar Errores\ndel Pipeline" as UC_PIP_02
   usecase "Filtrar ejecuciones\nfailed" as FILTRAR
   usecase "Cargar stack trace\n+ error_code" as CARGAR_TRACE
   usecase "Sanitizar payload\n(sin PII)" as SANITIZAR
   usecase "Devolver\ncorrelation_id" as CORRELATION
 }

 INVOKER --> UC_PIP_02
 UC_PIP_02 ..> FILTRAR : <<include>>
 UC_PIP_02 ..> CARGAR_TRACE : <<include>>
 UC_PIP_02 ..> SANITIZAR : <<include>>
 UC_PIP_02 ..> CORRELATION : <<include>>

 FILTRAR --> PE
 CARGAR_TRACE --> PL
 SANITIZAR --> PII
 SANITIZAR --> SAN

 note bottom of SANITIZAR
   Stack traces pueden contener PII
   (CNST-026). PIIScanner detecta,
   Sanitizer reemplaza antes de
   devolver al cliente.
 end note

 note bottom of CORRELATION
   correlation_id permite tracing
   end-to-end. Out of scope: reintento
   (UC_PIP_04).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   PipelineExecution (filtra estado=failed).
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   logs detallados con stack trace y error_code.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector de PII en stack traces.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   sanitizador que reemplaza PII detectada.
