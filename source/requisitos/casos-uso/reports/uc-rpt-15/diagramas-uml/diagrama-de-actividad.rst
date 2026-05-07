.. _uc-rpt-15-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Transferencias
=======================================================

.. uml::
 :caption: UC_RPT_15 — flujo de consulta de reporte de transferencias.

 @startuml

 start
 :GET /api/v1/reportes/transferencias/ con trimestre;
 :Servicio de Aplicacion verifica capability view_reports;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif
 :Resolver segmento (UC_INC_RPT_01);
 :Cache lookup;
 if (Cache HIT?) then (si)
   :Return cached;
   stop
 endif
 :Consultar sp_rpt_centros_transferencia;
 :Consultar sp_rpt_centros_xsegmento;
 :Construir ReporteTransferencias;
 :Cache write TTL 300s;
 :200 OK;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
