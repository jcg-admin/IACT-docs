.. _uc-adm-02-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

CA-01: Crear funcion con codename unico → 201.
CA-02: Codename duplicado → 409.
CA-03: Codename con formato invalido → 400.
CA-04: Module invalido → 400.
CA-05: Update description → funcion actualizada.
CA-06: Desactivar funcion → is_active=False;
nuevas asignaciones bloqueadas.
CA-07: Asignaciones historicas preservadas
tras desactivacion.
CA-08: Audit completo (CREATED/UPDATED/DEACTIVATED).
CA-09: Sin AGR-010 → 403.
CA-10: PermissionsEngine recarga tras creacion.
CA-11: Listado filtrando por module y state.

Resumen
=======

.. list-table::
 :widths: 12 50 38

 * - ID
   - Concepto
   - Tipo
 * - CA-01..04
   - CRUD + validation
   - Funcional
 * - CA-05
   - Update parcial
   - Funcional
 * - CA-06..07
   - Deactivate lifecycle
   - Robustez
 * - CA-08
   - Audit
   - Compliance
 * - CA-09
   - Auth
   - Seguridad
 * - CA-10
   - Catalog reload
   - Integracion
 * - CA-11
   - Listado
   - Funcional
