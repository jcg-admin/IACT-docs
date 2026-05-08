.. _uc-usr-07-parte-08-diagrama-secuencia:

8.2 Diagrama de secuencia
==========================

.. uml::

   @startuml

   actor "User" as User
   participant "UpdateOwnProfileEndpoint" as Endpoint
   participant "AuthorizationGuard" as Guard
   participant "User" as UserDM
   participant "EmailValidator" as EmailVal
   participant "UpdateOwnProfileCommand" as Cmd
   participant "AuditService" as Audit

   User -> Endpoint : PATCH /users/me\n{full_name?, email?}
   activate Endpoint

   Endpoint -> Guard : check(actor, 'edit_own_profile')
   Guard --> Endpoint : authorized

   Endpoint -> Endpoint : validate_no_forbidden_fields(payload)
   note right
     EDITABLE_FIELDS_SELF =
     {'full_name', 'email'}
     Otros campos → 400 FORBIDDEN_FIELD
   end note

   Endpoint -> Cmd : execute(actor_id, patch)
   activate Cmd

   Cmd -> UserDM : select_for_update(jwt.user_id)
   UserDM --> Cmd : User instance

   Cmd -> Cmd : detect diff vs current values

   alt no diff
     Cmd --> Endpoint : no_changes=true
   else has diff
     opt 'email' in fields_changed
       Cmd -> EmailVal : validate_format(email)
       Cmd -> EmailVal : validate_unique(email, exclude=user_id)
       EmailVal --> Cmd : OK or raise
     end

     Cmd -> UserDM : update(fields_changed)
     Cmd -> Audit : emit('PROFILE_UPDATED',\n{fields_changed: [...]})\nNO PII en payload
     Audit --> Cmd : event_id
     Cmd --> Endpoint : UpdateResult
   end

   deactivate Cmd

   Endpoint --> User : 200 OK\n{user_id, full_name, email, updated_at}
   deactivate Endpoint

   @enduml
