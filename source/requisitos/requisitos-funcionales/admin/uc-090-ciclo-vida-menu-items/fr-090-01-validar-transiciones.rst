.. meta::
 :artefacto: FR-090.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-090-01:

==================================================
FR-090.01: Validar transiciones de estado MenuItem
==================================================

1. Identificacion
-----------------

* **ID:** FR-090.01
* **UC origen:** UC-090 (UC_ADM_05)
* **Modulo:** MOD_Admin
* **Tipo:** Validacion + mutacion
* **Permission:** ACC-003

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE rechazar transiciones de estado
que no esten en la state machine ``VALID_TRANSITIONS`` y aplicar
solo las permitidas, manteniendo audit trail.

**Comportamiento implementado:**

* ``MenuLifecycleService.transition(item, new_status,
  block_reason=None)``:

  - Si ``new_status not in VALID_TRANSITIONS[item.status]`` ->
    raises ``ValidationError`` (HTTP 400 desde view).
  - Si valido: actualiza ``item.status`` + ``item.save()``.
  - Si transition a ``DEPRECATED`` o ``ARCHIVED`` con
    ``block_reason``, lo persiste en ``deprecation_reason`` /
    ``archive_reason``.

* Endpoint: ``PATCH /api/access/menu-items/<pk>/transition/``.

3. Criterios de aceptacion
--------------------------

* CA-01: ``DRAFT->ACTIVE`` -> 200.
* CA-02: ``ACTIVE->DRAFT`` (no permitida) -> 400 + mensaje
  con transiciones validas.
* CA-03: ``ARCHIVED->cualquier-estado`` -> 400 (terminal).
* CA-04: ``new_status`` invalido (no en STATUS_CHOICES) -> 400.

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_menu_lifecycle.py``
* **Codigo:** ``apps/access/services/menu_lifecycle_service.py
  MenuLifecycleService.transition()`` + ``apps/access/views.py
  @action transition``.
