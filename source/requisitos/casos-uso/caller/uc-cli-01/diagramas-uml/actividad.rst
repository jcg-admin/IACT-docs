8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Llamada al DID;
 :Telephony acepta;
 :Capturar caller_id;
 :Hash caller_id;
 :registrar CallSession;
 :Reproducir greeting;
 :Audit CALL_STARTED;
 :Pasar a IVR;
 stop
 @enduml

