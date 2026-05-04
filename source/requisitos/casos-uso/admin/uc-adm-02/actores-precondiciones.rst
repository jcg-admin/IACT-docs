.. _uc-adm-02-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **AGR-009** ``admin_sistema`` — unico actor autorizado
- **FunctionRepo** (catalogo de funciones)
- **PermissionsEngine** (consume catalogo activo)

2.2 Precondiciones
==================

Auth + RBAC verificado. Actor tiene AGR-009 asignado.

2.3 Postcondiciones
===================

- Function creada / actualizada / desactivada.
- Audit ``FUNCTION_CREATED`` / ``FUNCTION_UPDATED`` /
  ``FUNCTION_DEACTIVATED`` emitido.
- PermissionsEngine recarga catalogo de funciones activas.

2.4 Datos de entrada
====================

::

   POST /api/admin/functions/
   body: {
     codename, description,
     module, scope, is_active: true
   }

   PATCH /api/admin/functions/{id}/
   body: { description?, scope?, is_active? }

2.5 Datos de salida
===================

Function completa con estado, modulo y version.
