8.4 Tail
========

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 queue "LogStore" as LogStore
 User -> Endpoint: GET tail (SSE)
 loop
   LogStore -> Endpoint: new entry
   Endpoint -> User: data
 end
 @enduml
