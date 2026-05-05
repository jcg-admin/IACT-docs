.. meta::
 :artefacto: ARQ_MOD_010_DIAG_BARGE_IN
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/supervision/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_010_barge_in_tripartita:

==================================
Barge-In — Intervencion Tripartita
==================================

.. uml::
 :caption: Estado de canal en barge-in — supervisor, agente y cliente conectados.

 @startuml

 [*] --> canal_agente_cliente : llamada activa\n(answer_inbound_calls)

 canal_agente_cliente --> supervision_activa : monitor_live_calls\n(silent/whisper)

 supervision_activa --> canal_tripartito : barge_in_calls
 canal_tripartito --> canal_agente_cliente : supervisor abandona\n(barge_in_calls off)
 supervision_activa --> canal_agente_cliente : supervisor abandona\nmonitoreo

 canal_agente_cliente --> [*] : llamada finalizada
 canal_tripartito --> [*] : llamada finalizada

 note right of canal_tripartito
   Los tres canales estan activos.
   Tono de supervision emitido
   en cada transicion (compliance).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/supervision/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
