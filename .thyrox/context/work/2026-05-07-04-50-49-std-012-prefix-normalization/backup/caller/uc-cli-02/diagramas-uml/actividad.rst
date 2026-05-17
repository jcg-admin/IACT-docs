8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Cargar IVR;
 :Reproducir nodo;
 repeat
   :Esperar input;
   if (Input recibido?) then (si)
     if (Opcion valida?) then (si)
       :Avanzar a hijo;
     else (no)
       :Re-prompt;
     endif
   else (timeout)
     :Re-prompt o fallback;
   endif
 repeat while (no llego a salida)
 :Ejecutar accion;
 stop
 @enduml

