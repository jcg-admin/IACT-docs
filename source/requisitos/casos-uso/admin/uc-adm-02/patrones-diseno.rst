.. _uc-adm-02-parte-10:

==========================
Parte 10 — Patrones
==========================

10.1 Patrones aplicados
=======================

.. list-table::
 :widths: 18 32 50

 * - Patron
   - Nombre
   - Aplicacion
 * - **P-15**
   - RBAC granular
   - solo AGR-010 accede
 * - **P-39**
   - Audit reforzado
   - toda escritura auditada
 * - **P-41**
   - Logical soft-deactivate
   - BR-009: is_active=False no DELETE
 * - **P-44** (nuevo)
   - Immutable codename
   - codename no cambia tras creacion;
     evita referencias rotas en
     asignaciones existentes

10.2 P-44: Immutable codename
==============================

**Problema**: si el codename cambia, todas
las referencias en grupos, asignaciones
y permisos efectivos quedan rotas.

**Solucion**: codename es inmutable tras
creacion. Para renombrar, se crea una nueva
funcion y se desactiva la antigua.
Solo description, scope y is_active son
actualizables.

10.3 Trazabilidad
=================

.. list-table::
 :widths: 30 70

 * - Origen
   - Implementado en
 * - P-15
   - PASO 2 RBAC check
 * - P-39
   - PASO 5 audit
 * - P-41
   - desactivar (is_active=False)
 * - P-44
   - Validator impide cambio codename
