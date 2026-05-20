.. meta::
 :artefacto: FR-086.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-086-01:

============================================
FR-086.01: Listar reglas de separacion (SoD)
============================================

1. Identificacion
-----------------

* **ID:** FR-086.01
* **UC origen:** UC-086 (UC_ADM_01)
* **Modulo:** MOD_Admin
* **Tipo:** Consulta
* **Permission:** ACC-005

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE exponer un endpoint que retorne
todas las reglas SoD vigentes y sus metadatos cuando el actor
posee ``ACC-005``.

**Comportamiento implementado:**

* ``GET /api/access/separation-rules/`` retorna lista paginada.
* Cada regla incluye: ``rule_id``, ``code``, ``severity``
  (HARD/SOFT), ``conflict_set`` (codigos de Function en
  conflicto), ``description``, ``is_active``.
* Sin permission ``ACC-005`` -> 403.

3. Criterios de aceptacion
--------------------------

* CA-01: actor con ``ACC-005`` -> 200 con lista.
* CA-02: actor sin permission -> 403.
* CA-03: regla inactiva (``is_active=False``) aparece en la
  respuesta marcada — el filtrado lo decide el cliente.

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_separation_rules.py``
* **Codigo:** ``apps/access/separation_rule_view.py
  SeparationRuleListCreateView.get()``
