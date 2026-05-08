8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "Call" as CALL <<sistema>>
 actor "Metric" as METRIC <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_05\nCalificar Atencion\n(Post-Call CSAT)" as UC_CLI_05
   usecase "Reproducir 1-3\npreguntas DTMF" as PREGUNTAR
   usecase "Capturar respuestas\n(opt-out: hangup)" as CAPTURAR
   usecase "Persistir CSAT\ncomo Metric" as PERSISTIR
 }

 CALLER --> UC_CLI_05

 UC_CLI_05 ..> PREGUNTAR : <<include>>
 UC_CLI_05 ..> CAPTURAR : <<include>>
 UC_CLI_05 ..> PERSISTIR : <<include>>

 PREGUNTAR --> CALL
 PERSISTIR --> METRIC

 note bottom of CAPTURAR
   Compliance opt-out: caller
   puede colgar en cualquier
   momento sin penalidad ni
   reintento.
 end note

 note right of CALLER
   Trigger: agente cuelga + flag
   `offer_csat_post_call` activo
   en la cola/segmento.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con metadata de CSAT post-call.
 - :doc:`/arquitectura-tecnica/domain-model/metric` —
   entidad Metric donde se persiste el CSAT.
