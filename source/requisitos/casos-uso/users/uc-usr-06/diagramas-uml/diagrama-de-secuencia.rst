.. _uc-usr-06-parte-08-diagrama-secuencia:

8.2 Diagrama de secuencia
==========================

.. uml::

   @startuml

   actor "Admin" as Admin
   participant "UnblockUserEndpoint" as Endpoint
   participant "AuthorizationGuard" as Guard
   participant "User" as User
   participant "UnblockUserCommand" as Cmd
   participant "AuditEvent" as Audit

   Admin -> Endpoint : POST /users/{id}/unblock\n{reason}
   activate Endpoint

   Endpoint -> Guard : check(actor, 'unblock_users')
   Guard --> Endpoint : authorized

   Endpoint -> Cmd : execute(actor_id, target_id, reason)
   activate Cmd

   Cmd -> User : select_for_update(user_id)
   User --> Cmd : User instance

   alt User.state == 'ACTIVE'
     Cmd --> Endpoint : already_unblocked=true
   else User.state == 'ELIMINATED'
     Cmd --> Endpoint : raise UserEliminatedError
   else User.state == 'INACTIVE'
     Cmd --> Endpoint : raise InvalidStateTransitionError
   else target == actor
     Cmd --> Endpoint : raise SelfUnblockForbiddenError
   else User.state == 'BLOCKED'
     Cmd -> Audit : query last block event\n(USER_BLOCKED|ACCOUNT_LOCKED|...)
     Audit --> Cmd : block_event or null

     opt block_event is null
       Cmd -> Audit : emit USER_STATE_INCONSISTENCY
     end

     Cmd -> User : state = 'ACTIVE'
     Cmd -> Audit : emit USER_UNBLOCKED\n{reason, original_block_event_id, ...}
     Audit --> Cmd : event_id
     Cmd --> Endpoint : UnblockResult
   end

   deactivate Cmd

   Endpoint --> Admin : 200 OK\n{user_id, state, original_block_event_id}
   deactivate Endpoint

   @enduml
