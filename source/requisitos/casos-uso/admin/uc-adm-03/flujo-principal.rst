.. _uc-adm-03-parte-03:

==========================
Parte 3 — Flujo principal
==========================

3.1 Agregar funcion a AGR de sistema
=====================================

PASO 1 — POST /api/admin/system-groups/{id}/functions/.
PASO 2 — JWT + verificar AGR-009.
PASO 3 — Verificar que FunctionGroup.is_system=True.
PASO 4 — Validar:

- Funcion existe en catalogo activo (UC_ADM_02).
- Funcion no genera conflicto SoD con otras
  funciones del grupo (UC_ADM_01).
- Funcion no ya asignada al grupo.

PASO 5 — INSERT GroupFunction.
PASO 6 — Audit AGR_FUNCTION_ADDED (alta criticidad).
PASO 7 — PermissionsEngine.recalculate(agr_id).
PASO 8 — 201.

3.2 Remover funcion de AGR de sistema
======================================

DELETE con verificacion analoga.
Audit AGR_FUNCTION_REMOVED. Recalculo effective_set.

3.3 Ver composicion e impacto
==============================

GET composicion: lista de funciones del AGR.
GET impact: numero de usuarios afectados + preview
de effective_set resultante (informativo, sin cambio).

3.4 Resumen
===========

.. list-table::
 :widths: 8 50 22 20

 * - Paso
   - Accion
   - Componente
   - CNST
 * - 1-2
   - POST + JWT + RBAC
   - Endpoint
   - 009
 * - 3
   - Verificar is_system
   - Guard
   - 029
 * - 4
   - Validar SoD + exist
   - Validator
   - 030
 * - 5
   - INSERT GroupFunction
   - Repo
   - —
 * - 6
   - Audit
   - AuditService
   - 025
 * - 7
   - Recalcular
   - PermissionsEngine
   - —
 * - 8
   - 201
   - View
   - —
