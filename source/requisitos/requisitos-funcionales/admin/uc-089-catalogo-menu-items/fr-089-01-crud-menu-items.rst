.. meta::
 :artefacto: FR-089.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-089-01:

==========================================
FR-089.01: CRUD de MenuItems
==========================================

1. Identificacion
-----------------

* **ID:** FR-089.01
* **UC origen:** UC-089 (UC_ADM_04)
* **Modulo:** MOD_Admin
* **Tipo:** Mutacion
* **Permission:** ACC-003

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE permitir crear, listar, modificar
y eliminar entradas del catalogo de ``MenuItem`` via ModelViewSet
DRF estandar, con persistencia inmediata en BD.

**Comportamiento implementado:**

* ``MenuItemViewSet`` (``apps/access/views.py:1039``) — DRF
  ModelViewSet con CRUD completo.
* Campos del modelo: ``code``, ``label``, ``icon``, ``path``,
  ``parent``, ``order``, ``status`` (DRAFT/ACTIVE/DEPRECATED/
  ARCHIVED), ``required_function`` (FK opcional a Function).
* Filtros: ``status``, ``parent``, ``required_function``.
* Ordering: ``order``, ``code``, ``label``.

3. Criterios de aceptacion
--------------------------

* CA-01: POST con payload valido + ACC-003 -> 201.
* CA-02: PATCH parcial soportado.
* CA-03: DELETE soportado pero la baja real depende de la
  transicion de estado (ver UC-090).
* CA-04: code unico (constraint BD).

4. Trazabilidad
---------------

* **TST:** ``IACT-ui/src/pages/admin/__tests__/MenuItemCatalogPage.test.jsx``
* **Codigo:** ``apps/access/views.py MenuItemViewSet``.
