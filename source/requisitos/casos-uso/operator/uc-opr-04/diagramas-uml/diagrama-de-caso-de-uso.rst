8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "hold_unhold_own_call" as INVOKER
 actor "Caller" as CALLER <<beneficiario>>
 actor "Call" as CALL <<sistema>>
 actor "TimingCalculator" as TC <<sistema>>
 actor "AlertHook" as AH <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold / Unhold Llamada" as UC_OPR_04
   usecase "Validar Call\nactiva" as VALIDAR
   usecase "Pausar audio\nbidireccional" as PAUSAR
   usecase "Reproducir musica\n/ mensaje al caller" as MUSICA
   usecase "Tracker de hold time\n(adherence)" as TRACK
   usecase "Disparar alerta\nsi hold > N seg" as ALERTAR <<extend>>
 }

 INVOKER --> UC_OPR_04
 UC_OPR_04 ..> VALIDAR : <<include>>
 UC_OPR_04 ..> PAUSAR : <<include>>
 UC_OPR_04 ..> MUSICA : <<include>>
 UC_OPR_04 ..> TRACK : <<include>>
 ALERTAR ..> UC_OPR_04 : <<extend>>

 PAUSAR --> CALL
 MUSICA --> CALLER
 TRACK --> TC
 ALERTAR --> AH

 note bottom of TRACK
   Hold time tracked como parte
   de adherence — afecta KPIs en
   UC_RPT_12.
 end note

 note bottom of ALERTAR
   Long hold > N segundos genera
   alerta operacional al supervisor
   (UC_ALR_02 via AlertHook).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con flags hold_state + hold_count + hold_total_time.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tracker de hold time para adherence.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   evaluador que dispara alerta cuando hold > threshold.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla configurada para hold time excessive.
