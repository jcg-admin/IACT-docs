.. _uc-adm-03-parte-05:

==========================
Parte 5 — Excepciones
==========================

EX-01: JWT invalido — 401.
EX-02: No tiene AGR-010 — 403.
EX-03: FunctionGroup no existe — 404.
EX-04: FunctionGroup no es de sistema — 403.
EX-05: Funcion no existe en catalogo — 400.
EX-06: Funcion ya asignada — 409.
EX-07: Conflicto SoD — 400.
EX-08: BD timeout — 503.
EX-09: PermissionsEngine no responde — cambio guardado, recalculo async retry.

Resumen
=======

.. list-table::
 :widths: 12 40 18 30
 :header-rows: 1

 * - ID
   - Condicion
   - Status
   - Notas
 * - EX-01..02
   - Auth / RBAC
   - 401/403
   - middleware
 * - EX-03..04
   - Group guard
   - 404/403
   - is_system check
 * - EX-05..07
   - Validacion
   - 400/409
   - Validator
 * - EX-08
   - BD
   - 503
   -
 * - EX-09
   - Recalculo fallido
   - 201 parcial
   - async retry
