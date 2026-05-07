.. meta::
 :artefacto: AT_UC_CLI_04_USECASE
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

.. _at_uc_cli_04_solicitar_callback:

==============================
UC_CLI_04 — Solicitar Callback
==============================

Caller acepta opcion de callback (auto-servicio o cola exhausto SLA).
Confirma numero de retorno + ventana horaria. Sistema crea
``CallbackEntry`` (Call con type=callback) + hangup voluntario.

.. uml::
 :caption: UC_CLI_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "Caller" as Caller <<externo>>
 actor "Call" as Call <<sistema>>
 actor "Session" as Session <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nSolicitar Callback" as UC_CLI_04
   usecase "Confirmar numero\nde retorno" as CONFIRM_NUM
   usecase "Confirmar ventana\nhoraria" as CONFIRM_WINDOW
   usecase "Crear CallbackEntry\n(Call type=callback)" as CREATE_CB
   usecase "Hangup voluntario" as HANGUP
 }

 Caller --> UC_CLI_04

 UC_CLI_04 ..> CONFIRM_NUM : <<include>>
 UC_CLI_04 ..> CONFIRM_WINDOW : <<include>>
 UC_CLI_04 ..> CREATE_CB : <<include>>
 UC_CLI_04 ..> HANGUP : <<include>>

 CREATE_CB --> Call
 HANGUP --> Session

 note bottom of CONFIRM_NUM
   Default: caller_id (hashed).
   Alternativa: numero alterno
   indicado por el caller.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con type=callback.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session terminada.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-04/index` —
   spec textual.
