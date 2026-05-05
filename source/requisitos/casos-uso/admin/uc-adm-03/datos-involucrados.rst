.. _uc-adm-03-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 FunctionGroup (AGR de sistema)
===================================

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
   - AGR-001..012
 * - is_system
   - bool
   - True para AGR de sistema
 * - functions
   - M2M -> Function
   - composicion actual
 * - created_at, updated_at
   - timestamp
   -

7.2 GroupFunction (tabla intermedia)
=====================================

- group_id, function_id, added_by, added_at.

7.3 AuditEvent generados
========================

- ``AGR_FUNCTION_ADDED``
- ``AGR_FUNCTION_REMOVED``

7.4 Indices
===========

- ``GroupFunction(group_id)`` — composicion.
- ``GroupFunction(function_id)`` — referencias cruzadas.

7.5 Datos NO involucrados
=========================

- Asignacion de AGR a usuarios (MOD_Access,
  UC_ACC_01/02).
- Grupos custom (UC_PERM_05/06).
