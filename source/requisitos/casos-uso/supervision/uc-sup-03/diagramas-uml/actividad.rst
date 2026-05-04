8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST broadcast;
 :JWT + RBAC;
 :Validar target;
 :Resolver recipients;
 :Bulk registrar mailbox;
 if (Urgente?) then (si)
   :SSE push;
 endif
 :Audit BROADCAST_SENT;
 :200;
 stop
 @enduml

