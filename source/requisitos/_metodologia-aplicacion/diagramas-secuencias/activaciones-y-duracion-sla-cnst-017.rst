6. Activaciones y duración — SLA CNST_017
=========================================

La **altura** de la activación representa la**duración**.
Útil para visualizar SLAs (CNST_017 — latencia ≤ 10 s).

.. uml::

   @startuml

   participant ":Backend" as Backend
   participant ":CacheRedis" as CacheRedis
   participant ":BDAnalytics" as BDAnalytics

   Backend -> CacheRedis : GET reporte:dash:user_42
   activate CacheRedis
   note left of CacheRedis
     Cache lookup
     ~5 ms
   end note
   CacheRedis --> Backend : MISS
   deactivate CacheRedis

   Backend -> BDAnalytics : SELECT métricas WHERE segmento=?
   activate BDAnalytics
   note right of BDAnalytics
     Query con filtro
     CNST_008 ~ 800 ms
   end note
   BDAnalytics --> Backend : filas
   deactivate BDAnalytics

   Backend -> CacheRedis : SET reporte:dash:user_42 TTL=300
   activate CacheRedis
   CacheRedis --> Backend : ok
   deactivate CacheRedis

   note over Backend
     Total ≈ 850 ms
     ≤ CNST_017 (10 s) ✓
   end note
   @enduml
