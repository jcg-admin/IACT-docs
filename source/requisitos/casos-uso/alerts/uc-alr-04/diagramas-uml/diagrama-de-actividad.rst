.. _uc-alr-04-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar historial de alertas
============================================================

.. uml::
 :caption: UC_ALR_04 — flujo de consulta historica.

 @startuml

 start
 :Invoker emite GET /api/v1/alerts/history
   con filtros + period;
 :Servicio de Aplicacion verifica capability
   view_alert_history;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Resolver segmentos accesibles
   (UC_INC_RPT_01);
 :Validar range del period <= 1 ano;
 if (Range invalido?) then (si)
   :422 range excedido;
   stop
 endif

 :Cache lookup
   key=hash(filters, period, user_segments);
 if (Cache HIT?) then (si)
   :Return cached summary;
   :200 OK;
   stop
 endif

 :Query AlertRepo state IN (resolved, closed)
   AND scope IN segmentos
   AND fired_at WITHIN period;
 :TimingCalculator.compute_ttak(rows)
   (time-to-acknowledge);
 :TimingCalculator.compute_ttar(rows)
   (time-to-resolve);
 :Build summary con stats agregadas;
 :Cache write con TTL apropiado;
 :200 OK con summary + rows;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator`.
