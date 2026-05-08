8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST search;
 :JWT + RBAC;
 :Validar query + range ≤ 90;
 :Throttle check;
 :FTS search;
 :Sanitize results;
 :Meta-audit;
 :200;
 stop
 @enduml

