8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Insert QueueEntry;
 :Music on hold;
 repeat
   :Update position;
   if (Wait > X?) then (si)
     :Ofrecer callback;
   endif
 repeat while (no asignado)
 :Bridge agente;
 :Remove QueueEntry;
 stop
 @enduml

