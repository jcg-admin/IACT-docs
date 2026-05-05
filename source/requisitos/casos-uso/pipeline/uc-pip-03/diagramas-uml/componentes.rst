8.4 Componentes
===============

.. uml::

 @startuml
 component "DisponibilidadDatosService" as Disponibilidaddatosservice
 component "ETLEjecucionRepo" as Etlejecucionrepo
 component "DisponibilidadBuilder" as Disponibilidadbuilder
 Disponibilidaddatosservice --> Etlejecucionrepo
 Disponibilidaddatosservice --> Disponibilidadbuilder
 @enduml
