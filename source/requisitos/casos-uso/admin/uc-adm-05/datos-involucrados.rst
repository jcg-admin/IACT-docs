.. meta::
 :artefacto: UC_ADM_05_DATOS
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==========================
7. Datos Involucrados
==========================

7.1 Campos del MenuItem usados por UC_ADM_05
============================================

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Campo
   - Tipo
   - Uso en UC_ADM_05
 * - ``status``
   - choice
   - LECTURA (validacion) + ESCRITURA (transicion)
 * - ``deprecated_at``
   - datetime null
   - ESCRITURA en transiciones que lo derivan
 * - ``archived_at``
   - datetime null
   - ESCRITURA en transiciones que lo derivan
 * - ``block_auto_archive``
   - bool
   - ESCRITURA en FA-05 / FA-06
 * - ``block_reason``
   - varchar(500)
   - ESCRITURA en FA-05
 * - ``block_set_by``
   - FK User
   - ESCRITURA en FA-05
 * - ``block_set_at``
   - datetime null
   - ESCRITURA en FA-05
 * - ``function``
   - FK Function
   - LECTURA (validacion is_active=True en publish)

7.2 Nuevos campos respecto a UC_ADM_04
======================================

UC_ADM_04 maneja los campos de metadata UX (display_label,
icon, route_path, parent, display_order). UC_ADM_05 agrega
gestion de:

- ``deprecated_at``, ``archived_at`` (derivados de
  transicion).
- Cuarteto block: ``block_auto_archive``, ``block_reason``,
  ``block_set_by``, ``block_set_at``.

7.3 Audit events emitidos
=========================

.. list-table::
 :widths: 35 15 50
 :header-rows: 1

 * - event_type
   - flujo
   - Payload
 * - ``MENU_ITEM_LIFECYCLE_TRANSITION``
   - principal, FA-01, FA-02, FA-03, FA-07
   - actor, before_status, after_status, deprecated_at,
     archived_at, block_flag_cleared (si aplica)
 * - ``LIFECYCLE_AUTO_ARCHIVED``
   - FA-04
   - actor='system', menu_item_id, deprecated_at,
     days_in_deprecated
 * - ``MENU_ITEM_BLOCK_FLAG_SET``
   - FA-05
   - actor, block_reason, timestamp
 * - ``MENU_ITEM_BLOCK_FLAG_CLEARED``
   - FA-06
   - actor, timestamp, previous_block_reason (redactado)

7.4 Origen de los datos
=======================

- ``MenuItem`` proviene de UC_ADM_04 (creacion).
- ``Function.is_active`` provista por UC_ADM_03.
- ``actor='system'`` en auto-archive proviene del service
  account del Planificador de Tareas.

7.5 Indices que sostienen el job de auto-archive
================================================

El query del Planificador es:

::

   SELECT id FROM menu_items
    WHERE status = 'DEPRECATED'
      AND deprecated_at < (NOW() - INTERVAL '90 days')
      AND block_auto_archive = FALSE;

El indice ``deprecated_at`` (de los 13 P3) cubre la
clausula ``deprecated_at < ?`` con scan eficiente. El
scan adicional por ``status`` y ``block_auto_archive`` es
soportado por el indice composite si la cardinalidad lo
justifica (Phase 7 puede agregar
``(status, deprecated_at, block_auto_archive)`` si
benchmark lo amerita).
