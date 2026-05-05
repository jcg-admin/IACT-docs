.. meta::
 :artefacto: AT_UC_MOD_REPORTS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_reports:

=========================================
MOD_Reports — Reportes IVR: UC por Modulo
=========================================

Módulo principal de análisis. 16 UCs de reporte + 1 UC
``<<include>>`` compartido (Resolver Segmento). Todos los
reportes filtran datos por segmento IVR del usuario vía
``UC_INC_RPT_01``.

.. uml::
 :caption: MOD_Reports — actores canónicos (roles RBAC) y
           UCs operativos del módulo.

 @startuml
 left to right direction

 actor Operator
 actor Supervisor

 Operator <|-- Supervisor

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_01\nVer Dashboard IVR" as VER_DASHBOARD_IVR
   usecase "UC_RPT_02\nVer Metricas\nTiempo Real" as VER_METRICAS_TIEMPO_REAL
   usecase "UC_RPT_03\nVer Reportes\nHistoricos" as VER_REPORTES_HISTORICOS
   usecase "UC_RPT_04\nExportar Reporte" as EXPORTAR_REPORTE
   usecase "UC_RPT_07\nProgramar Reporte" as PROGRAMAR_REPORTE
   usecase "UC_RPT_08\nVer Reportes\nProgramados" as VER_REPORTES_PROGRAMADOS
   usecase "UC_RPT_10\nGuardar Vista" as GUARDAR_VISTA
   usecase "UC_RPT_11\nCompartir Reporte" as COMPARTIR_REPORTE
   usecase "UC_RPT_12\nReporte de Agentes" as REPORTE_AGENTES
   usecase "UC_RPT_13\nReporte de Colas" as REPORTE_COLAS
   usecase "UC_RPT_14\nReporte de Campanas" as REPORTE_CAMPANAS
   usecase "UC_RPT_15\nReporte de\nTransferencias" as REPORTE_TRANSFERENCIAS
   usecase "UC_RPT_16\nReporte de Menus IVR" as REPORTE_MENUS_IVR
   usecase "UC_RPT_17\nReporte de Clientes\nUnicos" as REPORTE_CLIENTES_UNICOS
 }

 Operator --> VER_DASHBOARD_IVR
 Operator --> VER_METRICAS_TIEMPO_REAL
 Operator --> VER_REPORTES_HISTORICOS
 Operator --> REPORTE_AGENTES
 Operator --> REPORTE_COLAS
 Operator --> REPORTE_CAMPANAS
 Operator --> REPORTE_TRANSFERENCIAS
 Operator --> REPORTE_MENUS_IVR
 Operator --> REPORTE_CLIENTES_UNICOS
 Operator --> GUARDAR_VISTA
 Operator --> COMPARTIR_REPORTE

 Supervisor --> EXPORTAR_REPORTE
 Supervisor --> PROGRAMAR_REPORTE
 Supervisor --> VER_REPORTES_PROGRAMADOS

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

 note right of MOD_Reports
   Codenames RBAC requeridos:
     view_dashboard, view_kpis, view_reports
     → vistas (Operator)
     export_csv, export_pdf, export_excel
     → exportacion (Supervisor)
     schedule_report → programacion (Supervisor)
     save_view, share_report → colaboracion
 end note

 @enduml

Lectura del diagrama
====================

- ``Operator`` (AGR-001) ejecuta los UCs de **lectura**:
  dashboards, KPIs, reportes históricos y los 6 reportes
  específicos por dominio (agentes, colas, campañas,
  transferencias, menús IVR, clientes únicos).
- ``Supervisor`` (AGR-002,003,004) hereda de
  ``Operator`` y agrega capacidad de **exportar** y
  **programar** reportes.
- ``UC_INC_RPT_01 Resolver Segmento`` es ``<<include>>``
  obligatorio en todo UC de lectura — implementa
  CNST-008 (filtro por segmento del invocador).
- ``UC_RPT_03`` puede extenderse con
  ``UC_RPT_04 Exportar`` y ``UC_RPT_07 Programar``
  (relación ``<<extend>>``).

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-04-exportar-reporte`
