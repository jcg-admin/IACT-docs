.. meta::
 :artefacto: AT_UC_OPR_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Fuera del scope
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_04_hold_unhold_llamada:

============================================================
UC_OPR_04 — Hold / Unhold Llamada
============================================================

Agente pausa audio bidireccional. Caller escucha musica/mensaje.
Hold time tracked (afecta adherence). Long hold > N seg dispara
alerta supervisor (UC_ALR_02). ``hold_unhold_own_call``.

.. uml::
 :caption: UC_OPR_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "hold_unhold_own_call" as hold_unhold_own_call
 actor "Caller" as Caller <<beneficiario>>
 actor "Call" as Call <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>
 actor "AlertHook" as AlertHook <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold / Unhold Llamada\n.. extension points ..\nAlertarLongHold" as UC_OPR_04
   usecase "Validar Call activa" as VALIDAR
   usecase "Pausar audio\nbidireccional" as PAUSAR
   usecase "Reproducir musica\n/ mensaje al caller" as MUSICA
   usecase "Tracker de hold time\n(adherence)" as TRACK
   usecase "Disparar alerta\nsi hold > N seg" as ALERTAR
 }

 hold_unhold_own_call --> UC_OPR_04

 UC_OPR_04 ..> VALIDAR : <<include>>
 UC_OPR_04 ..> PAUSAR : <<include>>
 UC_OPR_04 ..> MUSICA : <<include>>
 UC_OPR_04 ..> TRACK : <<include>>
 ALERTAR ..> UC_OPR_04 : <<extend>> (AlertarLongHold)

 PAUSAR --> Call
 MUSICA --> Caller
 TRACK --> TimingCalculator
 ALERTAR --> AlertHook

 note bottom of TRACK
   Hold time tracked como parte
   de adherence — afecta KPIs en
   UC_RPT_12.
 end note

 note bottom of ALERTAR
   Long hold > N seg dispara
   alerta operacional al supervisor
   (UC_ALR_02 via AlertHook).
   HoldMessageStrategy variants.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con hold_state + hold_count.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tracker hold time.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   trigger alerta long hold.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla configurada.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   HoldMessageStrategy.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-04/index` —
   spec textual.
