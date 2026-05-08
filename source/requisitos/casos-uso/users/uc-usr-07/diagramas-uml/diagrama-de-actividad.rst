.. _uc-usr-07-parte-08-diagrama-actividad:

8.3 Diagrama de actividad
==========================

.. uml::

   @startuml

   start

   :User invoca\nPATCH /users/me\n{full_name?, email?};

   :AuthorizationGuard verifica\nfuncion edit_own_profile;

   if (autorizado?) then (no)
     :403 PERMISSION_DENIED;
     stop
   else (si)
   endif

   if (payload contiene\ncampo prohibido?) then (si)
     :400 FORBIDDEN_FIELD;
     stop
   else (no)
   endif

   if (payload vacio?) then (si)
     :400 EMPTY_PAYLOAD;
     stop
   else (no)
   endif

   :Cargar User por jwt.user_id;

   if (User.state == ACTIVE?) then (no)
     :409 INVALID_STATE;
     stop
   else (si)
   endif

   :Detectar diff vs estado actual;

   if (no hay diff?) then (si)
     :200 OK no_changes=true;
     stop
   else (no)
   endif

   if (email modificado?) then (si)
     :Validar formato email;
     if (formato valido?) then (no)
       :400 INVALID_EMAIL_FORMAT;
       stop
     else (si)
     endif
     :Validar unicidad email;
     if (email unico?) then (no)
       :409 EMAIL_ALREADY_TAKEN;
       stop
     else (si)
     endif
   else (no)
   endif

   partition "transaction.atomic" {
     :User UPDATE\ncampos modificados;
     :emit PROFILE_UPDATED\n{fields_changed: [...]}\nSIN valores PII;

     if (alguna falla?) then (si)
       :rollback;
       :500 PROFILE_UPDATE_FAILED;
       stop
     else (no)
       :commit;
     endif
   }

   :200 OK\n{user_id, full_name, email, updated_at};
   stop

   @enduml
