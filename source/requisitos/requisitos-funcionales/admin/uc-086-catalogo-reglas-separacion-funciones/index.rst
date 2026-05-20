.. meta::
 :artefacto: UC-086
 :tipo: Caso de Uso (spec-from-code)
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-086:

============================================================
UC-086: Catalogo de Reglas de Separacion de Funciones (SoD)
============================================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo API**
   - ``UC_ADM_01``
 * - **Marker codigo UI**
   - ``UC_ADM_01``
 * - **Actor**
   - Administrador de seguridad
 * - **Modulo**
   - MOD_Admin
 * - **Solape**
   - Las reglas son consumidas por UC_ACC_01 (FR-010.02 SoD)

Proposito
=========

CRUD canonico de las reglas que el sistema usa para detectar
violaciones de separacion de funciones (SoD) al asignar
``Function`` o ``AccessGroup`` a un usuario (UC_ACC_01 /
UC_PERM_01). Este UC NO **aplica** las reglas — solo las
**administra**.

Endpoints implementados
=======================

.. list-table::
 :header-rows: 1
 :widths: 35 15 50

 * - Path
   - Metodo
   - Permission required
 * - ``/api/access/separation-rules/``
   - GET
   - ``ACC-005`` view_separation_rules
 * - ``/api/access/separation-rules/``
   - POST
   - ``ACC-011`` create_separation_rules
 * - ``/api/access/separation-rules/<rule_id>/``
   - GET
   - ``ACC-005``
 * - ``/api/access/separation-rules/<rule_id>/``
   - PATCH
   - ``ACC-012`` modify_separation_rules
 * - ``/api/access/separation-rules/<rule_id>/``
   - DELETE
   - ``ACC-011``
 * - ``/api/access/separation-rules/validate``
   - POST
   - ``ACC-005`` (preview-mode)

UI: ``IACT-ui/src/pages/admin/SeparationRulesCatalog.jsx``.

Eventos de auditoria emitidos
==============================

* ``SEPARATION_RULE_CREATED``
* ``SEPARATION_RULE_UPDATED``
* ``SEPARATION_RULE_DISABLED``

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-086-01-listar-reglas-separacion
 fr-086-02-crear-regla-separacion
 fr-086-03-validar-reglas-en-asignacion
