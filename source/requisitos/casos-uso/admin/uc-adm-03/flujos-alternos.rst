.. _uc-adm-03-parte-04:

==========================
Parte 4 — Flujos alternos
==========================

FA-01: Funcion no existe en catalogo: 400.
FA-02: Funcion ya asignada al grupo: 409.
FA-03: Funcion genera conflicto de separacion con otras
funciones del grupo: 400 + detalle de regla
Separacion violada.
FA-04: AGR objetivo no es de sistema
(is_system=False): 403 (usar UC_PERM_06).
FA-05: Ver impacto antes de cambiar: GET
/impact/ retorna preview sin modificar.

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
   - Ya asignada
   - 409
   - idempotencia
 * - FA-03
   - Conflicto de separacion
   - 400 + regla
   - UC_ADM_01
 * - FA-04
   - No es_sistema
   - 403
   - usar UC_PERM_06
 * - FA-05
   - Preview impacto
   - 200 informativo
   - no modifica
