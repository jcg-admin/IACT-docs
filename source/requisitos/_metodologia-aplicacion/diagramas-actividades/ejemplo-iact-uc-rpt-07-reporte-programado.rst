Ejemplo IACT — UC_RPT_07 (Reporte programado)
---------------------------------------------

Al cierre de la ventana ETL (CNST_006/007/008), tres tareas
arrancan en paralelo: cálculo de métricas, persistencia y
notificación al solicitante.

.. uml::

   @startuml
   start
   :Detectar fin de ventana ETL;
   :Cargar configuracion del reporte;
   fork
     :Calcular metricas BR_016/017/018;
     :Persistir resultados en BDAnalytics;
   fork again
     :Generar archivo de exportacion (async, CNST_019);
     :Subir a almacen temporal;
   fork again
     :Componer notificacion;
     :Publicar en buzon interno (CNST_001);
   end fork
   :Marcar reporte como entregado;
   :Registrar evento en AuditLog;
   stop
   @enduml
