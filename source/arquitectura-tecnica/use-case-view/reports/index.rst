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
   usecase "UC_RPT_02\nVer Metricas\nTiempo Real" as VER_METRICAS_TIEMPO_REAL   usecase "UC_RPT_03\nVer Reportes\nHistoricos\n.. extension points ..\nExportar / Programar / Filtrar" as VER_REPORTES_HISTORICOS
   usecase "UC_RPT_04\nExportar Reporte" as EXPORTAR_REPORTE
   usecase "UC_RPT_07\nProgramar Reporte" as PROGRAMAR_REPORTE
   usecase "UC_RPT_08\nVer Reportes\nProgramados" as VER_REPORTES_PROGRAMADOS
   usecase "UC_RPT_09\nConfigurar Filtros" as CONFIGURAR_FILTROS
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
 Operator --> CONFIGURAR_FILTROS

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

 EXPORTAR_REPORTE ..> VER_REPORTES_HISTORICOS : <<extend>>
 PROGRAMAR_REPORTE ..> VER_REPORTES_HISTORICOS : <<extend>>
 CONFIGURAR_FILTROS ..> VER_REPORTES_HISTORICOS : <<extend>>

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

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/base-report-service`
  — clase abstracta raíz (template-method
  ``apply_segment_filter`` para CNST-008).
- :doc:`/arquitectura-tecnica/domain-model/agent-report-service`
  (UC_RPT_12 Reporte de Agentes).
- :doc:`/arquitectura-tecnica/domain-model/abandonment-report-service`
  (UC_RPT_13 Reporte de Colas).
- :doc:`/arquitectura-tecnica/domain-model/caller-report-service`
  (UC_RPT_17 Clientes Únicos).
- :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service`
  (UC_RPT_16 Reporte de Menús IVR).
- :doc:`/arquitectura-tecnica/domain-model/transfer-report-service`
  (UC_RPT_15 Reporte de Transferencias).
- :doc:`/arquitectura-tecnica/domain-model/scheduled-report-list-service`
  (UC_RPT_07/08 programación y listado).
- :doc:`/arquitectura-tecnica/domain-model/scheduled-report`
  / :doc:`/arquitectura-tecnica/domain-model/scheduled-report-repo`.
- :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
  / :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
  / :doc:`/arquitectura-tecnica/domain-model/filter-validator`.
- :doc:`/arquitectura-tecnica/domain-model/saved-filter`
  (UC_RPT_09 Configurar Filtros)
  / :doc:`/arquitectura-tecnica/domain-model/saved-view`
  (UC_RPT_10 Guardar Vista).
- :doc:`/arquitectura-tecnica/domain-model/historical-report`
  / :doc:`/arquitectura-tecnica/domain-model/bucket`
  / :doc:`/arquitectura-tecnica/domain-model/comparative`
  / :doc:`/arquitectura-tecnica/domain-model/column-catalog`.
- :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`.

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_INC_RPT_01 </requisitos/casos-uso/reports/uc-inc-rpt-01/index>`
   - UC_INC_RPT_01 — Resolver Segmento
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_01 </requisitos/casos-uso/reports/uc-rpt-01/index>`
   - Ver Dashboard
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_02 </requisitos/casos-uso/reports/uc-rpt-02/index>`
   - Ver Metricas en Tiempo Real
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_03 </requisitos/casos-uso/reports/uc-rpt-03/index>`
   - Ver Reportes Historicos
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_04 </requisitos/casos-uso/reports/uc-rpt-04/index>`
   - Exportar Reporte
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-04/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_07 </requisitos/casos-uso/reports/uc-rpt-07/index>`
   - Programar Reporte
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-07/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_08 </requisitos/casos-uso/reports/uc-rpt-08/index>`
   - Ver Reportes Programados
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-08/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_09 </requisitos/casos-uso/reports/uc-rpt-09/index>`
   - Configurar Filtros
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-09/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_10 </requisitos/casos-uso/reports/uc-rpt-10/index>`
   - Guardar Vista
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_11 </requisitos/casos-uso/reports/uc-rpt-11/index>`
   - Compartir Reporte
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_12 </requisitos/casos-uso/reports/uc-rpt-12/index>`
   - Reporte de Agentes
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_13 </requisitos/casos-uso/reports/uc-rpt-13/index>`
   - Reporte de Colas
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_14 </requisitos/casos-uso/reports/uc-rpt-14/index>`
   - Reporte de Campanas
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_15 </requisitos/casos-uso/reports/uc-rpt-15/index>`
   - Reporte de Transferencias
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_16 </requisitos/casos-uso/reports/uc-rpt-16/index>`
   - Reporte de Menus IVR
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_RPT_17 </requisitos/casos-uso/reports/uc-rpt-17/index>`
   - Reporte de Clientes Unicos
   - :doc:`Diagrama </requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-04-exportar-reporte`
