8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/etl/supervision/;
 :JWT + RBAC (view_pipeline_status);
 :Consultar Registro de Ejecuciones;
 :Construir ResumenSalud;
 :200 con estado general;
 stop
 @enduml

