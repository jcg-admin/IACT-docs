.. meta::
 :artefacto: ARQ_MOD_009_DIAG_SECUENCIA_ATENCION
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/operator/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_009_secuencia_atencion_llamada:

=========================================
Secuencia de Atencion de Llamada Entrante
=========================================

.. uml::
 :caption: Secuencia UC_OPR_02 — atencion de llamada entrante con disposicion post-llamada.

 @startuml

 actor "answer_inbound_calls" as answer_inbound_calls
 participant "AgentPanel\n(/api/v1/operator/)" as Agentpanel
 participant "TelephonyRouter\n(ACD/IVR)" as Telephonyrouter
 participant "DispositionEndpoint\n(/api/v1/disposition/)" as DISP
 database "audit_log\n(PostgreSQL)" as audit_log

 Telephonyrouter -> Agentpanel : llamada entrante asignada al agente
 Agentpanel -> answer_inbound_calls : notificacion de llamada
 answer_inbound_calls -> Agentpanel : POST /answer
 Agentpanel -> Agentpanel : JWT + RBAC (answer_inbound_calls)
 Agentpanel -> Telephonyrouter : conectar canal audio
 Telephonyrouter --> answer_inbound_calls : canal de voz activo

 note over answer_inbound_calls, Telephonyrouter
   Operador atiende la llamada.
   Estado del agente = busy.
 end note

 answer_inbound_calls -> Agentpanel : POST /disposition {code, notes}
 Agentpanel -> Agentpanel : JWT + RBAC (enter_call_disposition)
 Agentpanel -> DISP : registrar disposition record
 Agentpanel -> audit_log : registrar AuditEvent CALL_DISPOSED
 Agentpanel -> Telephonyrouter : liberar canal
 Telephonyrouter --> Agentpanel : agente disponible
 Agentpanel --> answer_inbound_calls : 200 OK, estado = available

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/operator/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
