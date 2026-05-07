.. _uc-pip-03-parte-08-diagrama-componentes:

8.4 Diagrama de componentes
=============================

.. uml::
 :caption: UC_PIP_03 — componentes involucrados.

 @startuml

 component "DisponibilidadDatosService" as DisponibilidadDatosService
 component "PipelineExecutionRepo" as PipelineExecutionRepo
 component "DisponibilidadBuilder" as DisponibilidadBuilder

 DisponibilidadDatosService --> PipelineExecutionRepo : query ultima exitosa
 DisponibilidadDatosService --> DisponibilidadBuilder : computa frescura

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`.
