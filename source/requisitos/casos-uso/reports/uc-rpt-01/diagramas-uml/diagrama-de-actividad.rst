8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_01 — flujo

 @startuml

 start
 :GET /api/dashboard/?period=today;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_reports?) then (no)
   :403 + audit; stop
 endif
 :Resolver segmentos del User;
 if (Sin segmentos?) then (si)
   :400 USER_WITHOUT_SEGMENT; stop
 else (no)
 endif
 :Validar periodo;
 if (Cache hit?) then (si)
   :return cached;
   stop
 else (no)
 endif
 :Consultar Servicio de Reportes (sp_rpt_centros_xsegmento);
 :Calcular derivados (TMO, SL, abandono);
 :Construir response;
 :Cache write;
 :200 OK;
 stop

 @enduml

