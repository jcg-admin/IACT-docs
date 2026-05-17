.. _uc-alr-02-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Listar alertas activas
====================================================

.. uml::
 :caption: UC_ALR_02 — flujo de listado de alertas activas.

 @startuml

 start
 :Invoker emite GET /api/v1/alerts/active/;
 :Servicio de Aplicacion verifica capability
   view_alerts;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Resolver segmentos del usuario
   (UC_INC_RPT_01);
 :Query AlertRepo
   WHERE state IN (firing, acknowledged)
   AND scope IN segmentos_user;
 :Ordenar por severity DESC, fired_at DESC;
 :200 OK con lista paginada;
 :Interfaz de Usuario renderiza
   con auto-refresh cada 10s;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`.
