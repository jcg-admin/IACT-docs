.. meta::
 :artefacto: FR-089.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-089-02:

============================================
FR-089.02: Bulk reorder + block-archive
============================================

1. Identificacion
-----------------

* **ID:** FR-089.02
* **UC origen:** UC-089 (UC_ADM_04 + UC_ADM_05)
* **Modulo:** MOD_Admin
* **Tipo:** Mutacion bulk
* **Permission:** ACC-003

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE soportar operaciones bulk sobre
multiples MenuItems en un solo request para facilitar la
administracion (reorder y archive masivos).

**Comportamiento implementado:**

* Endpoints DRF generados via ``MenuItemViewSet`` con actions
  custom (consultar implementacion).
* La UI (``IACT-ui/src/redux/slices/admin.js``) tiene thunks
  ``bulkReorderMenuItems`` y ``bulkBlockArchiveMenuItems``.

3. Criterios de aceptacion
--------------------------

* CA-01: bulk reorder acepta lista ``[{id, order}, ...]`` y
  persiste en transaction.
* CA-02: bulk block-archive transiciona varios items a
  ``ARCHIVED`` en un solo request.

4. Trazabilidad
---------------

* **Codigo API:** ``apps/access/views.py MenuItemViewSet``.
* **Codigo UI:** ``IACT-ui/src/redux/slices/admin.js`` actions
  ``bulkReorderMenuItems``, ``bulkBlockArchiveMenuItems``.
