.. _uc-rpt-15-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Analista\nde Datos" as USR
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_15\nReporte Transferencias" as UC15
   usecase "Ver por segmento" as SEG
 }
 USR --> UC15
 UC15 ..> INC : <<include>>
 UC15 ..> SEG : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/transferencias/?trimestre=;
 :JWT + RBAC (view_transfer_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 :Consultar sp_rpt_centros_transferencia;
 :Consultar sp_rpt_centros_xsegmento;
 :Construir ReporteTransferencias;
 :Cache write TTL 300s;
 :200;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class TransferenciasReportService {
   + get(trimestre, invoker) : ReporteTransferencias
 }
 class ServicioReportes {
   + centros_transferencia(trimestre) : list[dict]
   + centros_xsegmento(trimestre) : list[dict]
 }
 class SegmentResolver
 TransferenciasReportService --> ServicioReportes
 TransferenciasReportService --> SegmentResolver
 @enduml
