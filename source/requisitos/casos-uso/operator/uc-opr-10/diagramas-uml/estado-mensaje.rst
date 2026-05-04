8.3 Estado mensaje
==================

.. uml::

 @startuml
 [*] --> sent
 sent --> delivered
 delivered --> read : POST read
 read --> archived
 archived --> [*]
 @enduml

