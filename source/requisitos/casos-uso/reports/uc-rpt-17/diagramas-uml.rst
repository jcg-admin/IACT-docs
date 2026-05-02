.. _uc-rpt-17-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 left to right direction
 actor "Analista\nde Datos" as USR
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_17\nClientes Unicos IVR" as UC17
 }
 USR --> UC17
 UC17 ..> INC : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 start
 :GET /api/v1/reportes/clientes/?trimestre=;
 :JWT + RBAC (view_unique_clients_reports);
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
 !include ../../_static/plantuml-styles.puml
 component "tbl_historico_*\n(cTelefono_Origen raw)" as SRC
 component "sp_etl_base_clientes\n(hash unidireccional)" as ETL
 component "base_ivr_clientes\n(telefono_hashed)" as DEST
 component "sp_rpt_clientes\n(solo lee hash)" as RPT
 SRC --> ETL
 ETL --> DEST
 DEST --> RPT
 note right of ETL
   PII nunca almacenada
   en base analitica
 end note
 @enduml

8.4 Clases
==========

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
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
