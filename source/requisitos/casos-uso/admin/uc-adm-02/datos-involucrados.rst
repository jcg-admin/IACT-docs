.. _uc-adm-02-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Function
============

.. list-table::
 :widths: 25 25 50

 * - Campo
   - Tipo
   - Notas
 * - id
   - uuid
   - PK
 * - codename
   - string
   - unico, snake_case, inmutable
 * - description
   - text
   - actualizable
 * - module
   - enum
   - MOD_Auth, MOD_User, MOD_Access,
     MOD_Permissions, MOD_Admin, etc.
 * - scope
   - string
   - alcance de la funcion
 * - is_active
   - bool
   - BR-009 soft-deactivate
 * - version_added
   - string
   - ej. v5.6.0 para nuevas funciones
 * - created_at, updated_at
   - timestamp
   -

7.2 AuditEvent generados
========================

- ``FUNCTION_CREATED``
- ``FUNCTION_UPDATED``
- ``FUNCTION_DEACTIVATED``

7.3 Indices
===========

- ``Function(codename)`` — unicidad.
- ``Function(module, is_active)`` — filtros frecuentes.

7.4 Datos NO involucrados
=========================

- Asignaciones de funciones a usuarios (MOD_Access).
- Grupos predefinidos (UC_ADM_03).
