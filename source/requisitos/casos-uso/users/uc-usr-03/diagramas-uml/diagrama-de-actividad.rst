8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_USR_03 — actividad

 @startuml

 start

 :Admin edita campos del User;
 :PATCH /api/users/{id}/;

 if (JWT valido?) then (no)
   :401 INVALID_TOKEN;
   stop
 else (si)
 endif

 if (Tiene modify_users?) then (no)
   :403 FORBIDDEN;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404 USER_NOT_FOUND;
   stop
 else (si)
 endif

 if (Datos validos?) then (no)
   :400 VALIDATION_ERROR;
   stop
 else (si)
 endif

 if (patch incluye state?) then (si)
   if (user_id == admin.id?) then (si)
     :400 SELF_STATE_CHANGE_FORBIDDEN;
     :Audit USER_MODIFY_FAILED ALERTA;
     stop
   else (no)
   endif
   if (transicion permitida?) then (no)
     :400 INVALID_STATE_TRANSITION;
   stop
   else (si)
   endif
 else (no)
 endif

 if (patch incluye email cambiado?) then (si)
   if (email duplicado?) then (si)
     :409 EMAIL_EXISTS;
   stop
   else (no)
   endif
 else (no)
 endif

 partition "Transaccion atomica" {
   :actualizar User parcial\n+ last_modified_*;
   if (state -> BLOCKED?) then (si)
     :actualizar Sessions ACTIVE -> CLOSED;
     :registrar BlacklistedToken (N);
   else (no)
   endif
   if (state cambio Y notify activo?) then (si)
     :registrar InternalMessage;
   else (no)
   endif
   :registrar AuditEvent USER_MODIFIED (CNST-025);
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500 / 503;
   stop
 else (si)
 endif

 :200 OK con fields_changed;
 :Frontend toast resumen;

 stop

 @enduml

