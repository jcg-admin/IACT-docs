.. _uc-usr-05-parte-08-diagrama-actividad:

8.3 Diagrama de actividad
==========================

.. uml::

   @startuml

   start

   :Admin invoca\nPOST /users/{id}/block\n{reason};

   :AuthorizationGuard verifica\nfuncion block_users;

   if (autorizado?) then (no)
     :403 PERMISSION_DENIED;
     :emit ACCESS_DENIED;
     stop
   else (si)
   endif

   :Cargar User por user_id;

   if (User existe?) then (no)
     :404 USER_NOT_FOUND;
     stop
   else (si)
   endif

   if (User.state == ELIMINATED?) then (si)
     :409 USER_ELIMINATED;
     stop
   else (no)
   endif

   if (target == actor?) then (si)
     :409 SELF_BLOCK_FORBIDDEN;
     stop
   else (no)
   endif

   if (User.state == BLOCKED?) then (si)
     :200 OK already_blocked=true;
     :sin AuditEvent;
     stop
   else (no)
   endif

   partition "transaction.atomic" {
     :User.state = BLOCKED;
     :bulk close Sessions ACTIVE\n→ CLOSED USER_BLOCKED;
     :bulk insert BlacklistedToken\npor cada refresh token vivo;
     :AuditService.emit(USER_BLOCKED,\n{reason, counts});

     if (alguna falla?) then (si)
       :rollback completo;
       :500 BLOCK_FAILED;
       stop
     else (no)
       :commit;
     endif
   }

   :200 OK\n{user_id, state, counts};
   stop

   @enduml
