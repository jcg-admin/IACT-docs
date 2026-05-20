.. meta::
 :artefacto: FR-088.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-088-01:

==========================================
FR-088.01: Listar catalogo de AGR
==========================================

1. Identificacion
-----------------

* **ID:** FR-088.01
* **UC origen:** UC-088 (UC_ADM_03)
* **Modulo:** MOD_Admin
* **Tipo:** Consulta
* **Permission:** ACC-005 (compartida con UC-016)

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE exponer la lista de AGRs
activos junto con su composicion (Functions miembros), para
que el catalogo admin pueda mostrar la estructura completa.

**Comportamiento implementado:**

* ``GET /api/access/access-groups/`` (AccessGroupListCreateView).
  Lista AGRs con metadata: ``code``, ``name``, ``is_predefined``,
  ``is_active``, ``function_count``.
* ``GET /api/access/access-groups/<agr_id>/`` retorna detalle
  incluyendo la lista de Functions del grupo.

3. Criterios de aceptacion
--------------------------

* CA-01: actor con ``ACC-005`` -> 200 lista AGRs.
* CA-02: detalle muestra ``functions: [...]`` con codigos.
* CA-03: AGRs retirados (``is_active=False``) se incluyen con
  marca — el filtrado lo decide el cliente.
* CA-04: AGRs predefinidos (``is_predefined=True``) marcados —
  el cliente no debe permitir editarlos (delegado a UC-016
  validacion).

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_access_group_management.py``,
  ``IACT-ui/src/pages/admin/__tests__/AGRComposition.test.jsx``
* **Codigo:** ``apps/access/access_group_view.py
  AccessGroupListCreateView`` + ``AccessGroupDetailView``.
* **UI:** ``IACT-ui/src/pages/admin/AGRCatalog.jsx``.
