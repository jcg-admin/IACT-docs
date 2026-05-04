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
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_01\nVer Dashboard IVR" as R01
   usecase "UC_RPT_02\nVer Metricas\nTiempo Real" as R02
   usecase "UC_RPT_03\nVer Reportes\nHistoricos" as R03
   usecase "UC_RPT_04\nExportar Reporte" as R04
   usecase "UC_RPT_07\nProgramar Reporte" as R07
   usecase "UC_RPT_08\nVer Reportes\nProgramados" as R08
   usecase "UC_RPT_10\nGuardar Vista" as R10
   usecase "UC_RPT_11\nCompartir Reporte" as R11
   usecase "UC_RPT_12\nReporte de Agentes\n(sp_rpt_centros_xsegmento)" as R12
   usecase "UC_RPT_13\nReporte de Colas\n(sp_rpt_llamadas_abandonadas)" as R13
   usecase "UC_RPT_14\nReporte de Campanas" as R14
   usecase "UC_RPT_15\nReporte de\nTransferencias\n(sp_rpt_centros_transferencia)" as R15
   usecase "UC_RPT_16\nReporte de Menus IVR\n(sp_rpt_menu_redirigidos)" as R16
   usecase "UC_RPT_17\nReporte de Clientes\nUnicos\n(sp_rpt_clientes)" as R17
 }

 view_dashboard --> R01
 view_kpis --> R02
 view_reports --> R03
 export_csv --> R04
 schedule_report --> R07
 schedule_report --> R08
 save_view --> R10
 share_report --> R11
 view_reports --> R12
 view_reports --> R13
 view_reports --> R14
 view_reports --> R15
 view_reports --> R16
 view_reports --> R17

 R01 ..> INC : <<include>>
 R02 ..> INC : <<include>>
 R03 ..> INC : <<include>>
 R12 ..> INC : <<include>>
 R13 ..> INC : <<include>>
 R14 ..> INC : <<include>>
 R15 ..> INC : <<include>>
 R16 ..> INC : <<include>>
 R17 ..> INC : <<include>>

 R03 ..> R04 : <<extend>>
 R03 ..> R07 : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
