8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_04 — actividad

 @startuml

 start

 :POST /api/users/{id}/access-groups/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene assign_function_groups?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 if (User state OK?) then (no)
   :400 INVALID_USER_STATE; stop
 else (si)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_ASSIGN_FORBIDDEN;
   :Audit ALERTA;
   stop
 else (no)
 endif

 if (AGR existe + ACTIVE?) then (no)
   :400 ACCESS_GROUP_NOT_FOUND/INACTIVE; stop
 else (si)
 endif

 if (Ya asignado?) then (si)
   :Audit AGR_ASSIGN_NOOP;
   :200 OK informativo;
   stop
 else (no)
 endif

 :Expandir funciones del AGR;
 :Construir effective_post_assign
  = current ∪ agr_functions;
 :Evaluar SoDRules;

 if (SoD viola?) then (si)
   :409 SOD_VIOLATION;
   :Audit AGR_ASSIGN_FAILED;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :registrar Assignment (target=AGR);
   :registrar AuditEvent AGR_ASSIGNED;
   if (notify activo?) then (si)
     :registrar InternalMessage;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :PermissionCache.invalidate (post-COMMIT);
 :201 Created con resumen;

 stop

 @enduml

