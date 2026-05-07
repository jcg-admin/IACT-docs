8.3 Estado de la llamada
========================

.. uml::

 @startuml
 [*] --> bridged
 bridged --> on_hold : hold
 on_hold --> bridged : unhold
 bridged --> ended : hangup
 on_hold --> ended : caller hangup
 ended --> [*]
 @enduml

