.. _uc-adm-01-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

CA-01: Crear regla basica → 201 + SeparationRule en BD.
CA-02: Conjuntos no disjuntos rechazado 400.
CA-03: Funcion inexistente rechazada 400.
CA-04: Nombre duplicado → 409.
CA-05: Update incrementa version.
CA-06: Disable → INACTIVE; enforcement deja
de aplicarla en nuevas asignaciones.
CA-07: Reactivar → ACTIVE; enforcement recarga.
CA-08: Audit completo (CREATED/UPDATED/DISABLED).
CA-09: Sin AGR-010 → 403.
CA-10: EnforcementEngine recarga tras cada cambio.

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
 * - CA-06..07
   - State lifecycle
   - Robustez
 * - CA-08
   - Audit
   - Compliance
 * - CA-09
   - Auth
   - Seguridad
 * - CA-10
   - Enforcement reload
   - Integracion
