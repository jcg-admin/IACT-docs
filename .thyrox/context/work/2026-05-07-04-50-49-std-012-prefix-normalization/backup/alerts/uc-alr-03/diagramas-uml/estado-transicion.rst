8.3 Estado (transicion)
=======================

.. uml::

 @startuml
 [*] --> firing
 firing --> acknowledged : ack
 acknowledged --> resolved : metric normal
 firing --> resolved : metric normal
 resolved --> closed
 @enduml

