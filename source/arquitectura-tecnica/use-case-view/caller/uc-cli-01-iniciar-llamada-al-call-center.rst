.. meta::
 :artefacto: AT_UC_CLI_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: caller
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_cli_01_iniciar_llamada_al_call_center:

==================================================
UC_CLI_01 — Iniciar Llamada al Call Center
==================================================

Caller externo marca DID del call center. Sistema reproduce welcome,
hashea ``caller_id`` (CNST-026 sin PII), crea ``Session`` + ``Call``,
transfiere control a IVRRunner. BReq-007. Caller es actor externo
(no autenticado en sistema).

.. uml::
 :caption: UC_CLI_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "Caller" as Caller <<externo>>
 actor "Trunk SIP" as Trunk_SIP <<sistema_externo>>
 actor "Session" as Session <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar Llamada\nal Call Center" as UC_CLI_01
   usecase "Reproducir welcome\n/ saludo" as WELCOME
   usecase "Hashear caller_id\n(CNST-026)" as HASH
   usecase "Crear Session\ncon caller_hash" as CREATE_SESSION
   usecase "Crear Call asociado" as CREATE_CALL
   usecase "Transferir control\na IVR (UC_CLI_02)" as HANDOFF
 }

 Caller --> Trunk_SIP
 Trunk_SIP --> UC_CLI_01

 UC_CLI_01 ..> WELCOME : <<include>>
 UC_CLI_01 ..> HASH : <<include>>
 UC_CLI_01 ..> CREATE_SESSION : <<include>>
 UC_CLI_01 ..> CREATE_CALL : <<include>>
 UC_CLI_01 ..> HANDOFF : <<include>>

 HASH --> Sanitizer
 CREATE_SESSION --> Session
 CREATE_CALL --> Call

 note bottom of HASH
   CNST-026: caller_hash desde
   primer momento. Nunca se persiste
   caller_id en limpio. Sin PII en logs.
 end note

 note right of Caller
   BReq-007 — actor externo,
   no autenticado en sistema.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session creada con caller_hash.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call asociado.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   hashea caller_id.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-02/index` —
   IVR navigation siguiente.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-01/index` —
   spec textual.
