8.4 Diagrama de estado
======================

.. uml::
 :caption: Estado de conexion

 @startuml
 [*] --> Handshake
 Handshake --> Authorized : ok
 Handshake --> Closed : 401/403
 Authorized --> Streaming : suscrito
 Streaming --> Streaming : event / heartbeat
 Streaming --> Reconnecting : red caida
 Reconnecting --> Streaming : recuperado
 Reconnecting --> Closed : timeout
 Streaming --> Closed : user close
 Closed --> [*]
 @enduml
