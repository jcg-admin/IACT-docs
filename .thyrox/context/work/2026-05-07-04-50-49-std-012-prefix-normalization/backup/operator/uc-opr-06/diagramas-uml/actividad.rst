8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST disposition;
 :JWT + ownership;
 :Validar code + notes;
 if (do_not_call?) then (si)
   :Add DNC list;
 endif
 if (follow_up?) then (si)
   :Crear CallbackEntry;
 endif
 :actualizar CallSession;
 :Audit;
 :State ACW → available;
 :200;
 stop
 @enduml

