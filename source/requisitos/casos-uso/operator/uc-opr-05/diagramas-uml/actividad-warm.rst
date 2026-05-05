8.2 Actividad warm
==================

.. uml::

 @startuml
 start
 :POST transfer warm;
 :Consult B;
 if (B accepts?) then (no)
   :Cancel; stop
 endif
 :Bridge caller-B;
 :Disconnect A;
 :Audit;
 :200;
 stop
 @enduml

