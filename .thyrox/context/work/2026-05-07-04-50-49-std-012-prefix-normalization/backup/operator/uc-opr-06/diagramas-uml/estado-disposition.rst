8.3 Estado disposition
======================

.. uml::

 @startuml
 [*] --> pending : ACW start
 pending --> set : agente
 pending --> auto_no_disp : timeout
 set --> [*]
 auto_no_disp --> [*]
 @enduml

