6. Diagrama de actividades — UC_RPT_04 (exportar reporte)
=========================================================

.. uml::

   @startuml

   start
   :Operador solicita exportar\n(formato: CSV / Excel / PDF);
   :Verificar permiso export_<formato>;

   if ([permiso ok]) then (sí)
   else (no)
     :Mostrar 403 + auditar;
     stop
   endif

   :Aplicar filtros BR_012\n(segmento del usuario);
   :Estimar # filas resultado;

   if ([throttling CNST_020 alcanzado]) then (sí)
     :Mostrar "Límite del día";
     stop
   endif

   if ([filas > 10k → CNST_019]) then (sí)
     :Encolar export asíncrono;
     :Notificar al buzón cuando listo;
     :Operador descarga desde panel;
   else ([≤ 10k])
     :Generar archivo en línea;
     :Devolver descarga directa;
   endif

   :Registrar export en AuditLog;
   :Fin: archivo entregado;
   stop
   @enduml

**Aplicación:** DOC-20 (UC_RPT) y otros UCs con exportación.
