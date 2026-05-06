.. _uc-adm-03-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

CA-01: Agregar funcion a AGR sistema → 201.
CA-02: Funcion ya asignada → 409.
CA-03: Funcion inexistente en catalogo → 400.
CA-04: Conflicto SoD detectado → 400 + detalle.
CA-05: AGR no de sistema → 403.
CA-06: Remover funcion → effective_set
recalculado para todos los usuarios del AGR.
CA-07: Vista /impact/ retorna numero de
usuarios afectados sin modificar.
CA-08: Audit completo (ADDED/REMOVED).
CA-09: Sin AGR-010 → 403.
CA-10: PermissionsEngine recalcula tras cambio.

Resumen
=======

.. list-table::
 :widths: 12 50 38

 * - ID
   - Concepto
   - Tipo
 * - CA-01..05
   - CRUD + validation
   - Funcional
 * - CA-06
   - Recalculo effective_set
   - Integracion
 * - CA-07
   - Impact preview
   - UX
 * - CA-08
   - Audit
   - Compliance
 * - CA-09
   - Auth
   - Seguridad
 * - CA-10
   - Engine reload
   - Integracion
