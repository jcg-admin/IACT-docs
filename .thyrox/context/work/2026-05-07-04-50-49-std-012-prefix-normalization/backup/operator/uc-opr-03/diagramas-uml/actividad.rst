8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST outbound;
 :JWT + RBAC;
 :Validar destination;
 if (En lista permitida?) then (no)
   :400 BLOCKED; stop
 endif
 :Telephony dial;
 if (Pickup?) then (si)
   :Bridge + state busy;
   :Audit OUTBOUND_INITIATED;
   :200;
 else (no)
   :State available;
   :Audit NO_ANSWER;
 endif
 stop
 @enduml

