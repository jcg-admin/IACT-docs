8.3 Estado overall
==================

.. uml::

 @startuml
 [*] --> green
 green --> yellow : 1+ deg
 yellow --> red : critical
 red --> yellow : recover
 yellow --> green : recover
 @enduml

