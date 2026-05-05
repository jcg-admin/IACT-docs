8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_16 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "IvrNavigationReportService" as SVC <<sistema>>
 actor "IVRStatRepo" as REPO <<sistema>>

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
 SVC --> REPO

 note bottom of UC_RPT_16
   BReq-001 + BReq-007. Identificar
   cuello de botella en IVR: opciones
   confusas, drop-off alto,
   tiempo en menu excesivo.
 end note

 @enduml
