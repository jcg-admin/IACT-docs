.. _uc-adm-03-parte-10:

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
 * - **P-45** (nuevo)
   - System-group guard
   - is_system=True verificado;
     grupos custom usan UC_PERM_06
 * - **P-46** (nuevo)
   - Impact preview
   - GET /impact/ antes de confirmar;
     operador evalua antes de cambiar
 * - **P-30**
   - SoD pre-check
   - verificar SoD al agregar funcion
     al grupo

10.2 P-45: System-group guard
==============================

**Problema**: UC_PERM_06 permite que
administradores funcionales modifiquen
grupos custom. Si accedieran a AGR de sistema
podrian escalar privilegios.

**Solucion**: guard verifica is_system=True.
Si False, endpoint retorna 403 con mensaje
"usar UC_PERM_06 para grupos custom".

10.3 P-46: Impact preview
==========================

**Problema**: modificar composicion de AGR
de sistema afecta a todos sus usuarios.
Sin vista previa, el administrador desconoce
el alcance del cambio.

**Solucion**: GET /impact/ calcula y muestra
numero de usuarios afectados y preview del
effective_set resultante, sin persistir.

10.4 Trazabilidad
=================

.. list-table::
 :widths: 30 70

 * - Origen
   - Implementado en
 * - P-15
   - PASO 2 RBAC check
 * - P-39
   - PASO 6 audit
 * - P-45
   - PASO 3 is_system guard
 * - P-46
   - GET /impact/ endpoint
 * - P-30
   - PASO 4 SoD pre-check
