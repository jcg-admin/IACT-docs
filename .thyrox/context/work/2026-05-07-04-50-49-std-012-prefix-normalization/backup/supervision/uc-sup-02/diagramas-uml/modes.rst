8.3 Modes
=========

.. uml::

 @startuml
 [*] --> active
 active --> takeover : disconnect agent
 active --> ended : leave
 takeover --> ended
 ended --> [*]
 @enduml

