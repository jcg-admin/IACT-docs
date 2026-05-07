.. _uc-rpt-10-parte-08-diagrama-actividad-crear:

8.2 Diagrama de actividad — Crear SavedView
=============================================

.. uml::
 :caption: UC_RPT_10 — flujo de creacion de vista guardada.

 @startuml

 start
 :Invoker emite POST /api/v1/me/views/;
 :Servicio de Aplicacion verifica autenticacion;
 if (Autenticado?) then (no)
   :401 Unauthorized;
   stop
 endif

 :Validar nombre, columns, segmento;
 if (Cross-segmento detectado?) then (si)
   :400 Bad Request;
   stop
 endif

 :Verificar limite de SavedViews del user;
 if (User excede 30?) then (si)
   :429 Too Many Views;
   stop
 endif

 :Persistir SavedView en SavedFilter Repo;
 :Audit VIEW_CREATED;
 :201 Created con SavedView;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-estados-saved-view`.
