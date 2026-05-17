8.3 Componentes
===============

.. uml::

 @startuml
 component "Endpoint" as Endpoint
 component "CallSessionRepo" as Callsessionrepo
 component "Sanitizer" as Sanitizer
 Endpoint --> Callsessionrepo
 Endpoint --> Sanitizer
 @enduml

