.. meta::
 :artefacto: AT_UC_OPR_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Fuera del scope
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_opr_01_cambiar_estado_del_agente:

============================================================
UC_OPR_01 — Cambiar Estado del Agente
============================================================

Agente declara disponibilidad para recibir llamadas. State machine:
available, not_ready, break, busy, offline. Sistema usa estado para
routing. ``manage_own_agent_state``. Cambios afectan adherence
(insumo UC_RPT_12).

.. uml::
 :caption: UC_OPR_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_own_agent_state" as manage_own_agent_state
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Session" as Session <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado\ndel Agente" as UC_OPR_01
   usecase "Validar transicion\n(state machine)" as VALIDAR_TRANS
   usecase "Persistir estado\n(available | not_ready | break)" as PERSISTIR
   usecase "Notificar router\n(propagar disponibilidad)" as NOTIFY_ROUTER
   usecase "Emitir AuditEvent\nAGENT_STATE_CHANGED" as AUDITAR
 }

 manage_own_agent_state --> UC_OPR_01

 UC_OPR_01 ..> VALIDAR_TRANS : <<include>>
 UC_OPR_01 ..> PERSISTIR : <<include>>
 UC_OPR_01 ..> NOTIFY_ROUTER : <<include>>
 UC_OPR_01 ..> AUDITAR : <<include>>

 PERSISTIR --> Session
 NOTIFY_ROUTER --> EvaluatorReloader
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of NOTIFY_ROUTER
   Router consume estado para
   routing — solo enruta a agentes
   en `available`. Cambio debe
   propagarse en tiempo real.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session con campo agent_state.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   User del agente.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   propaga al routing.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-01/index` —
   spec textual.
