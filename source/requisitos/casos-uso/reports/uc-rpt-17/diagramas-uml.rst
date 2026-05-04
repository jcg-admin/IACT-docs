.. _uc-rpt-17-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_17\nClientes Unicos IVR" as UC17
 }
 view_reports --> UC17
 UC17 ..> INC : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/clientes/?trimestre=;
 :JWT + RBAC (view_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 :Consultar Servicio de Reportes (sp_rpt_clientes);
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 con ReporteClientes (telefono_hashed);
 stop
 @enduml

8.3 Flujo de anonimizacion (ETL)
==================================

.. uml::

 @startuml
 component "tbl_historico_*\n(cTelefono_Origen raw)" as TblHistorico
 component "sp_etl_base_clientes\n(hash unidireccional)" as sp_etl_base_clientes
 component "base_ivr_clientes\n(telefono_hashed)" as DEST
 component "sp_rpt_clientes\n(solo lee hash)" as sp_rpt_clientes
 TblHistorico --> sp_etl_base_clientes
 sp_etl_base_clientes --> DEST
 DEST --> sp_rpt_clientes
 note right of sp_etl_base_clientes
   PII nunca almacenada
   en base analitica
 end note
 @enduml

8.4 Clases
==========

.. uml::

 @startuml
 class ClientesReportService {
   + get(trimestre, invoker) : ReporteClientes
 }
 class ServicioReportes {
   + clientes(trimestre) : list[dict]
 }
 class SegmentResolver
 ClientesReportService --> ServicioReportes
 ClientesReportService --> SegmentResolver
 @enduml
