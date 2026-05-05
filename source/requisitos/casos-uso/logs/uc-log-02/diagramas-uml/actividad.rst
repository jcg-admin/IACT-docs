8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/etl/;
 :JWT + RBAC (view_pipeline_logs);
 :Validar filtros (trimestre, estado);
 :Consultar pipeline_runs en el Almacen de Datos;
 :Filtrar por estado si aplica;
 :Sanitizar resultados;
 :200 con lista de ejecuciones ETL;
 stop
 @enduml

