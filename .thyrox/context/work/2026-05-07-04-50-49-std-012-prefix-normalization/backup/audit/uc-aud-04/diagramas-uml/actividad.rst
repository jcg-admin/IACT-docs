8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST template + period;
 :JWT + RBAC;
 :Validar;
 :Encolar Worker;
 :Audit QUEUED;
 :202;
 :Re-check permiso;
 :Ejecutar template queries;
 :Sanitize;
 :Firmar HMAC;
 :Upload storage + URL;
 :Audit GENERATED + hash;
 :Mailbox notify;
 stop
 @enduml

