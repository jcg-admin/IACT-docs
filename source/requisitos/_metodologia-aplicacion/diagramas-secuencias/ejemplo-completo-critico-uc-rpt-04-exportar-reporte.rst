11. Ejemplo completo crítico — UC_RPT_04 (Exportar reporte)
===========================================================

Combina todo: instancia + alternativas + creación de objeto +
loop + asincrónico + auditoría inmutable.

.. uml::

   @startuml

   actor Supervisor
   participant ":Frontend"      as Frontend
   participant ":Backend"       as Backend
   participant ":SecRules"      as SecRules
   participant ":Reporte"       as Reporte
   participant ":BDAnalytics"   as BDAnalytics
   participant ":ExportQueue"   as ExportQueue
   participant ":BuzonInterno"  as BuzonInterno
   participant ":AuditLog"      as AuditLog

   == UC_RPT_04: Exportar reporte ==

   Supervisor -> Frontend : clic "Exportar (Excel)"
   Frontend -> Backend          : POST /api/reports/{id}/export?fmt=xlsx
   activate Backend

   Backend -> SecRules : verificarPermiso(export_excel)\n           + throttling CNST_020
   alt [permiso denegado o throttling]
     SecRules --> Backend : denegado
     Backend ->> AuditLog : registrar(EXPORT_DENIED)
     Backend --> Frontend  : 403
     Frontend --> Supervisor : ✗ "Sin permiso o límite del día"
     deactivate Backend
   else [autorizado]
     SecRules --> Backend : ok + segmento

     Backend -> Reporte : aplicarFiltrosSegmento(BR_012, CNST_008)
     activate Reporte
     Reporte -> BDAnalytics : SELECT con filtro
     activate BDAnalytics
     BDAnalytics --> Reporte : filas
     deactivate BDAnalytics

     alt [filas ≤ 10k → síncrono]
       create participant ":Archivo" as Archivo
       Reporte -> Archivo : <<create>> generarXLSX(filas)
       activate Archivo
       Archivo --> Reporte : archivo
       deactivate Archivo
       Reporte ->> AuditLog : registrar(EXPORT_OK)
       Reporte --> Backend  : url_descarga
       Backend --> Frontend  : url
       Frontend --> Supervisor : descarga directa
       deactivate Reporte
     else [filas > 10k → asincrónico CNST_019]
       Reporte -> ExportQueue : encolar(filtros, fmt, supervisor_id)
       activate ExportQueue
       ExportQueue --> Reporte : job_id
       deactivate ExportQueue
       Reporte ->> AuditLog : registrar(EXPORT_QUEUED)
       Reporte --> Backend  : job_id
       Backend --> Frontend  : "Procesando, te avisaremos"
       Frontend --> Supervisor : aviso

       deactivate Reporte

       loop [hasta job listo]
         ExportQueue -> ExportQueue : procesar(job)
         activate ExportQueue
       end
       deactivate ExportQueue

       ExportQueue ->> BuzonInterno : entregar(supervisor_id,\n            "Tu export está listo")
       BuzonInterno ->> Supervisor : aviso al buzón\n(CNST_001)
     end
   end
   deactivate Backend
   @enduml
