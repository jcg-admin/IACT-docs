8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "hold_unhold_own_call" as INVOKER
 actor "Caller" as CALLER <<beneficiario>>
 actor "TelephonyClient" as CHANNEL <<sistema>>
 actor "AdherenceTracker" as ADHERENCE <<sistema>>
 actor "AlertEvaluator" as ALERTS <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold / Unhold Llamada" as UC_OPR_04
   usecase "Validar llamada\nactiva" as VALIDAR
   usecase "Pausar audio\nbidireccional" as PAUSAR
   usecase "Reproducir musica\n/ mensaje al caller" as MUSICA
   usecase "Tracker de hold time\n(adherence)" as TRACK
   usecase "Alerta supervisor\nsi hold > N seg" as ALERTAR <<extend>>
 }

 INVOKER --> UC_OPR_04
 UC_OPR_04 ..> VALIDAR : <<include>>
 UC_OPR_04 ..> PAUSAR : <<include>>
 UC_OPR_04 ..> MUSICA : <<include>>
 UC_OPR_04 ..> TRACK : <<include>>
 ALERTAR ..> UC_OPR_04 : <<extend>>

 PAUSAR --> CHANNEL
 MUSICA --> CALLER
 TRACK --> ADHERENCE
 ALERTAR --> ALERTS

 note bottom of TRACK
   Hold time tracked como parte
   de adherence — afecta KPIs en
   UC_RPT_12.
 end note

 note bottom of ALERTAR
   Long hold > N segundos genera
   alerta operacional al supervisor
   (UC_ALR_02).
 end note

 @enduml
