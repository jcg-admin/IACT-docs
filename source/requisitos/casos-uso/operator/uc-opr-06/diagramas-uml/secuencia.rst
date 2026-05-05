8.4 Secuencia
=============

.. uml::

 @startuml
 actor "enter_call_disposition" as enter_call_disposition
 participant "Endpoint" as Endpoint
 database "Repo" as Repo
 enter_call_disposition -> Endpoint: POST disposition
 Endpoint -> Repo: actualizar
 Endpoint -> Endpoint: emit DISPOSITION_SET
 Endpoint --> enter_call_disposition: 200
 @enduml
