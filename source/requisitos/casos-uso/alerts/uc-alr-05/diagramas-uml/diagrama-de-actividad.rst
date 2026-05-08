.. _uc-alr-05-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Suscribirse a alertas
===================================================

.. uml::
 :caption: UC_ALR_05 — flujo de creacion de Subscription.

 @startuml

 start
 :Invoker emite POST /api/v1/alerts/subscriptions/;
 :Servicio de Aplicacion verifica capability
   manage_alert_subscriptions
   (own o admin para terceros);
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar type + scope de la subscription;
 if (Cross-segmento detectado?) then (si)
   :400 sin permiso al segmento;
   stop
 endif
 if (Duplicada — misma combinacion
     user+rule+channel?) then (si)
   :409 Conflict;
   stop
 endif

 :BEGIN TRANSACTION;
 :INSERT Subscription (state=active);
 :Audit ALERT_SUBSCRIPTION_CREATED;
 :COMMIT;

 :201 Created con Subscription;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/subscription`.
