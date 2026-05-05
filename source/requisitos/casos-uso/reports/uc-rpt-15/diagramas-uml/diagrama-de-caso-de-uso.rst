8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_15 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "TransferReportService" as SVC <<sistema>>
 actor "Call" as CALL <<sistema>>
 actor "TimingCalculator" as TC <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_15\nReporte de Transferencias" as UC_RPT_15
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Calcular total transfers\n(in/out)" as METRIC_TOTAL
   usecase "Calcular avg time\npre-transfer" as METRIC_PRETIME
   usecase "Calcular Disposition\npost-transfer" as METRIC_POST
   usecase "Top reasons\n(skill, language, escalation)" as METRIC_REASONS
 }

 INVOKER --> UC_RPT_15
 UC_RPT_15 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_15 ..> METRIC_TOTAL : <<include>>
 UC_RPT_15 ..> METRIC_PRETIME : <<include>>
 UC_RPT_15 ..> METRIC_POST : <<include>>
 UC_RPT_15 ..> METRIC_REASONS : <<include>>

 METRIC_TOTAL --> SVC
 SVC --> CALL
 METRIC_PRETIME --> TC

 note bottom of UC_RPT_15
   BReq-001 + BReq-002. Identificar
   transfers excesivos (skill misrouting),
   circulares, agentes con alta tasa
   transfer-out (capacitacion).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service` —
   servicio especifico para reporte de transferencias.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method base.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con flag transferred=true y reason.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tiempo medio pre-transfer.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-05/index` —
   UC origen de los datos (transferir llamada).
