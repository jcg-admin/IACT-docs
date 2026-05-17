8.2 Actividad (crear)
=====================

.. uml::

 @startuml
 start
 :POST /api/me/views/;
 if (JWT?) then (no)
   :401; stop
 endif
 :Validar nombre + columns + segmento;
 if (Cross-segmento?) then (si)
   :400; stop
 endif
 if (User > 30?) then (si)
   :429; stop
 endif
 :registrar;
 :Audit VIEW_CREATED;
 :201;
 stop
 @enduml

