8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/transferencias/?trimestre=;
 :JWT + RBAC (view_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 :Consultar sp_rpt_centros_transferencia;
 :Consultar sp_rpt_centros_xsegmento;
 :Construir ReporteTransferencias;
 :Cache write TTL 300s;
 :200;
 stop
 @enduml

