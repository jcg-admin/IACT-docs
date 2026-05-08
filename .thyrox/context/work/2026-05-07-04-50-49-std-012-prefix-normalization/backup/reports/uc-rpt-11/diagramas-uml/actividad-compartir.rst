8.2 Actividad (compartir)
=========================

.. uml::

 @startuml
 start
 :POST share;
 if (JWT?) then (no)
   :401; stop
 endif
 if (share_report?) then (no)
   :403; stop
 endif
 :Validar view + owner + target;
 if (Owner != invoker?) then (si)
   :403; stop
 endif
 if (expires_at en pasado?) then (si)
   :400; stop
 endif
 :registrar ShareEntry;
 :Audit REPORT_SHARED;
 :Mailbox notify (si receptor permite);
 :201;
 stop
 @enduml

