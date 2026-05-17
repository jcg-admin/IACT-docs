.. _uc-alr-03-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Acknowledge alerta
================================================

.. uml::
 :caption: UC_ALR_03 — flujo de acknowledge de alerta.

 @startuml

 start
 :Invoker emite POST /api/v1/alerts/{id}/ack/;
 :Servicio de Aplicacion verifica capability
   acknowledge_alert;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Cargar Alert por id (AlertRepo);
 if (Alert no encontrada?) then (si)
   :404 Not Found;
   stop
 endif

 :Verificar scope de la alerta es
   accesible al user (segmentos);
 if (Cross-segment violation?) then (si)
   :403 sin acceso al segmento;
   stop
 endif

 :Validar state actual = firing;
 if (state != firing?) then (si)
   :409 Conflict (ya acknowledged
     o resolved);
   stop
 endif

 :BEGIN TRANSACTION;
 :UPDATE Alert
   SET state='acknowledged',
       ack_by=invoker,
       ack_at=now();
 :Audit ALERT_ACKNOWLEDGED;
 :COMMIT;

 :Suprimir notificaciones pendientes
   para esta Alert;
 :200 OK con Alert actualizada;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
