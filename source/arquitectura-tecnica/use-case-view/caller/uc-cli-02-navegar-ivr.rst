.. meta::
 :artefacto: AT_UC_CLI_02_USECASE
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

.. _at_uc_cli_02_navegar_ivr:

==============================
UC_CLI_02 — Navegar IVR
==============================

Caller navega arbol IVR via DTMF/audio. Salidas: cola para agente,
auto-servicio, callback (UC_CLI_04), hangup. Sin entrada HTTP — input
audio directo. Sin RBAC (actor externo).

.. uml::
 :caption: UC_CLI_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "Caller" as Caller <<externo>>
 actor "Session" as Session <<sistema>>
 actor "Call" as Call <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR\n.. extension points ..\nEnrutarCola\nAutoServicio\nCallback\nHangup" as UC_CLI_02
   usecase "Cargar arbol IVR\n(IVRDefinition)" as CARGAR
   usecase "Capturar input\n(audio / DTMF)" as CAPTURAR
   usecase "Enrutar a cola\n(UC_CLI_03)" as ROUTE_QUEUE
   usecase "Auto-servicio\n(saldo, horario, ...)" as SELF_SERVICE
   usecase "Ofrecer callback\n(UC_CLI_04)" as ROUTE_CALLBACK
   usecase "Hangup voluntario" as HANGUP
 }

 Caller --> UC_CLI_02

 UC_CLI_02 ..> CARGAR : <<include>>
 UC_CLI_02 ..> CAPTURAR : <<include>>
 ROUTE_QUEUE ..> UC_CLI_02 : <<extend>> (EnrutarCola)
 SELF_SERVICE ..> UC_CLI_02 : <<extend>> (AutoServicio)
 ROUTE_CALLBACK ..> UC_CLI_02 : <<extend>> (Callback)
 HANGUP ..> UC_CLI_02 : <<extend>> (Hangup)

 CARGAR --> Session
 CAPTURAR --> Call

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   estado IVR.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call durante navegacion.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-03/index` —
   transicion a cola.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-04/index` —
   transicion a callback.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-02/index` —
   spec textual.
