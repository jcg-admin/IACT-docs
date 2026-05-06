.. _uc-adm-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **AGR-010** ``system_admin`` — unico actor autorizado
- **SoDRuleRepo**
- **EnforcementEngine** (consume reglas activas)

2.2 Precondiciones
==================

Auth + RBAC verificado. Actor tiene AGR-010 asignado.

2.3 Postcondiciones
===================

- SoDRule creada / actualizada / desactivada.
- Audit ``SOD_RULE_CREATED`` / ``SOD_RULE_UPDATED`` /
  ``SOD_RULE_DISABLED`` emitido.
- EnforcementEngine recarga reglas activas.

2.4 Datos de entrada
====================

::

   POST /api/admin/sod-rules/
   body: {
     name, group_a: [function_codenames],
     group_b: [function_codenames],
     rationale
   }

   PATCH /api/admin/sod-rules/{id}/
   body: { name?, group_a?, group_b?, rationale? }

   POST /api/admin/sod-rules/{id}/disable/

2.5 Datos de salida
===================

SoDRule completa con estado y version.
