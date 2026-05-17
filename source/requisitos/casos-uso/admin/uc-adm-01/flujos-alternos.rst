.. _uc-adm-01-parte-04:

==========================
Parte 4 — Flujos alternos
==========================

FA-01: Funcion no existe en catalogo activo:
rechazado con 400 + detalle de funcion invalida.
FA-02: Conjuntos no disjuntos (funcion aparece
en group_a y group_b): rechazado 400.
FA-03: Nombre duplicado: 409 Conflict.
FA-04: Desactivar regla ya inactiva: 409.
FA-05: Reactivar regla inactiva: PATCH
state=ACTIVE — enforcement recarga.

Resumen
=======

.. list-table::
 :widths: 12 38 30 20

 * - FA
   - Disparador
   - Comportamiento
   - Notas
 * - FA-01
   - Funcion inexistente
   - 400
   - UC_ADM_02
 * - FA-02
   - Conjuntos no disjuntos
   - 400
   - CNST-030
 * - FA-03
   - Nombre duplicado
   - 409
   - unicidad
 * - FA-04
   - Ya inactiva
   - 409
   -
 * - FA-05
   - Reactivar
   - ACTIVE + reload
   - enforcement
