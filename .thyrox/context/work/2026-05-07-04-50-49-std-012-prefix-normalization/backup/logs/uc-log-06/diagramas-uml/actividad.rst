8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET status;
 :JWT + RBAC;
 :Cache lookup;
 fork
   :Check services;
 fork again
   :Check deps;
 fork again
   :Query ETL summary;
 fork again
   :Query alerts active count;
 end fork
 :Compute overall status;
 :Cache write;
 :200;
 stop
 @enduml

