8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_03 — flujo

 @startuml
 start
 :GET con periodo + filtros + group_by;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403 + audit; stop
 endif
 :Resolver segmento;
 :Validar (range, group_by, page);
 if (Cache hit?) then (si)
   :return cached;
   stop
 endif
 :Query current period;
 :Query prior period (comparative);
 :Calcular KPIs por bucket;
 :Construir comparative;
 :Cache write TTL adaptativo;
 :200 OK;
 stop
 @enduml

