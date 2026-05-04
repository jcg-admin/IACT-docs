.. meta::
 :artefacto: ARQ_MOD_010_DIAG_FLUJO_MONITOREO
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/supervision/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_010_flujo_monitoreo_tiempo_real:

=================================
Flujo de Monitoreo en Tiempo Real
=================================

Flujo de Monitoreo en Tiempo Real
====================================

.. uml::
 :caption: Secuencia UC_SUP_01 — monitor_live_calls en modo silent/whisper con tono de supervision.

 @startuml

 actor "monitor_live_calls" as monitor_live_calls
 participant "SupervisionEndpoint\n(/api/v1/supervision/)" as Supervisionendpoint
 participant "TelephonyBridge\n(SIP/WebRTC)" as Telephonybridge
 participant "AuditLog" as Auditlog
 actor "answer_inbound_calls" as answer_inbound_calls

 monitor_live_calls -> Supervisionendpoint : POST /supervision/monitor {call_id, mode}
 Supervisionendpoint -> Supervisionendpoint : JWT + RBAC (monitor_live_calls)
 Supervisionendpoint -> Telephonybridge : conectar canal supervision\n(mode: silent|whisper)
 Telephonybridge -> answer_inbound_calls : emitir tono de supervision\n(compliance obligatorio)
 Telephonybridge --> Supervisionendpoint : canal activo
 Supervisionendpoint -> Auditlog : INSERT SupervisionEvent {tipo, supervisor, call_id}
 Supervisionendpoint --> monitor_live_calls : 200 OK

 note over monitor_live_calls, answer_inbound_calls
   En modo silent: supervisor escucha,
   agente y cliente no escuchan al supervisor.
   En modo whisper: supervisor habla al agente,
   cliente no escucha al supervisor.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/supervision/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
