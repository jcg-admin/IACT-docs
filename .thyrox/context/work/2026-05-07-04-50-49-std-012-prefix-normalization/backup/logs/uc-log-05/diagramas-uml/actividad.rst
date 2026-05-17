8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/infra/;
 :JWT + RBAC (view_infrastructure_logs);
 :Validar filtros (host, severity, range);
 :Consultar InfraLogStore;
 :Aplicar filtros;
 :Sanitizar resultados;
 :200 con entries de infraestructura;
 stop
 @enduml

