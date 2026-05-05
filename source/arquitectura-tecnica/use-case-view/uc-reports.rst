.. meta::
 :artefacto: AT_UC_MOD_REPORTS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_reports:

=========================================
MOD_Reports — Reportes IVR: UC por Modulo
=========================================

MOD_Reports — Reportes IVR
=============================

Modulo principal de analisis. 16 UCs de reporte + 1 UC <<include>>
compartido (Resolver Segmento). Todos los reportes filtran datos
por segmento IVR del usuario via ``UC_INC_RPT_01``.

.. uml::
 :caption: Figura 20 — MOD_Reports: casos de uso

 @startuml
 left to right direction

 actor "view_dashboard" as view_dashboard
 actor "view_kpis" as view_kpis
 actor "view_reports" as view_reports
 actor "export_csv\n(export_pdf/excel)" as export_csv
 actor "schedule_report" as schedule_report
 actor "save_view" as save_view
 actor "share_report" as share_report

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as ResolverSegmento
   usecase "UC_RPT_01\nVer Dashboard IVR" as VER_DASHBOARD_IVR
   usecase "UC_RPT_02\nVer Metricas\nTiempo Real" as VER_METRICAS_TIEMPO_REAL
   usecase "UC_RPT_03\nVer Reportes\nHistoricos" as VER_REPORTES_HISTORICOS
   usecase "UC_RPT_04\nExportar Reporte" as EXPORTAR_REPORTE
   usecase "UC_RPT_07\nProgramar Reporte" as PROGRAMAR_REPORTE
   usecase "UC_RPT_08\nVer Reportes\nProgramados" as VER_REPORTES_PROGRAMADOS
   usecase "UC_RPT_10\nGuardar Vista" as GUARDAR_VISTA
   usecase "UC_RPT_11\nCompartir Reporte" as COMPARTIR_REPORTE
   usecase "UC_RPT_12\nReporte de Agentes\n(sp_rpt_centros_xsegmento)" as REPORTE_AGENTES
   usecase "UC_RPT_13\nReporte de Colas\n(sp_rpt_llamadas_abandonadas)" as REPORTE_COLAS
   usecase "UC_RPT_14\nReporte de Campanas" as REPORTE_CAMPANAS
   usecase "UC_RPT_15\nReporte de\nTransferencias\n(sp_rpt_centros_transferencia)" as REPORTE_TRANSFERENCIAS
   usecase "UC_RPT_16\nReporte de Menus IVR\n(sp_rpt_menu_redirigidos)" as REPORTE_MENUS_IVR
   usecase "UC_RPT_17\nReporte de Clientes\nUnicos\n(sp_rpt_clientes)" as REPORTE_CLIENTES_UNICOS
 }

 view_dashboard --> VER_DASHBOARD_IVR
 view_kpis --> VER_METRICAS_TIEMPO_REAL
 view_reports --> VER_REPORTES_HISTORICOS
 export_csv --> EXPORTAR_REPORTE
 schedule_report --> PROGRAMAR_REPORTE
 schedule_report --> VER_REPORTES_PROGRAMADOS
 save_view --> GUARDAR_VISTA
 share_report --> COMPARTIR_REPORTE
 view_reports --> REPORTE_AGENTES
 view_reports --> REPORTE_COLAS
 view_reports --> REPORTE_CAMPANAS
 view_reports --> REPORTE_TRANSFERENCIAS
 view_reports --> REPORTE_MENUS_IVR
 view_reports --> REPORTE_CLIENTES_UNICOS

 VER_DASHBOARD_IVR ..> INC : <<include>>
 VER_METRICAS_TIEMPO_REAL ..> INC : <<include>>
 VER_REPORTES_HISTORICOS ..> INC : <<include>>
 REPORTE_AGENTES ..> INC : <<include>>
 REPORTE_COLAS ..> INC : <<include>>
 REPORTE_CAMPANAS ..> INC : <<include>>
 REPORTE_TRANSFERENCIAS ..> INC : <<include>>
 REPORTE_MENUS_IVR ..> INC : <<include>>
 REPORTE_CLIENTES_UNICOS ..> INC : <<include>>

 VER_REPORTES_HISTORICOS ..> EXPORTAR_REPORTE : <<extend>>
 VER_REPORTES_HISTORICOS ..> PROGRAMAR_REPORTE : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
