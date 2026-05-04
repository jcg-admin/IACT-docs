5.1 Ejemplo IACT — UC_RPT_07 (Procesamiento de reportes programados)
--------------------------------------------------------------------

.. uml::

   @startuml
   allowmixing

   object ":Scheduler"     as Sch
   object ":ReporteProg"   as ReporteProg
   object ":SecRules"      as SecRules
   object ":BDAnalytics"   as BDAnalytics
   object ":BuzonInterno"  as BuzonInterno

   Sch -> ReporteProg : "1: [* reporte en\n   programados_pendientes]\n   ejecutar(reporte)"
   ReporteProg -> SecRules  : "1.1: verificar_permiso_owner()"
   ReporteProg -> BDAnalytics  : "1.2: aplicar_segmento(\n   owner, CNST_008)"
   ReporteProg -> BDAnalytics  : "1.3: ejecutar_query()"
   ReporteProg -> BuzonInterno  : "1.4: notificar(\n   owner, archivo_listo)"
   @enduml

----
