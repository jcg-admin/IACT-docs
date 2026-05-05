Ejemplo IACT — UC_RPT_04 (Exportar reporte)
-------------------------------------------

.. uml::

   @startuml
   |Supervisor|
   start
   :Seleccionar reporte y rango (max 6 meses, CNST_031);
   :Solicitar exportacion;
   |Backend|
   :Validar permiso (CNST_030 SoD);
   if (permiso ok?) then ([si])
     :Verificar throttling export (CNST_020);
     if (cuota disponible?) then ([si])
       :Encolar tarea async (CNST_019);
       |Worker Export|
       :Leer agregados de BDAnalytics;
       :Generar archivo CSV/XLSX;
       :Subir a almacen temporal;
       |Backend|
       :Notificar via buzon interno (CNST_001);
       |Supervisor|
       :Recibir notificacion;
       :Descargar archivo;
       stop
     else ([no])
       |Backend|
       :Responder "cuota agotada";
       stop
     endif
   else ([no])
     :Registrar intento denegado en AuditLog;
     stop
   endif
   @enduml
