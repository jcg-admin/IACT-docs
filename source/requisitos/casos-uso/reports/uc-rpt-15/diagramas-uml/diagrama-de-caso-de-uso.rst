8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_15 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "ReportingService\n(sp_rpt_centros_transferencia\n+ sp_rpt_centros_xsegmento)" as SP <<sistema>>
 database "BD_IVR" as BDIVR

 rectangle "MOD_Reports" {
   usecase "UC_RPT_15\nReporte de Transferencias" as UC_RPT_15
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
 }

 INVOKER --> UC_RPT_15
 UC_RPT_15 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_15 --> SP : callproc x2 (centros + xsegmento)
 SP --> BDIVR : CALL sp_rpt_centros_transferencia\nCALL sp_rpt_centros_xsegmento

 note bottom of UC_RPT_15
   BReq-001 + BReq-002. Identificar
   transfers excesivos (skill misrouting),
   circulares, agentes con alta tasa
   transfer-out (capacitacion).
   CNST-007 read-only BD_IVR — DOBLE SP.
   El backend solo combina los dos
   result sets ya pre-agregados.
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
