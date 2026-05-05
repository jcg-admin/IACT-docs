8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/system/;
 :JWT + RBAC;
 :Validar range;
 :Query LogStore;
 :Sanitize;
 :200;
 stop
 @enduml

