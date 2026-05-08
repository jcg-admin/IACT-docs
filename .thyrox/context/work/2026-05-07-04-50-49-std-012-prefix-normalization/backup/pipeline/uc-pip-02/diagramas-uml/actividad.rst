8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/etl/errores/ con filtros;
 :JWT + RBAC (view_pipeline_errors);
 :Validar parametros;
 :Consultar Registro de Ejecuciones (fallidas);
 :200 con lista de ejecuciones fallidas;
 stop
 @enduml

