8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_13 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "ReportingService\n(sp_rpt_llamadas_abandonadas)" as SP <<sistema>>
 database "BD_IVR" as BDIVR

 rectangle "MOD_Reports" {
   usecase "UC_RPT_13\nReporte de Colas" as UC_RPT_13
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
 }

 INVOKER --> UC_RPT_13
 UC_RPT_13 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_13 --> SP : callproc(period, segments)
 SP --> BDIVR : CALL sp_rpt_llamadas_abandonadas

 note bottom of UC_RPT_13
   BReq-001 + BReq-006. Detectar
   colas saturadas o con SL bajo.
   CNST-007 read-only BD_IVR via SP.
   El SP entrega offered/answered/
   abandoned/asa/SL/abandon rate ya
   pre-calculados.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method que implementa el reporte de colas.
 - :doc:`/arquitectura-tecnica/domain-model/bucket` —
   bucket de agregacion (SL within threshold, queue depth).
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   calculo de ASA, SL%, abandon rate.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   fuente de datos (calls offered/answered/abandoned).
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   componente para calcular wait times y SL within.
