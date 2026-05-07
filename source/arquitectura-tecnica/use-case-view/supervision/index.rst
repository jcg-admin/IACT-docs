.. meta::
 :artefacto: AT_UC_MOD_SUPERVISION
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Reservado
 :version: 2.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_supervision:

====================================================
MOD_Supervision — Supervision en Vivo: UC por Modulo
====================================================

.. warning:: Modulo reservado (out-of-scope para v5.6.0)

 Vista arquitectonica de un **extension point open-closed** del
 modelo RBAC v5.6.0. Las 3 funciones (UC_SUP_01..03) estan
 declaradas en el catalogo pero NO son implementables en esta
 release. El diagrama UML y la especificacion se preservan como
 base de diseño para activacion futura.

 Especificacion de los UCs:
 :doc:`/requisitos/casos-uso/supervision/index`. Modelo RBAC:
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

Monitoreo en tiempo real de llamadas activas, intervención
de supervisor y comunicación con el equipo de agentes.
Requiere AGR-003 ``quality_supervisor`` (Supervisor).

.. uml::
 :caption: MOD_Supervision — Supervisor monitorea, interviene
           y comunica al equipo de Operators.

 @startuml
 left to right direction

 actor Supervisor
 actor Operator

 actor Caller
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
 MONITOREAR --> Operator
 INTERVENIR --> Caller

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

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_SUP_01 </requisitos/casos-uso/supervision/uc-sup-01/index>`
   - Monitorear Llamada (Whisper)
   - :doc:`Diagrama </requisitos/casos-uso/supervision/uc-sup-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_SUP_02 </requisitos/casos-uso/supervision/uc-sup-02/index>`
   - Barge-in en Llamada
   - :doc:`Diagrama </requisitos/casos-uso/supervision/uc-sup-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_SUP_03 </requisitos/casos-uso/supervision/uc-sup-03/index>`
   - Mensaje Broadcast al Equipo
   - :doc:`Diagrama </requisitos/casos-uso/supervision/uc-sup-03/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

UC standalone uml-07
====================

Diagramas standalone uml-07 por UC (auto-explicativos):

.. toctree::
 :maxdepth: 1

 uc-sup-01-monitorear-llamada-whisper
 uc-sup-02-barge-in-en-llamada
 uc-sup-03-mensaje-broadcast-al-equipo
