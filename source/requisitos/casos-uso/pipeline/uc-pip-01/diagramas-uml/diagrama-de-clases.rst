.. _uc-pip-01-parte-08-diagrama-clases:

8.4 Diagrama de clases
=======================

.. uml::
 :caption: UC_PIP_01 — clases involucradas.

 @startuml

 class SupervisionETLService {
   + supervisar() : ResumenSalud
 }

 class PipelineExecutionRepo {
   + last_successful_by_dataset(dataset) : PipelineExecution
   + find_recent(period) : List
 }

 class ResumenSaludAssembler {
   + build(executions) : ResumenSalud
 }

 class ResumenSalud {
   + estado_general : EstadoSalud
   + ultima_ejecucion : DateTime
   + total_exitosas : Integer
   + total_fallidas : Integer
 }

 SupervisionETLService --> PipelineExecutionRepo : reads
 SupervisionETLService --> ResumenSaludAssembler : delegates
 ResumenSaludAssembler --> ResumenSalud : produces

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`.
