.. meta::
 :artefacto: AT_DESIGN_STATE_MENU_ITEM
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: MenuItem
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_menu_item:

============================================================
Design View — Ciclo de Vida: MenuItem
============================================================

Maquina de estados de la entidad ``MenuItem``. ``MenuItem``
es metadata visual (label, icono, ruta, orden) con lifecycle
propio independiente de la ``Function`` que lo respalda. UC
asociado: ``UC_ADM_05`` (gestion de items de menu).

.. uml::
 :caption: MenuItem FSM — DRAFT/ACTIVE/DEPRECATED/ARCHIVED.

 @startuml

 [*] --> DRAFT : Admin.create_menu_item()

 DRAFT      --> ACTIVE     : Admin.publish()
 ACTIVE     --> DEPRECATED : Admin.deprecate()
 DEPRECATED --> ACTIVE     : Admin.reactivate()\n(limpia deprecated_at)
 DEPRECATED --> ARCHIVED   : Admin.archive()\nor auto 90d
 ARCHIVED   --> ACTIVE     : Admin.reactivate()\n(limpia archived_at)

 ARCHIVED   --> [*] : retencion (purga)

 note right of DRAFT
   Visible solo en la consola de
   admin. NO aparece en menus de
   usuarios finales.
 end note

 note right of ACTIVE
   Visible y navegable por usuarios
   con permiso (resuelto via la
   Function asociada).
 end note

 note bottom of DEPRECATED
   Marca temporal — el item sigue
   accesible pero el admin recibe
   warning. ``deprecated_at`` = now.
 end note

 note bottom of ARCHIVED
   Auto-transicion: 90 dias
   desde DEPRECATED. ``archived_at``
   = now. Reactivable.
 end note

 @enduml

Reglas de transicion
=====================

.. list-table::
 :widths: 28 38 34
 :header-rows: 1

 * - Transicion
   - Cambio en campos derivados
   - Block flags
 * - ``DRAFT → ACTIVE``
   - ``deprecated_at = NULL``,
     ``archived_at = NULL``
   - reset
 * - ``ACTIVE → DEPRECATED``
   - ``deprecated_at = now()``
   - sin cambio
 * - ``DEPRECATED → ACTIVE``
   - ``deprecated_at = NULL``
   - reset
 * - ``DEPRECATED → ARCHIVED``
   - ``archived_at = now()``
   - reset
 * - ``ARCHIVED → ACTIVE``
   - ``deprecated_at = NULL``,
     ``archived_at = NULL``
   - reset

Cualquier otra combinacion responde HTTP 409 Conflict.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/menu-item` —
   entidad y campo ``status``.
 - :doc:`/arquitectura-tecnica/domain-model/menu-lifecycle-service` —
   service que orquesta las transiciones.
 - :doc:`bounded-context` — contexto del modulo Admin.
 - :doc:`interaction-pattern` — patron de orquestacion admin.
