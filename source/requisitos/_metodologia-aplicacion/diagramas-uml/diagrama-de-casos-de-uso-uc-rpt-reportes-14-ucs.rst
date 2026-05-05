3. Diagrama de casos de uso — UC_RPT (reportes, 14 UCs)
=======================================================

.. uml::

   @startuml

   left to right direction
   actor Operador
   actor Supervisor

   rectangle "UC_RPT — Reportes (14 UCs)" {
     usecase "UC_RPT_01\nVer Dashboard"             as VER_DASHBOARD_IVR
     usecase "UC_RPT_02\nVer Métricas Tiempo Real"  as VER_METRICAS_TIEMPO_REAL
     usecase "UC_RPT_03\nVer Reportes Históricos"   as VER_REPORTES_HISTORICOS
     usecase "UC_RPT_04\nExportar Reporte"          as EXPORTAR_REPORTE
     usecase "UC_RPT_07\nProgramar Reporte"         as PROGRAMAR_REPORTE
     usecase "UC_RPT_08\nVer Programados"           as VER_REPORTES_PROGRAMADOS
     usecase "UC_RPT_09\nConfigurar Filtros"        as CONFIGURAR_FILTROS
     usecase "UC_RPT_10\nGuardar Vista"             as GUARDAR_VISTA
     usecase "UC_RPT_11\nCompartir Reporte"         as COMPARTIR_REPORTE
     usecase "UC_RPT_12\nReporte Agentes"           as REPORTE_AGENTES
     usecase "UC_RPT_13\nReporte Colas"             as REPORTE_COLAS
     usecase "UC_RPT_14\nReporte Campañas"          as REPORTE_CAMPANAS
   }

   Operador   --> VER_DASHBOARD_IVR
   Operador   --> VER_METRICAS_TIEMPO_REAL
   Operador   --> CONFIGURAR_FILTROS
   Operador   --> GUARDAR_VISTA

   Supervisor --> VER_REPORTES_HISTORICOS
   Supervisor --> EXPORTAR_REPORTE
   Supervisor --> PROGRAMAR_REPORTE
   Supervisor --> VER_REPORTES_PROGRAMADOS
   Supervisor --> COMPARTIR_REPORTE
   Supervisor --> REPORTE_AGENTES
   Supervisor --> REPORTE_COLAS
   Supervisor --> REPORTE_CAMPANAS

   VER_DASHBOARD_IVR ..> CONFIGURAR_FILTROS : <<include>>
   VER_REPORTES_HISTORICOS ..> CONFIGURAR_FILTROS : <<include>>
   EXPORTAR_REPORTE ..> VER_REPORTES_HISTORICOS : <<include>>
   PROGRAMAR_REPORTE ..> VER_REPORTES_HISTORICOS : <<include>>
   @enduml

**Aplicación:** DOC-20 (UC_RPT + UC_NOT) usa este diagrama como
vista global de su dominio.

**Perspectiva:** DINÁMICA (POV usuario). **Audiencia:** Product
Owners / Analistas.
