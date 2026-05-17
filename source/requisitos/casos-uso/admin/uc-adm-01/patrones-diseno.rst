.. _uc-adm-01-parte-10:

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
 * - **P-41** (nuevo)
   - Logical soft-delete
   - BR-009: INACTIVE no DELETE
 * - **P-42** (nuevo)
   - Enforcement reload
   - recarga sincrona tras cambio
 * - **P-43** (nuevo)
   - Disjoint-set validation
   - conjuntos group_a / group_b
     mutuamente excluyentes

10.2 P-42: Enforcement reload
==============================

**Problema**: si EnforcementEngine usa cache
de reglas de separacion, un cambio en BD no se aplica
hasta restart.

**Solucion**: tras cada escritura exitosa,
UC_ADM_01 notifica al EnforcementEngine para
recargar. Reload es sincrono (≤ 2 s) —
el 201 se emite despues.

**Trade-off**: latencia de write aumenta 2 s.
Aceptable por ser operacion de admin poco frecuente.

10.3 P-43: Disjoint-set validation
===================================

**Problema**: una regla de separacion mal definida con
funcion en ambos grupos bloquea a todos.

**Solucion**: Validator comprueba
``set(group_a) ∩ set(group_b) == ∅``
antes de persistir.

10.4 Trazabilidad
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
   - PASO desactivar (INACTIVE)
 * - P-42
   - PASO 6 reload
 * - P-43
   - PASO 3 validar
