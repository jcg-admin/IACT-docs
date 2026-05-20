.. meta::
 :artefacto: FR-087.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-087-01:

==================================================
FR-087.01: Listar catalogo de Functions del RBAC
==================================================

1. Identificacion
-----------------

* **ID:** FR-087.01
* **UC origen:** UC-087 (UC_ADM_02)
* **Modulo:** MOD_Admin
* **Tipo:** Consulta (readonly)
* **Permission:** ACC-003

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE exponer el catalogo completo
de ``Function`` (las primitivas de RBAC: ``USR-001``,
``ACC-005``, etc.) para administracion y UIs de asignacion.

**Comportamiento implementado:**

* ``GET /api/access/functions/`` retorna lista paginada de
  Functions con: ``id``, ``code``, ``name``, ``description``,
  ``module_code``, ``is_active``.
* Filtros: ``module``, ``is_active``, ``search``.
* Ordering: ``code``, ``module``, ``name``.
* Sin ``ACC-003`` -> 403.

3. Criterios de aceptacion
--------------------------

* CA-01: actor con ``ACC-003`` -> 200 con lista completa.
* CA-02: filtro por ``module=MOD_Users`` -> solo funciones USR-*.
* CA-03: search ``access`` -> match icontains en code/name.
* CA-04: actor sin permission -> 403.

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_function_catalog.py``
* **Codigo:** ``apps/access/views.py FunctionListView``
  (line 477).
* **Catalogo:** poblado por
  ``apps/access/management/commands/create_functions.py``.
