.. _uc-rpt-11-parte-08-diagrama-actividad-compartir:

8.2 Diagrama de actividad — Compartir SavedView
==================================================

.. uml::
 :caption: UC_RPT_11 — flujo de compartir vista.

 @startuml

 start
 :Invoker emite POST /api/v1/views/{id}/share/;
 :Servicio de Aplicacion verifica autenticacion;
 if (Autenticado?) then (no)
   :401 Unauthorized;
   stop
 endif
 :Verificar capability share_report;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar view + owner + target user;
 if (Owner != invoker?) then (si)
   :403 Forbidden (solo el owner comparte);
   stop
 endif
 if (expires_at en el pasado?) then (si)
   :400 Bad Request;
   stop
 endif

 :BEGIN TRANSACTION;
 :Persistir ShareEntry (state=active);
 :Audit REPORT_SHARED;
 :COMMIT;

 :InternalMailbox notify (si receptor permite);
 :201 Created;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-estados-share`.
 - :doc:`/arquitectura-tecnica/domain-model/saved-view`.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`.
