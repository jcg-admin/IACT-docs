8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /audit/;
 :JWT + RBAC;
 :Validar;
 :Query AuditRepo + cursor;
 :Sanitize;
 :Build cursor;
 :Meta-audit GENERAL_AUDIT_QUERIED;
 if (Meta-audit ok?) then (no)
   :503; stop
 endif
 :200;
 stop
 @enduml

