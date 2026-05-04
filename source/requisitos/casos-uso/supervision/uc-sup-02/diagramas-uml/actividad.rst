8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST barge-in;
 :JWT + RBAC + segmento + reason;
 :Telephony bridge 3-way;
 :Audit CALL_BARGED;
 :200;
 stop
 @enduml

