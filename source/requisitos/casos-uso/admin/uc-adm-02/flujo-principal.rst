.. _uc-adm-02-parte-03:

==========================
Parte 3 — Flujo principal
==========================

3.1 Crear funcion atomica
=========================

PASO 1 — POST /api/admin/functions/.
PASO 2 — JWT + verificar AGR-010.
PASO 3 — Validar:

- codename unico (snake_case, sin espacios).
- module valido (MOD_Auth, MOD_User, MOD_Access, etc.).
- scope definido.

PASO 4 — INSERT Function (is_active=True).
PASO 5 — Audit FUNCTION_CREATED (alta criticidad).
PASO 6 — PermissionsEngine.reload_catalog().
PASO 7 — 201.

3.2 Actualizar funcion
======================

PATCH con validacion de codename unico si cambia.
Audit FUNCTION_UPDATED. Reload catalog.
Nota: codename es inmutable tras creacion (P-44).

3.3 Desactivar funcion
======================

Funcion pasa a is_active=False (BR-009 — no DELETE).
Asignaciones historicas preservadas. Nuevas
asignaciones de la funcion bloqueadas.
Audit FUNCTION_DEACTIVATED.

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
   - Validar codename
   - Validator
   - 029
 * - 4
   - INSERT Function
   - Repo
   - —
 * - 5
   - Audit
   - AuditService
   - 025
 * - 6
   - Reload catalog
   - PermissionsEngine
   - —
 * - 7
   - 201
   - View
   - —
