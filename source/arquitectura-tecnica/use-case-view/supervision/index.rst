.. meta::
 :artefacto: AT_UC_MOD_SUPERVISION
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_supervision:

====================================================
MOD_Supervision — Supervision en Vivo: UC por Modulo
====================================================

Monitoreo en tiempo real de llamadas activas, intervención
de supervisor y comunicación con el equipo de agentes.
Requiere rol ``Supervisor`` (AGR-003 quality_supervisor).

.. uml::
 :caption: MOD_Supervision — Supervisor monitorea, interviene
           y comunica al equipo de Operators.

 @startuml
 left to right direction

 actor Supervisor
 actor Operator

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamadas\nen Vivo" as MONITOREAR
   usecase "UC_SUP_02\nIntervenir en\nLlamada (barge in)" as INTERVENIR
   usecase "UC_SUP_03\nEnviar Mensaje\nal Equipo" as ENVIAR_MENSAJE
 }

 Supervisor --> MONITOREAR
 Supervisor --> INTERVENIR
 Supervisor --> ENVIAR_MENSAJE

 ENVIAR_MENSAJE --> Operator

 INTERVENIR ..> MONITOREAR : <<include>>

 note right of MOD_Supervision
   Codenames RBAC:
     Supervisor (AGR-003) →
       monitor_live_calls,
       barge_in_calls,
       broadcast_team_messages
     Operator (AGR-001): rol receptor de
       UC_SUP_03 (no inicia, recibe).
 end note

 @enduml

Lectura del diagrama
====================

- ``Supervisor`` (AGR-003) inicia los 3 UCs.
- ``Operator`` aparece como **actor receptor** (a la
  derecha de ``UC_SUP_03``) — el supervisor envía el
  mensaje, el operador lo recibe. Patrón canónico
  *actor que se beneficia* per
  ``uml-07/representacion-de-un-modelo-de-caso-de-uso``.
- ``UC_SUP_02 Intervenir`` ``<<include>>``
  ``UC_SUP_01 Monitorear``: la intervención requiere
  estar monitoreando previamente.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/call` — Call (UC_SUP_01 monitoreo).
- :doc:`/arquitectura-tecnica/domain-model/user` — User (operador receptor de UC_SUP_03).


.. toctree::
 :maxdepth: 1
 :caption: Casos de uso del módulo

 uc-sup-01/index
 uc-sup-02/index
 uc-sup-03/index

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
