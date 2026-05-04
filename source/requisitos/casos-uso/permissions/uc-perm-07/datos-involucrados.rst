.. _uc-perm-07-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Entidad
   - Uso
 * - **User**
   - validar existencia + estado activo
 * - **Function**
   - validar existencia (catalogo)
 * - **ExceptionalPermission**
   - check REVOKE / GRANT activo
 * - **Assignment**
   - via AGR
 * - **AccessGroup**
   - validar ACTIVE
 * - **AccessGroupFunction**
   - composicion AGR
 * - **PermissionCache**
   - lookup / write

7.2 Entidades escritas
======================

NINGUNA. Operacion read-only.

PermissionCache no es entidad de dominio,
es infraestructura.

7.3 Modelo de cache
===================

Key:

.. note::

 Los detalles de implementacion de esta regla estan delegados
 al documento tecnico de la capa de persistencia y servicio.
 Esta especificacion describe el QUE y el POR QUE, no el COMO.

Value:

.. note::

 Los detalles de implementacion de esta regla estan delegados
 al documento tecnico de la capa de persistencia y servicio.
 Esta especificacion describe el QUE y el POR QUE, no el COMO.

TTL: ``min(default_ttl, remaining_validity)``
= 60s typical, < 60s si concesion proxima a
expirar.

7.4 Indices criticos
====================

Para que el algoritmo cumpla P50 ≤ 25 ms en
cache miss:

- ``ExceptionalPermission(user_id,
  function_code, type, state)`` — covering
- ``Assignment(user_id, target_type, state,
  valid_until)``
- ``AccessGroupFunction(access_group_id,
  function_code)``

7.5 Query agregada (cache miss)
===============================

Stack-agnostico, una sola peticion:

.. note::

 Los detalles de implementacion de esta regla estan delegados
 al documento tecnico de la capa de persistencia y servicio.
 Esta especificacion describe el QUE y el POR QUE, no el COMO.

Nota: representacion conceptual; cada motor
expresa esto en su dialecto. Lo importante es
que sea **una** ida-vuelta a BD.

7.6 Bulk query
==============

Para ``check_bulk(user_id, function_codes
[])``: la query agrega resultados por
function_code en lugar de filtrar por uno.
Igualmente una ida-vuelta.

7.7 Datos NO involucrados
=========================

- AuditEvent — no se emite por check.
- PII del User — no necesaria, solo id.
- Modulo / segmento — no determinan
  ``allowed``; CNST-008 aplica al USAR la
  funcion, no al chequearla.
