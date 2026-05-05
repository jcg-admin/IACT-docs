.. meta::
 :artefacto: AT_UC_OPR_09_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_09_ver_propio_historial_de_llamadas:

==============================================
UC_OPR_09 — Ver Propio Historial de Llamadas
==============================================

Vista PROPIA del agente. List paginado de propias llamadas con
disposition + duracion + tags. Sin PII de cliente (caller_hash).
Util para self-coaching, recordar casos pendientes, follow-up.
``view_own_call_history``.

.. uml::
 :caption: UC_OPR_09 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_own_call_history" as view_own_call_history
 actor "Call" as Call <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_09\nVer Propio Historial\nde Llamadas" as UC_OPR_09
   usecase "Validar period\n(default last_7d)" as VALIDAR_PERIOD
   usecase "Filtrar por\ndisposition" as FILTRAR
   usecase "Cargar caller_hash\n(sin PII)" as HASH
   usecase "Devolver entries\n(disposition + duracion + tags)" as DEVOLVER
   usecase "Cursor pagination" as PAGINACION
 }

 view_own_call_history --> UC_OPR_09

 UC_OPR_09 ..> VALIDAR_PERIOD : <<include>>
 UC_OPR_09 ..> FILTRAR : <<include>>
 UC_OPR_09 ..> HASH : <<include>>
 UC_OPR_09 ..> DEVOLVER : <<include>>
 UC_OPR_09 ..> PAGINACION : <<include>>

 FILTRAR --> Call
 DEVOLVER --> Call
 HASH --> Sanitizer
 PAGINACION --> CursorEncoder

 note bottom of HASH
   CNST-026 sin PII: caller_hash
   se devuelve, NUNCA caller_id
   en limpio.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Calls del propio User.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   garantiza caller_hash.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-09/index` —
   spec textual.
