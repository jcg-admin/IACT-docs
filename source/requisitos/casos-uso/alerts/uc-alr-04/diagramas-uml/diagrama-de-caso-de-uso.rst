8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_alert_history" as INVOKER
 actor "AlertRepo" as REPO <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_04\nVer Historial\nde Alertas" as UC_ALR_04
   usecase "Validar period\n(<= 1 ano online)" as VALIDAR_PERIOD
   usecase "Filtrar por\nrule_id, severity" as FILTRAR
   usecase "Calcular tiempo\nmedio de ack" as METRICA_ACK
   usecase "Calcular tiempo\nmedio de resolve" as METRICA_RESOLVE
   usecase "Cursor-based\npagination" as PAGINACION
 }

 INVOKER --> UC_ALR_04
 UC_ALR_04 ..> VALIDAR_PERIOD : <<include>>
 UC_ALR_04 ..> FILTRAR : <<include>>
 UC_ALR_04 ..> METRICA_ACK : <<include>>
 UC_ALR_04 ..> METRICA_RESOLVE : <<include>>
 UC_ALR_04 ..> PAGINACION : <<include>>

 FILTRAR --> REPO
 METRICA_ACK --> REPO
 METRICA_RESOLVE --> REPO

 note bottom of VALIDAR_PERIOD
   Hasta 1 ano online. Mas antiguo
   requiere export con archive
   (UC_RPT_04).
 end note

 note bottom of UC_ALR_04
   Insumo para mejorar reglas
   (UC_ALR_01) y SLAs.
   Out of scope: alertas activas
   (UC_ALR_02).
 end note

 @enduml
