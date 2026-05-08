8.4 Estado
==========

.. uml::

 @startuml
 [*] --> active : crear
 active --> degraded : columna deprecada
 degraded --> active : columna restaurada
 active --> [*] : delete
 @enduml
