.. _uc-rpt-11-parte-08-diagrama-actividad-aplicar:

8.3 Diagrama de actividad — Aplicar SavedView
================================================

.. uml::
 :caption: UC_RPT_11 — flujo de aplicacion de vista compartida o propia.

 @startuml

 start
 :GET con view_id;
 :Servicio de Aplicacion carga SavedView;
 if (Owner == invoker?) then (si)
   :Aplicar (segmento del invoker);
 else (no)
   :Buscar ShareEntry activo;
   if (Encontrado?) then (no)
     :403 sin acceso a la view;
     stop
   endif
   if (Expirado?) then (si)
     :403 SHARE_EXPIRED;
     stop
   endif
   :Aplicar (segmento del invoker);
 endif
 :200 OK con resultados;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-actividad-compartir`.
 - :doc:`diagrama-de-estados-share`.
 - :doc:`/arquitectura-tecnica/domain-model/saved-view`.
 - :doc:`/arquitectura-tecnica/domain-model/saved-filter`.
