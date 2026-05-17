8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Offer ring;
 if (Agente acepta?) then (no)
   :Decline; stop
 endif
 :Bridge;
 :State busy;
 :Audit CALL_ANSWERED;
 :200;
 stop
 @enduml

