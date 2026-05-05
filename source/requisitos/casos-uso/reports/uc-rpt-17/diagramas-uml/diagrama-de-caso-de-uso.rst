8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_17 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "CallerReportService" as SVC <<sistema>>
 actor "Sanitizer" as SAN <<sistema>>
 actor "Call" as CALL <<sistema>>
 actor "KpiCalculator" as KPI <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_17\nReporte de\nClientes Unicos" as UC_RPT_17
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Hashear caller_id\n(CNST-026 sin PII)" as HASH
   usecase "Calcular clientes\ndistintos" as METRIC_UNIQUE
   usecase "Calcular recurrencia\n(distribucion)" as METRIC_RECUR
 }

 INVOKER --> UC_RPT_17
 UC_RPT_17 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_17 ..> HASH : <<include>>
 UC_RPT_17 ..> METRIC_UNIQUE : <<include>>
 UC_RPT_17 ..> METRIC_RECUR : <<include>>

 HASH --> SAN
 METRIC_UNIQUE --> SVC
 METRIC_RECUR --> KPI
 SVC --> CALL

 note bottom of HASH
   CNST-026 sin PII: identificador
   del cliente es hash del telefono
   o cliente_id, NUNCA el valor
   en limpio.
 end note

 note bottom of UC_RPT_17
   BReq-001 + BReq-003. Util para
   campanas inbound y dimensionamiento.
   Medir alcance: cuantos clientes
   distintos, cuantos recurrentes.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service` —
   servicio especifico para reporte de clientes unicos.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method base.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   componente que hashea caller_id (CNST-026).
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Calls con caller_hash agrupado.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   calculo de distribucion de recurrencia.
