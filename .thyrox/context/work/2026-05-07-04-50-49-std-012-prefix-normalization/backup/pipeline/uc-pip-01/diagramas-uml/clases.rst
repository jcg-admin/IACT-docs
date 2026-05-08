8.4 Clases
==========

.. uml::

 @startuml
 class SupervisionETLService
 class PipelineExecutionRepo
 class ResumenSaludBuilder
 SupervisionETLService --> PipelineExecutionRepo
 SupervisionETLService --> ResumenSaludBuilder
 @enduml
