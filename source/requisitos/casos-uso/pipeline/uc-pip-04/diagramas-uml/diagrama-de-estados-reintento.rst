.. _uc-pip-04-parte-08-diagrama-estados-reintento:

8.3 Diagrama de estados — Reintento ETL
=========================================

.. uml::
 :caption: PipelineExecution con manual=True — ciclo de reintento.

 @startuml

 [*] --> en_ejecucion : POST /reintento/\nDisparador ETL inicia
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*]

 note right of en_ejecucion
   manual=True distingue de
   ejecucion automatica programada.
 end note

 note right of fallido
   Si falla, requiere otro
   reintento manual o
   intervencion del admin.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
