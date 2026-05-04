8.3 Diagrama de estado
======================

.. uml::
 :caption: ExportJob

 @startuml
 [*] --> queued
 queued --> running : worker pickup
 queued --> cancelled : eliminar running --> done : ok
 running --> failed : error
 running --> cancelled : cancellation_requested
 done --> expired : 24h
 failed --> [*]
 cancelled --> [*]
 expired --> [*]
 @enduml

