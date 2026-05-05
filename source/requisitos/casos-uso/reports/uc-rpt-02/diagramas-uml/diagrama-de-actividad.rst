8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_02 — flujo

 @startuml

 start
 :Frontend abre conexion stream;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_kpis?) then (no)
   :403 + audit; stop
 endif
 if (Sin segmento?) then (si)
   :400; stop
 endif
 :Suscribir a AnalyticsStream
  con filtro segmento;
 :Audit REALTIME_STREAM_OPENED;

 while (Conexion abierta?)
   if (Evento del stream?) then (si)
     :Construir snapshot;
     :Throttle 1/5s;
     :Emit event: metrics;
   else (no)
     if (>= 30s sin data?) then (si)
       :Emit event: heartbeat;
     endif
   endif
 endwhile

 :Audit REALTIME_STREAM_CLOSED;
 :Limpieza;
 stop

 @enduml

