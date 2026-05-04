8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_pipeline_errors" as view_pipeline_errors
 participant "Endpoint" as Endpoint
 database "Registro de\nEjecuciones" as RegistroDe
 view_pipeline_errors -> Endpoint: GET /api/v1/etl/errores/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> RegistroDe: query estado=fallido
 RegistroDe --> Endpoint: filas con mensaje_error
 Endpoint --> view_pipeline_errors: 200 lista ejecuciones fallidas
 @enduml
