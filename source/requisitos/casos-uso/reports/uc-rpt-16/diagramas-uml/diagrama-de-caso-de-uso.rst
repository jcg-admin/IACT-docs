8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_16 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "IvrNavigationReportService" as SVC <<sistema>>
 actor "Bucket" as BK <<sistema>>
 actor "Call" as CALL <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_16\nReporte de Menus IVR" as UC_RPT_16
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Calcular total\ningresos al IVR" as METRIC_VOL
   usecase "Distribucion por\nopcion del menu raiz" as METRIC_DIST
   usecase "Drop-off rate\npor nodo" as METRIC_DROP
   usecase "Avg time in menu\n+ Top paths" as METRIC_PATH
 }

 INVOKER --> UC_RPT_16
 UC_RPT_16 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_16 ..> METRIC_VOL : <<include>>
 UC_RPT_16 ..> METRIC_DIST : <<include>>
 UC_RPT_16 ..> METRIC_DROP : <<include>>
 UC_RPT_16 ..> METRIC_PATH : <<include>>

 METRIC_VOL --> SVC
 METRIC_DIST --> BK
 METRIC_DROP --> BK
 SVC --> CALL

 note bottom of UC_RPT_16
   BReq-001 + BReq-007. Identificar
   cuello de botella en IVR: opciones
   confusas, drop-off alto,
   tiempo en menu excesivo.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service` —
   servicio especifico para reporte IVR.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method base.
 - :doc:`/arquitectura-tecnica/domain-model/bucket` —
   bucket de distribucion por opcion + drop-off por nodo.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con paths IVR navegados.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-02/index` —
   UC origen de la navegacion IVR.
