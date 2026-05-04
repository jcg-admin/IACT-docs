10. Ejemplo completo IACT — UC_RPT_04 (Exportar reporte) en contexto espacial
=============================================================================

Combina todo: numeración, condiciones, anidación, ciclos,
sincronización, objetos activos / pasivos.

.. uml::

   @startuml
   allowmixing
   actor Supervisor

   object ":Backend" as Backend <<active>>
   object ":SecRules"               as SecRules
   object ":Reporte"                as Reporte
   object ":BDAnalytics"            as BDAnalytics
   object ":ExportQueue" as ExportQueue <<active>>
   object ":Archivo"                as Archivo
   object ":BuzonInterno"           as BuzonInterno
   object ":AuditLog"               as AuditLog

   Supervisor -> Backend  : "1: solicitar_export(\n   reporte_id, fmt)"
   Backend          -> SecRules : "1.1: verificar_permiso(\n   export_<fmt>)"
   Backend          -> SecRules : "1.2: validar_throttling(\n   CNST_020)"

   Backend  -> Reporte   : "[autorizado] 2: aplicar_filtros(\n   filtros, segmento)"
   Reporte  -> BDAnalytics  : "2.1: aplicar_segmento(\n   BR_012, CNST_008)"
   Reporte  -> BDAnalytics  : "2.2: estimar_filas := count()"

   Backend  -> Archivo   : "[filas <= 10k] 3a: <<create>>\n   generar_sincrono(fmt)"
   Archivo  -> BDAnalytics  : "3a.1: ejecutar_query()"
   Archivo  -> Backend   : "3a.2: archivo_listo"

   Backend  -> ExportQueue  : "[filas > 10k] 3b: encolar(\n   reporte_id, fmt, supervisor_id)"
   ExportQueue -> ExportQueue  : "3b.1: [* job en cola]\n   procesar(job)"
   ExportQueue -> BuzonInterno  : "3b.2: entregar(supervisor,\n   archivo_listo)"
   BuzonInterno -> Supervisor : "3b.3: aviso buzón\n   (CNST_001)"

   Backend  -> AuditLog  : "1.1, 2 / 4: registrar(\n   EXPORT_ACTION,\n   resultado)"
   Backend  -> Supervisor : "5: respuesta(url | aviso)"

   note right of ExportQueue
     ExportQueue es objeto activo:
     procesa jobs en background,
     escribe en BuzonInterno cuando
     termina (CNST_019). Borde grueso.
   end note

   note right of AuditLog
     Sincronización: el registro 4
     en AuditLog espera a que se
     completen 1.1 (verificación)
     Y 2 (filtros aplicados).
   end note
   @enduml

----
