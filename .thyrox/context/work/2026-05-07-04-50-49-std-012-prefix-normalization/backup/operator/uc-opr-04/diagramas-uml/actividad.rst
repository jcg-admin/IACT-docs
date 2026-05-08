8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST hold;
 :Validar ownership;
 :Telephony.hold;
 :actualizar session;
 :Audit CALL_HELD;
 :200;
 stop
 @enduml

