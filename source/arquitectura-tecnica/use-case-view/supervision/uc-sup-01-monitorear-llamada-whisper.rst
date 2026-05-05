.. meta::
 :artefacto: AT_UC_SUP_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: supervision
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_sup_01_monitorear_llamada_whisper:

================================================
UC_SUP_01 — Monitorear Llamada (silent/whisper)
================================================

Supervisor monitorea una llamada activa entre Operator y Caller en
modo **silent** (escucha pasiva, ni operator ni caller perciben) o
**whisper** (puede instruir audible al operator, caller no oye).
Operacion **muy sensitiva** — auditoria reforzada P-39 + obligacion
legal de notificar al agente con tono audible al iniciar (compliance).

.. uml::
 :caption: UC_SUP_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "monitor_live_calls" as monitor_live_calls
 actor "answer_inbound_calls" as Operator <<beneficiario>>
 actor "Caller" as Caller <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada\n(silent | whisper)\n.. extension points ..\nSwitchModo\nNotificarAgente" as UC_SUP_01
   usecase "Verificar\nmonitor_live_calls" as VERIFICAR_AGR
   usecase "Validar agent target\n∈ segmento (CNST-008)" as VALIDAR_SEGMENTO
   usecase "Validar reason ≥ 20" as VALIDAR_REASON
   usecase "Validar mode\n(silent | whisper)" as VALIDAR_MODE
   usecase "Telephony.bridge_listen\n(sup + caller + agent)" as ESTABLECER_LISTEN
   usecase "Tono audible al agent\n(politica legal)" as TONO_AUDIBLE
   usecase "Notificar agent\nUI badge" as UI_BADGE
   usecase "Switch silent ↔ whisper\nen vivo" as SWITCH_MODO
   usecase "Stop monitor\n(unbridge)" as STOP_MONITOR
   usecase "Auto-stop\nllamada termina" as AUTO_STOP
   usecase "Emitir AuditEvent\nCALL_MONITORED\n(P-39 reforzado)" as AUDITAR
 }

 monitor_live_calls --> UC_SUP_01

 UC_SUP_01 ..> VERIFICAR_AGR : <<include>>
 UC_SUP_01 ..> VALIDAR_SEGMENTO : <<include>>
 UC_SUP_01 ..> VALIDAR_REASON : <<include>>
 UC_SUP_01 ..> VALIDAR_MODE : <<include>>
 UC_SUP_01 ..> ESTABLECER_LISTEN : <<include>>
 UC_SUP_01 ..> TONO_AUDIBLE : <<include>>
 UC_SUP_01 ..> AUDITAR : <<include>>
 SWITCH_MODO ..> UC_SUP_01 : <<extend>> (SwitchModo)
 UI_BADGE ..> UC_SUP_01 : <<extend>> (NotificarAgente)
 STOP_MONITOR ..> UC_SUP_01 : <<extend>>
 AUTO_STOP ..> UC_SUP_01 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_SEGMENTO --> SegmentResolver
 ESTABLECER_LISTEN --> Call
 TONO_AUDIBLE --> Operator
 UI_BADGE --> Operator
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of TONO_AUDIBLE
   Compliance legal: tono audible
   obligatorio al Operator al
   iniciar monitor. Caller no oye.
   Whisper permite supervisor
   instruir al Operator audible.
 end note

 note bottom of AUDITAR
   P-39 audit reforzado:
   reason + mode + supervisor +
   call_id + Operator afectado.
   Operacion muy sensitiva
   (CNST-013 + CNST-025).
 end note

 note right of Caller
   Caller percibe:
   - silent: nada
   - whisper: nada
   - barge-in (UC_SUP_02): si oye
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call objetivo del monitoreo.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session del Operator afectada (state badge).
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica monitor_live_calls.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   valida agent target en segmento del supervisor (CNST-008).
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent CALL_MONITORED (P-39 reforzado).
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-013/025).

 **UCs relacionados**:

 - :doc:`/requisitos/casos-uso/supervision/uc-sup-02/index` —
   Barge-in (3-way) escalacion de UC_SUP_01.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-02/index` —
   Operator atendiendo la llamada que se monitorea.

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index` — Parte 1-12.
