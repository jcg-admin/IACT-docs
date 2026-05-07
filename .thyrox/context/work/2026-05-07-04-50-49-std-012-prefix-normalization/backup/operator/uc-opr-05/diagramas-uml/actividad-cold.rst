8.3 Actividad cold
==================

.. uml::

 @startuml
 start
 :POST transfer cold;
 :Direct bridge B;
 :Disconnect A;
 :Audit;
 :200;
 stop
 @enduml

