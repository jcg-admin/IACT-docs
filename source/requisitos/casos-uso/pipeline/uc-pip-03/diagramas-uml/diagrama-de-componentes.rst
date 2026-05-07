.. _uc-pip-03-parte-08-diagrama-componentes:

8.4 Diagrama de componentes
=============================

.. uml::
 :caption: UC_PIP_03 — componentes involucrados, agrupados
           por capa (Boundary / Domain / Infrastructure).

 @startuml

 package "Boundary" {
   component "Servicio de Aplicacion" as SA
 }

 package "Domain" {
   component "DisponibilidadDatosService" as DisponibilidadDatosService
   component "DisponibilidadBuilder" as DisponibilidadBuilder
 }

 package "Infrastructure" {
   component "PipelineExecutionRepo" as PipelineExecutionRepo
   component "Almacen de Datos" as AlmacenDatos
 }

 SA --> DisponibilidadDatosService : query disponibilidad
 DisponibilidadDatosService --> PipelineExecutionRepo : query ultima exitosa
 DisponibilidadDatosService --> DisponibilidadBuilder : computa frescura
 PipelineExecutionRepo --> AlmacenDatos : persists

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
