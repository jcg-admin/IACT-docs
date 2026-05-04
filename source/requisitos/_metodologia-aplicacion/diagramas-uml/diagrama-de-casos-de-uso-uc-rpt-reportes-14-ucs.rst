3. Diagrama de casos de uso — UC_RPT (reportes, 14 UCs)
=======================================================

.. uml::

   @startuml

   left to right direction
   actor Operador
   actor Supervisor

   rectangle "UC_RPT — Reportes (14 UCs)" {
     usecase "UC_RPT_01\nVer Dashboard"             as U01
     usecase "UC_RPT_02\nVer Métricas Tiempo Real"  as U02
     usecase "UC_RPT_03\nVer Reportes Históricos"   as U03
     usecase "UC_RPT_04\nExportar Reporte"          as U04
     usecase "UC_RPT_07\nProgramar Reporte"         as U07
     usecase "UC_RPT_08\nVer Programados"           as U08
     usecase "UC_RPT_09\nConfigurar Filtros"        as U09
     usecase "UC_RPT_10\nGuardar Vista"             as U10
     usecase "UC_RPT_11\nCompartir Reporte"         as U11
     usecase "UC_RPT_12\nReporte Agentes"           as U12
     usecase "UC_RPT_13\nReporte Colas"             as U13
     usecase "UC_RPT_14\nReporte Campañas"          as U14
   }

   Operador   --> U01
   Operador   --> U02
   Operador   --> U09
   Operador   --> U10

   Supervisor --> U03
   Supervisor --> U04
   Supervisor --> U07
   Supervisor --> U08
   Supervisor --> U11
   Supervisor --> U12
   Supervisor --> U13
   Supervisor --> U14

   U01 ..> U09 : <<include>>
   U03 ..> U09 : <<include>>
   U04 ..> U03 : <<include>>
   U07 ..> U03 : <<include>>
   @enduml

**Aplicación:** DOC-20 (UC_RPT + UC_NOT) usa este diagrama como
vista global de su dominio.

**Perspectiva:** DINÁMICA (POV usuario). **Audiencia:** Product
Owners / Analistas.

----
