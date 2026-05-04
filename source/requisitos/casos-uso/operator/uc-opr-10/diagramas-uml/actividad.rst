8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /me/mailbox;
 :JWT;
 :Query mailbox;
 :Filter status;
 :200;
 stop
 @enduml

