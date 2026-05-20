.. meta::
 :artefacto: FR-086.03
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-086-03:

================================================================
FR-086.03: Endpoint de pre-validacion (preview) de violaciones
================================================================

1. Identificacion
-----------------

* **ID:** FR-086.03
* **UC origen:** UC-086
* **Modulo:** MOD_Admin
* **Tipo:** Consulta (preview)
* **Permission:** ACC-005

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE exponer un endpoint que valide
si un set de funciones propuesto violaria alguna regla SoD del
catalogo, **sin** aplicar la asignacion. Permite al cliente
hacer preview antes de invocar el endpoint de asignacion
(UC_ACC_01 / UC_PERM_01).

**Comportamiento implementado:**

* ``POST /api/access/separation-rules/validate`` con payload
  ``{user_id, proposed_function_codes: [...]}``.
* Responde lista de violaciones (vacia si no hay).
* No muta BD ni emite audit (es preview).

3. Criterios de aceptacion
--------------------------

* CA-01: sin violaciones -> ``{"violations": []}``.
* CA-02: con violaciones HARD -> lista con ``severity='HARD'`` +
  ``conflict_set``.
* CA-03: cliente UI puede invocar antes del POST asignar para
  evitar 409 inesperado.

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_separation_rules.py``
* **Codigo:** ``apps/access/separation_rule_view.py`` (validate
  endpoint canonico despues de STD_008 FASE 3).
* **Consumido por:** ``DutySeparationValidator.validate()`` en
  ``apps/access/services/permission_service.py`` (FR-010.02).
