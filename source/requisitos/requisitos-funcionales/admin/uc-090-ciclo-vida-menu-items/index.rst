.. meta::
 :artefacto: UC-090
 :tipo: Caso de Uso (spec-from-code)
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-090:

============================================
UC-090: Ciclo de Vida (Lifecycle) de MenuItem
============================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo API**
   - ``UC_ADM_05``
 * - **Marker codigo UI**
   - ``UC_ADM_05``
 * - **Actor**
   - Administrador de UI / Sistema (auto-archivo)
 * - **Modulo**
   - MOD_Admin

Proposito
=========

Gestionar las transiciones de estado de ``MenuItem`` siguiendo
una state machine estricta + auto-archivado tras ``N`` dias en
``DEPRECATED``.

State machine
=============

::

   DRAFT --> ACTIVE --> DEPRECATED --> ARCHIVED (terminal)

Transiciones permitidas (``MenuLifecycleService.VALID_TRANSITIONS``):

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Estado origen
   - Estados destino permitidos
 * - DRAFT
   - ACTIVE
 * - ACTIVE
   - DEPRECATED
 * - DEPRECATED
   - ARCHIVED
 * - ARCHIVED
   - (terminal — sin salida)

Auto-archivado
==============

* ``MenuLifecycleService.AUTO_ARCHIVE_DAYS = 90``: MenuItems
  en estado ``DEPRECATED`` por mas de 90 dias se transicionan
  automaticamente a ``ARCHIVED``.
* Tarea ejecutada por scheduler (ver
  ``apps/access/scheduler.py`` si aplica).

Endpoints
=========

* ``PATCH /api/access/menu-items/<pk>/transition/`` con payload
  ``{new_status, block_reason?}``.
* Validacion estricta: transition rechaza si ``new_status`` no
  esta en ``VALID_TRANSITIONS[current]``.

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-090-01-validar-transiciones
 fr-090-02-auto-archive-deprecated
