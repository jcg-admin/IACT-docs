.. _uc-pip-01-parte-08-diagrama-estados-ejecucion-etl:

8.3 Diagrama de estados — Ejecucion ETL
=========================================

.. uml::
 :caption: PipelineExecution — ciclo de vida.

 @startuml

 [*] --> en_ejecucion : Disparador ETL invoca SP
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*]

 note right of fallido
   Error preservado en
   PipelineExecution.error_message
   para diagnostico (UC_PIP_02).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
