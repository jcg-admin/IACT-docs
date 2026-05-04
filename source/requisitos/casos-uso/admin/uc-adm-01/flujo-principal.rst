.. _uc-adm-01-parte-03:

==========================
Parte 3 — Flujo principal
==========================

3.1 Crear regla SoD
===================

PASO 1 — POST /api/admin/sod-rules/.
PASO 2 — JWT + verificar AGR-009.
PASO 3 — Validar:

- group_a y group_b no vacios.
- Ninguna funcion en ambos grupos (conjuntos disjuntos).
- Funciones existen en catalogo activo (UC_ADM_02).
- Nombre unico.

PASO 4 — INSERT SoDRule (estado=ACTIVE).
PASO 5 — Audit SOD_RULE_CREATED (alta criticidad).
PASO 6 — EnforcementEngine.reload().
PASO 7 — 201.

3.2 Actualizar regla
====================

CRUD estandar con validacion de conjuntos disjuntos.
Audit por cada cambio. EnforcementEngine.reload().

3.3 Desactivar regla
====================

Toggle ACTIVE → INACTIVE. Regla permanece en BD
(no DELETE — BR-009 bajas logicas). Enforcement
deja de aplicarla. Audit SOD_RULE_DISABLED.

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
   - Validar conjuntos
   - Validator
   - 030
 * - 4
   - INSERT SoDRule
   - Repo
   - —
 * - 5
   - Audit
   - AuditService
   - 025
 * - 6
   - Reload enforcement
   - EnforcementEngine
   - —
 * - 7
   - 201
   - View
   - —
