.. meta::
 :artefacto: UC-089
 :tipo: Caso de Uso (spec-from-code)
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-089:

==========================================
UC-089: Catalogo de MenuItems
==========================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo API**
   - ``UC_ADM_04``
 * - **Marker codigo UI**
   - ``UC_ADM_04``
 * - **Actor**
   - Administrador de UI / Producto
 * - **Modulo**
   - MOD_Admin
 * - **Relacionado**
   - UC_PERM_08 (generar menu dinamico): este UC administra el
     catalogo desde el cual UC_PERM_08 deriva el menu del usuario.

Proposito
=========

CRUD del catalogo de ``MenuItem`` — entradas de menu de la UI
(iconos, rutas, parent, orden, permission required). Las rutas
del menu del usuario final se derivan filtrando este catalogo
por permisos efectivos.

Endpoints implementados
=======================

.. list-table::
 :header-rows: 1
 :widths: 35 15 50

 * - Path
   - Metodo
   - Permission required
 * - ``/api/access/menu-items/``
   - GET / POST
   - ``ACC-003``
 * - ``/api/access/menu-items/<pk>/``
   - GET / PATCH / DELETE
   - ``ACC-003``

UI: ``IACT-ui/src/pages/admin/MenuItemCatalog.jsx`` +
``MenuItemCatalogPage.test.jsx``.

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-089-01-crud-menu-items
 fr-089-02-bulk-reorder-items
