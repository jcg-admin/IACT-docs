8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_01 — actividad

 @startuml

 start

 :POST /api/users/{id}/functions/;

 if (JWT valido?) then (no)
   :401 INVALID_TOKEN; stop
 else (si)
 endif

 if (Tiene assign_functions?) then (no)
   :403 FORBIDDEN;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (Payload valido?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 if (User existe?) then (no)
   :404 USER_NOT_FOUND; stop
 else (si)
 endif

 if (User state válido?) then (no)
   :400 INVALID_USER_STATE; stop
 else (si)
 endif

 if (P-11 viola — auto-asignacion?) then (si)
   :400 SELF_ASSIGN_FORBIDDEN;
   :Audit ALERTA;
   stop
 else (no)
 endif

 if (Todas las funciones existen y ACTIVE?) then (no)
   :400 FUNCTION_NOT_FOUND/INACTIVE; stop
 else (si)
 endif

 :Filtrar funciones ya asignadas;

 if (Quedan funciones nuevas?) then (no — FA-01)
   :Audit FUNCTIONS_ASSIGN_NOOP;
   :200 OK informativo;
   stop
 else (si)
 endif

 :Construir effective_function_set
  (actuales + nuevas);
 :Evaluar SeparationRules ACTIVE contra set;

 if (Separacion violada?) then (si — EX-08)
   :409 SEPARATION_VIOLATION
    + rule_id + conflict_pair;
   :Audit FUNCTIONS_ASSIGN_FAILED ALERTA;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :registrar Assignment (N filas);
   :registrar AuditEvent FUNCTIONS_ASSIGNED;
   if (politica notify?) then (si)
     :registrar InternalMessage;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :PermissionCache.invalidate(target.id)
  (post-COMMIT);
 :201 Created con assigned + skipped;
 :Frontend toast resumen;

 stop

 @enduml

