8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_alerts" as INVOKER
 actor "AlertRepo" as REPO <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_02\nVer Alertas Activas" as UC_ALR_02
   usecase "Filtrar por scope\n(segmentos del User)" as FILTRAR_SCOPE
   usecase "Filtrar por estado\n(firing | acknowledged)" as FILTRAR_ESTADO
   usecase "Ordenar por\nseveridad + recencia" as ORDENAR
   usecase "Auto-refresh 10s" as REFRESH <<extend>>
 }

 INVOKER --> UC_ALR_02
 UC_ALR_02 ..> FILTRAR_SCOPE : <<include>>
 UC_ALR_02 ..> FILTRAR_ESTADO : <<include>>
 UC_ALR_02 ..> ORDENAR : <<include>>
 REFRESH ..> UC_ALR_02 : <<extend>>

 FILTRAR_SCOPE --> REPO
 FILTRAR_ESTADO --> REPO

 note bottom of FILTRAR_SCOPE
   CNST-008 isolation: solo alertas
   cuyo scope ⊆ segmentos del User.
   Read-only sin auditoria de invocacion.
 end note

 note bottom of REFRESH
   Auto-refresh 10s default —
   mas frecuente que UC_RPT_01
   por naturaleza operacional.
 end note

 @enduml
