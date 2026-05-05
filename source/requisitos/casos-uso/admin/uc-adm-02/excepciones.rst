.. _uc-adm-02-parte-05:

==========================
Parte 5 — Excepciones
==========================

EX-01: JWT invalido — 401.
EX-02: No tiene AGR-009 — 403.
EX-03: Codename duplicado — 409.
EX-04: Codename formato invalido — 400.
EX-05: Module invalido — 400.
EX-06: Function no existe — 404.
EX-07: BD timeout — 503.
EX-08: PermissionsEngine no responde — function guardada, reload async retry.

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
 * - EX-03..05
   - Validacion
   - 400/409
   - Validator
 * - EX-06
   - Not found
   - 404
   -
 * - EX-07
   - BD
   - 503
   -
 * - EX-08
   - Reload fallido
   - 201 parcial
   - async retry
