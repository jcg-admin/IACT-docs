.. _uc-rpt-17-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Clientes Unicos IVR
=============================================================

.. uml::
 :caption: UC_RPT_17 — flujo de consulta de reporte de clientes.

 @startuml

 start
 :GET /api/v1/reportes/clientes/ con trimestre;
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
 :Consultar Servicio de Reportes (sp_rpt_clientes);
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 OK con ReporteClientes (telefono_hashed);
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-flujo-de-anonimizacion-etl`.
 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
