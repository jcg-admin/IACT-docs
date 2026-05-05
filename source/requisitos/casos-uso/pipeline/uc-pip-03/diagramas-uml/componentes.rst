8.4 Componentes
===============

.. uml::

 @startuml
 component "DisponibilidadDatosService" as Disponibilidaddatosservice
 component "PipelineExecutionRepo" as Etlejecucionrepo
 component "DisponibilidadBuilder" as Disponibilidadbuilder
 Disponibilidaddatosservice --> Etlejecucionrepo
 Disponibilidaddatosservice --> Disponibilidadbuilder
 @enduml
