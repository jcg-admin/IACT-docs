.. _uc-usr-06-parte-08-diagrama-actividad:

8.3 Diagrama de actividad
==========================

.. uml::

   @startuml

   start

   :Admin invoca\nPOST /users/{id}/unblock\n{reason};

   :AuthorizationGuard verifica\nfuncion unblock_users;

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

   if (User.state == INACTIVE?) then (si)
     :409 INVALID_STATE_TRANSITION\n(use UC_USR_03);
     stop
   else (no)
   endif

   if (target == actor?) then (si)
     :409 SELF_UNBLOCK_FORBIDDEN;
     stop
   else (no)
   endif

   if (User.state == ACTIVE?) then (si)
     :200 OK already_unblocked=true;
     stop
   else (no)
   endif

   partition "transaction.atomic" {
     :Lookup ultimo AuditEvent\nde bloqueo previo;

     if (block event existe?) then (no)
       :emit USER_STATE_INCONSISTENCY warning;
     else (si)
     endif

     :User.state = ACTIVE;
     :emit USER_UNBLOCKED\n{reason, original_block_event_id};

     if (alguna falla?) then (si)
       :rollback;
       :500 UNBLOCK_FAILED;
       stop
     else (no)
       :commit;
     endif
   }

   :200 OK\n{user_id, state, original_block_event_id};
   stop

   @enduml
