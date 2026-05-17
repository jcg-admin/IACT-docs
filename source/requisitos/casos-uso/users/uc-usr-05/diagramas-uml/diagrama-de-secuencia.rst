.. _uc-usr-05-parte-08-diagrama-secuencia:

8.2 Diagrama de secuencia
==========================

.. uml::

   @startuml

   actor "Admin" as Admin
   participant "BlockUserEndpoint" as Endpoint
   participant "AuthorizationGuard" as Guard
   participant "User" as User
   participant "BlockUserCommand" as Cmd
   participant "Session" as Session
   participant "BlacklistedToken" as Token
   participant "AuditService" as Audit

   Admin -> Endpoint : POST /users/{id}/block\n{reason}
   activate Endpoint

   Endpoint -> Guard : check(actor, 'block_users')
   Guard --> Endpoint : authorized

   Endpoint -> Cmd : execute(actor_id, target_id, reason)
   activate Cmd

   Cmd -> User : select_for_update(user_id)
   User --> Cmd : User instance

   alt User.state == 'BLOCKED'
     Cmd --> Endpoint : already_blocked=true
   else User.state == 'ELIMINATED'
     Cmd --> Endpoint : raise UserEliminatedError
   else target == actor
     Cmd --> Endpoint : raise SelfBlockForbiddenError
   else valid transition (ACTIVE/INACTIVE)
     Cmd -> User : state = 'BLOCKED'
     Cmd -> Session : bulk update state='CLOSED'\nclose_reason='USER_BLOCKED'
     Session --> Cmd : sessions_closed_count
     Cmd -> Token : bulk insert\nblacklisted refresh tokens
     Token --> Cmd : tokens_blacklisted_count
     Cmd -> Audit : emit('USER_BLOCKED', payload)
     Audit --> Cmd : event_id
     Cmd --> Endpoint : BlockResult
   end

   deactivate Cmd

   Endpoint --> Admin : 200 OK\n{user_id, state, counts}
   deactivate Endpoint

   note over User, Audit
     Toda la seccion entre select_for_update y emit
     ocurre dentro de transaction.atomic.
     Fallo en cualquier paso → rollback completo.
   end note

   @enduml
