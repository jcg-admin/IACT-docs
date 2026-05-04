.. _uc-rpt-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_03 — historicos

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_03\nHistoricos" as UC03
   usecase "Filtros + grupos" as F
   usecase "Comparative" as C
   usecase "Cache" as CA
 }

 view_reports --> UC03
 UC03 ..> F : <<include>>
 UC03 ..> C : <<extend>>
 UC03 ..> CA : <<include>>
 @enduml

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

8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml
 class HistoricalReport {
   period
   group_by
   buckets: list[Bucket]
   comparative: Comparative
 }

 class Bucket {
   bucket_key
   kpis: KPISet
 }

 class Comparative {
   period_prior
   kpis_summary
   diff_pct
 }

 HistoricalReport "1" -- "*" Bucket
 HistoricalReport "1" -- "0..1" Comparative
 @enduml

8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_03 — secuencia

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "Cache" as Cache
 database "Analytics" as Analytics

 User -> Endpoint: GET con filtros
 Endpoint -> Endpoint: JWT + RBAC + segmento + validar
 Endpoint -> Cache: get(key)
 Cache --> Endpoint: miss
 par
   Endpoint -> Analytics: aggregate current
 also
   Endpoint -> Analytics: aggregate prior
 end
 Analytics --> Endpoint: rows
 Endpoint -> Endpoint: calcular KPIs + comparative
 Endpoint -> Cache: set
 Endpoint --> User: 200
 @enduml
