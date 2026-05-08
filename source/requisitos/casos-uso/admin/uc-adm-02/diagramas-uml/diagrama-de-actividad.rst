.. _uc-adm-02-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Crear Function
===========================================

.. uml::
 :caption: UC_ADM_02 — flujo de creacion de Function atomica.

 @startuml

 start
 :Invoker emite POST /api/v1/admin/functions/;
 :Servicio de Aplicacion verifica capability
   manage_function_catalog;
 if (Capability presente?) then (no)
   :403 Forbidden;
   :Audit CAPABILITY_DENIED;
   stop
 endif

 :Validar codename snake_case (STD-008);
 if (Formato invalido?) then (si)
   :400 codename invalido;
   stop
 endif

 :Validar codename unico
   (FunctionRepo);
 if (Codename duplicado?) then (si)
   :409 Conflict;
   stop
 endif

 :Validar module pertenece al catalogo
   (AUTH/USR/ACC/PIP/RPT/ALR/AUD/LOG/ADM);
 if (Module invalido?) then (si)
   :422 module invalido;
   stop
 endif

 :BEGIN TRANSACTION;
 :INSERT Function (is_active=True, is_critical=False);
 :Audit FUNCTION_CREATED
   (actor=invoker, snapshot);
 :COMMIT;

 :Invalidar PermissionCache (post-COMMIT);
 :EvaluatorReloader.reload_catalog()
   (hot reload);
 if (Reload OK?) then (no)
   :Log + telemetria
   (degraded mode);
 endif

 :201 Created con Function;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/normativa/estandares/std-008-naming-identificadores`.
 - :doc:`/arquitectura-tecnica/domain-model/function`.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`.
 - :doc:`/backend/adr-back-010-function-is-critical-governance`
   (is_critical via migration, no UC).
