.. _uc-adm-03-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Agregar Function a AGR del sistema
===============================================================

.. uml::
 :caption: UC_ADM_03 — flujo de adicion de Function al AGR.

 @startuml

 start
 :Invoker emite POST
   /api/v1/admin/system-groups/{id}/functions/;
 :Servicio de Aplicacion verifica capability
   assign_functions_to_group (AGR-010);
 if (Capability presente?) then (no)
   :403 Forbidden;
   :Audit CAPABILITY_DENIED;
   stop
 endif

 :Verificar AccessGroup existe + is_system=True;
 if (No existe / no es sistema?) then (si)
   :403 usar UC_PERM_06 para AGRs custom;
   stop
 endif

 :Verificar Function existe + is_active=True;
 if (Function no encontrada / inactiva?) then (si)
   :400 funcion invalida;
   stop
 endif

 :Validar SoD precheck (BR-007):
   no debe violar ninguna regla SoD activa;
 if (Conflicto SoD?) then (si)
   :400 + detalle de regla violada;
   stop
 endif

 :BEGIN TRANSACTION;
 :INSERT FunctionGroupMembership;
 :Audit AGR_FUNCTION_ADDED
   (actor=invoker, group_id, function_codename);
 :COMMIT;

 :Invalidar PermissionCache para users con el AGR
   (post-COMMIT);
 :EvaluatorReloader.recalculate(group_id);
 if (Recalculate OK?) then (no)
   :Log + telemetria
   (degraded mode);
 endif

 :201 Created;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/requisitos/reglas-negocio/br-007-separacion-funciones-sod`.
 - :doc:`/arquitectura-tecnica/domain-model/function-group`.
 - :doc:`/arquitectura-tecnica/domain-model/access-group`.
