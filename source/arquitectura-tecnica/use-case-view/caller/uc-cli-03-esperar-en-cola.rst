.. meta::
 :artefacto: AT_UC_CLI_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: caller
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_cli_03_esperar_en_cola:

==============================
UC_CLI_03 — Esperar en Cola
==============================

Caller espera atencion en cola. Sistema aplica reglas de routing
(skill, queue), reproduce mensajes de espera + posicion, monitorea
timeout SLA (max wait), ofrece callback cuando excede SLA. Resultado:
conectado con Operator (UC_OPR_02) o callback aceptado (UC_CLI_04).

.. uml::
 :caption: UC_CLI_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "Caller" as Caller <<externo>>
 actor "answer_inbound_calls" as Operator <<beneficiario>>
 actor "Call" as Call <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_03\nEsperar en Cola\n.. extension points ..\nOfrecerCallback\nConectar" as UC_CLI_03
   usecase "Aplicar reglas\nde routing (skill, queue)" as ROUTING
   usecase "Reproducir mensajes\nde espera + posicion" as MENSAJES
   usecase "Monitorear timeout\n(SLA max wait)" as TIMEOUT
   usecase "Ofrecer callback\n(UC_CLI_04)" as OFRECER_CB
   usecase "Conectar con Operator" as CONECTAR
 }

 Caller --> UC_CLI_03

 UC_CLI_03 ..> ROUTING : <<include>>
 UC_CLI_03 ..> MENSAJES : <<include>>
 UC_CLI_03 ..> TIMEOUT : <<include>>
 OFRECER_CB ..> UC_CLI_03 : <<extend>> (OfrecerCallback)
 CONECTAR ..> UC_CLI_03 : <<extend>> (Conectar)

 ROUTING --> Call
 TIMEOUT --> TimingCalculator
 CONECTAR --> Operator

 note bottom of TIMEOUT
   Restriccion SLA: tras X min
   ofrece callback automatico
   (RoutingStrategy + CallbackOfferStrategy).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con estado in_queue + queue_position.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session padre.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   wait time vs SLA.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   RoutingStrategy + CallbackOfferStrategy.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-04/index` —
   callback offer.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-02/index` —
   handoff al Operator.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-03/index` —
   spec textual.
