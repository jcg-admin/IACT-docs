.. _uc-adm-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **AGR-010** ``system_admin`` — unico actor autorizado
- **SeparationRuleRepo**
- **EnforcementEngine** (consume reglas activas)

2.2 Precondiciones
==================

Auth + RBAC verificado. Actor tiene AGR-010 asignado.

2.3 Postcondiciones
===================

- SeparationRule creada / actualizada / desactivada.
- Audit ``SEPARATION_RULE_CREATED`` / ``SEPARATION_RULE_UPDATED`` /
  ``SEPARATION_RULE_DISABLED`` emitido.
- EnforcementEngine recarga reglas activas.

2.4 Datos de entrada
====================

::

   POST /api/admin/separation-rules/
   body: {
     name, group_a: [function_codenames],
     group_b: [function_codenames],
     rationale
   }

   PATCH /api/admin/separation-rules/{id}/
   body: { name?, group_a?, group_b?, rationale? }

   POST /api/admin/separation-rules/{id}/disable/

2.5 Datos de salida
===================

SeparationRule completa con estado y version.
