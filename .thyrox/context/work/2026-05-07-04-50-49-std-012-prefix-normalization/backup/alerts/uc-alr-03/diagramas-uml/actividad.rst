8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /alerts/{id}/ack/;
 :JWT + RBAC;
 :Cargar Alert;
 if (Cross-segmento?) then (si)
   :403; stop
 endif
 if (state != firing?) then (si)
   :409; stop
 endif
 :BEGIN tx;
 :actualizar Alert state, ack_*;
 :Audit ALERT_ACKNOWLEDGED;
 :COMMIT;
 :Suprimir notify;
 :200;
 stop
 @enduml

