.. meta::
 :artefacto: AT_UC_MOD_SUPERVISION
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_supervision:

====================================================
MOD_Supervision — Supervision en Vivo: UC por Modulo
====================================================

MOD_Supervision — Supervision en Vivo
========================================

Monitoreo en tiempo real de llamadas activas, intervencion de
supervisor y comunicacion con el equipo de agentes. Requiere
funciones de supervision especificas.

.. uml::
 :caption: Figura 26 — MOD_Supervision: casos de uso

 @startuml
 left to right direction

 actor "monitor_live_calls" as monitor_live_calls
 actor "barge_in_calls" as barge_in_calls
 actor "broadcast_team_messages" as broadcast_team_messages

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamadas\nen Vivo" as S01
   usecase "UC_SUP_02\nIntervenir en\nLlamada\n(barge in)" as S02
   usecase "UC_SUP_03\nEnviar Mensaje\nal Equipo" as S03
 }

 monitor_live_calls --> S01
 barge_in_calls --> S02
 broadcast_team_messages --> S03

 S02 ..> S01 : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
