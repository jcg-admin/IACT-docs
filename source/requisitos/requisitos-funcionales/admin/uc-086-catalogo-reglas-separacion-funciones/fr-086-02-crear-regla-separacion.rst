.. meta::
 :artefacto: FR-086.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-086-02:

==========================================
FR-086.02: Crear / Modificar regla de SoD
==========================================

1. Identificacion
-----------------

* **ID:** FR-086.02
* **UC origen:** UC-086
* **Modulo:** MOD_Admin
* **Tipo:** Mutacion
* **Permission:** ACC-011 (crear) / ACC-012 (modificar)

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE permitir crear y modificar reglas
SoD via API protegida por permission, persistiendo cambios en BD
y emitiendo audit canonico inmutable (CNST-009).

**Comportamiento implementado:**

* ``POST /api/access/separation-rules/`` crea regla con
  ``conflict_set``, ``severity``, ``description``. Emite
  ``SEPARATION_RULE_CREATED``.
* ``PATCH /api/access/separation-rules/<rule_id>/`` modifica.
  Emite ``SEPARATION_RULE_UPDATED``.
* ``DELETE /api/access/separation-rules/<rule_id>/`` deshabilita
  (baja logica, ``is_active=False``). Emite
  ``SEPARATION_RULE_DISABLED``.

3. Criterios de aceptacion
--------------------------

* CA-01: POST con payload valido + ACC-011 -> 201 + audit emitido.
* CA-02: POST sin ACC-011 -> 403.
* CA-03: PATCH sin ACC-012 -> 403.
* CA-04: DELETE NO elimina fisicamente (baja logica
  ``is_active=False``).
* CA-05: audit emitido con ``target_entity_type='SeparationRule'``
  + ``target_entity_id=str(rule.pk)``.

4. Trazabilidad
---------------

* **TST:** ``tests/unit/access/test_separation_rules.py``
* **Codigo:** ``apps/access/separation_rule_view.py``
