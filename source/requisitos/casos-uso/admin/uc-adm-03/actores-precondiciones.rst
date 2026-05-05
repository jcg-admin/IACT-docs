.. _uc-adm-03-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **AGR-009** ``admin_sistema`` — unico actor autorizado
- **FunctionGroupRepo** (AGR de sistema)
- **PermissionsEngine** (recalcula effective_set)

2.2 Precondiciones
==================

Auth + RBAC verificado. Actor tiene AGR-009 asignado.
FunctionGroup objetivo existe y tiene is_system=True.

2.3 Postcondiciones
===================

- Composicion del AGR de sistema actualizada.
- Audit ``AGR_FUNCTION_ADDED`` / ``AGR_FUNCTION_REMOVED`` emitido.
- PermissionsEngine recalcula effective_set de
  todos los usuarios que tienen el AGR asignado.

2.4 Datos de entrada
====================

::

   POST /api/admin/system-groups/{agr_id}/functions/
   body: { function_codename }

   DELETE /api/admin/system-groups/{agr_id}/functions/{codename}/

   GET /api/admin/system-groups/{agr_id}/
   GET /api/admin/system-groups/{agr_id}/impact/

2.5 Datos de salida
===================

FunctionGroup actualizado con lista de funciones.
Vista de impacto: numero de usuarios afectados.
