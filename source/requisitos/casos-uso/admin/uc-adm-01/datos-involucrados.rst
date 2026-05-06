.. _uc-adm-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 SoDRule
===========

.. list-table::
 :widths: 25 25 50

 * - Campo
   - Tipo
   - Notas
 * - id
   - uuid
   - PK
 * - name
   - string
   - unico
 * - group_a
   - JSON list
   - codenames de funciones
 * - group_b
   - JSON list
   - codenames de funciones
 * - rationale
   - text
   - justificacion de negocio
 * - state
   - ACTIVE | INACTIVE
   - BR-009 bajas logicas
 * - version
   - int
   - incrementado por update
 * - created_by
   - int
   - AGR-010 user_id
 * - created_at, updated_at
   - timestamp
   -

7.2 AuditEvent generados
========================

- ``SOD_RULE_CREATED``
- ``SOD_RULE_UPDATED``
- ``SOD_RULE_DISABLED``
- ``SOD_RULE_REACTIVATED``

7.3 Indices
===========

- ``SoDRule(state)`` — enforcement filtra por ACTIVE.
- ``SoDRule(name)`` — unicidad.

7.4 Datos NO involucrados
=========================

- Asignaciones de usuarios (MOD_Access).
- Grupos predefinidos directamente (UC_ADM_03).
