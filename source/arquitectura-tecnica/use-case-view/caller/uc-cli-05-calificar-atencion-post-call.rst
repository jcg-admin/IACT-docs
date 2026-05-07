.. meta::
 :artefacto: AT_UC_CLI_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: caller
 :estado: Fuera del scope
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_cli_05_calificar_atencion_post_call:

============================================================
UC_CLI_05 — Calificar Atencion (Post-Call CSAT)
============================================================

Tras hangup del agent, sistema reproduce 1-3 preguntas DTMF al caller.
Compliance opt-out: caller puede colgar en cualquier momento sin
penalidad. Resultado persistido en ``Metric``.

.. uml::
 :caption: UC_CLI_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "Caller" as Caller <<externo>>
 actor "Call" as Call <<sistema>>
 actor "Metric" as Metric <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_05\nCalificar Atencion\n(Post-Call CSAT)" as UC_CLI_05
   usecase "Verificar flag\noffer_csat_post_call" as VERIFY_FLAG
   usecase "Reproducir 1-3\npreguntas DTMF" as PREGUNTAR
   usecase "Capturar respuestas\n(opt-out: hangup)" as CAPTURAR
   usecase "Persistir CSAT\ncomo Metric" as PERSISTIR
 }

 Caller --> UC_CLI_05

 UC_CLI_05 ..> VERIFY_FLAG : <<include>>
 UC_CLI_05 ..> PREGUNTAR : <<include>>
 UC_CLI_05 ..> CAPTURAR : <<include>>
 UC_CLI_05 ..> PERSISTIR : <<include>>

 PREGUNTAR --> Call
 PERSISTIR --> Metric

 note bottom of CAPTURAR
   Compliance opt-out: caller
   puede colgar sin penalidad
   ni reintento. Sin re-call.
 end note

 note right of Caller
   Trigger: agente cuelga + flag
   offer_csat_post_call activo
   en la cola/segmento.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con metadata CSAT.
 - :doc:`/arquitectura-tecnica/domain-model/metric` —
   CSAT result.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-05/index` —
   spec textual.
