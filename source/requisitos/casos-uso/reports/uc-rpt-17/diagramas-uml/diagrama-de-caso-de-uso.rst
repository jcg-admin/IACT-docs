8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_17 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "ReportingService\n(sp_rpt_clientes)" as ReportingService <<sistema>>
 actor "ETL upstream\n(sp_etl_base_clientes)" as EtlAnonimizador <<sistema>>
 database "BD_IVR" as BdIvrLegacy

 rectangle "MOD_Reports" {
   usecase "UC_RPT_17\nReporte de\nClientes Unicos" as UC_RPT_17
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
 }

 view_reports --> UC_RPT_17
 UC_RPT_17 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_17 --> ReportingService : callproc(sp_rpt_clientes)
 ReportingService --> BdIvrLegacy : CALL sp_rpt_clientes\n(lee telefono_hashed)
 EtlAnonimizador --> BdIvrLegacy : pobla base_ivr_clientes\n(hash unidireccional ANTES)

 note right of EtlAnonimizador
   CNST-026 sin PII: el hash del
   telefono lo aplica el ETL upstream
   ANTES de poblar base_ivr_clientes.
   El backend NUNCA ve el numero raw.
 end note

 note bottom of UC_RPT_17
   BReq-001 + BReq-003. Util para
   campanas inbound y dimensionamiento.
   CNST-007 read-only BD_IVR via SP.
   El SP entrega distinct counts,
   recurrence y new vs returning ya
   pre-calculados sobre el hash.
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
