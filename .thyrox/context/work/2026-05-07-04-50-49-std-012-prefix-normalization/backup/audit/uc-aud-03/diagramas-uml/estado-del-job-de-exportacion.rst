8.3 Estado del job de exportacion
===================================

.. uml::

 @startuml
 [*] --> Queued
 Queued --> Processing : worker disponible
 Processing --> Done : archivo generado
 Processing --> Failed : error I/O
 Done --> [*] : notificacion enviada
 Failed --> Queued : reintento automatico
 @enduml

