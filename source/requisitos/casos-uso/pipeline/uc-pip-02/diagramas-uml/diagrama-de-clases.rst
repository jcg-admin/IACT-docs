.. _uc-pip-02-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_PIP_02 — clases.

 @startuml

 class ErroresETLService {
   + listar(filters, period) : List
 }

 class PipelineExecutionRepo {
   + por_estado(state, filters) : List
 }

 ErroresETLService --> PipelineExecutionRepo : reads

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`.
