8.3 Estado de la llamada
========================

.. uml::

 @startuml
 [*] --> queued
 queued --> offered
 offered --> bridged : answer
 offered --> queued : decline
 offered --> abandoned : caller hangup
 bridged --> ended : hangup
 @enduml

