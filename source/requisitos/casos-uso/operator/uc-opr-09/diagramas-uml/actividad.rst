8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /me/calls/;
 :JWT;
 :Validar range;
 :Query own;
 :Sanitize;
 :Paginar;
 :200;
 stop
 @enduml

