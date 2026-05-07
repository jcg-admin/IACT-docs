8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con period + filtros;
 :JWT + RBAC;
 :Cache lookup;
 :Query TSDB;
 :Compute percentiles;
 :Cache write;
 :200;
 stop
 @enduml

