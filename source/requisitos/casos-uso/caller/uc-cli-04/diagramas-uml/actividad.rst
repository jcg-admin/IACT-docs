8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Ofrecer callback;
 if (Cliente acepta?) then (no)
   :Sigue cola;
   stop
 endif
 :Capturar numero;
 if (DNC?) then (si)
   :Mensaje rechazo;
   stop
 endif
 :Hash + registrar CallbackEntry;
 :Audit;
 :Confirmar + hangup;
 stop
 @enduml

