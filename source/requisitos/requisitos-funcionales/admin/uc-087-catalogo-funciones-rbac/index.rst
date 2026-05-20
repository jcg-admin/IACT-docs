.. meta::
 :artefacto: UC-087
 :tipo: Caso de Uso (spec-from-code)
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-087:

==========================================
UC-087: Catalogo de Funciones RBAC
==========================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo API**
   - ``UC_ADM_02``
 * - **Marker codigo UI**
   - ``UC_ADM_02``
 * - **Actor**
   - Administrador de seguridad
 * - **Modulo**
   - MOD_Admin
 * - **Solape**
   - Las funciones son consumidas por UC_ACC_01 (asignar)

Proposito
=========

Listado read-only del catalogo de ``Function`` registradas en
el sistema RBAC. El catalogo es **inmutable en runtime** —
se semi-poblado via comando management ``create_functions``
(ver ``apps/access/management/commands/create_functions.py``).
Este UC expone el catalogo para que las UI de asignacion
(UC_ACC_01) puedan presentar las funciones disponibles.

Endpoints implementados
=======================

.. list-table::
 :header-rows: 1
 :widths: 35 15 50

 * - Path
   - Metodo
   - Permission required
 * - ``/api/access/functions/``
   - GET
   - ``ACC-003`` view_functions

UI: ``IACT-ui/src/pages/admin/FunctionCatalog.jsx`` +
``FunctionCatalogPage.test.jsx``.

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-087-01-listar-catalogo-funciones
