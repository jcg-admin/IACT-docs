8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST monitor;
 :JWT + RBAC;
 :Validar segmento;
 if (Reason ok?) then (no)
   :400; stop
 endif
 :Telephony bridge listen;
 :Tono audible al agente;
 :Audit CALL_MONITORED;
 :200;
 stop
 @enduml

