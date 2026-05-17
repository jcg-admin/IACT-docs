8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_08 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "GrantExcView" as Grantexcview
 participant "AccessService" as Accessservice
 participant "SeparationRuleValidator" as Sodvalidator
 participant "PermissionCache" as Permissioncache
 participant "InternalMailbox" as Internalmailbox
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Form con functions, expires_at,\n  justification, ticket_ref
 Frontend -> Grantexcview: POST /api/users/{id}/\n  exceptional-permissions/

 Grantexcview -> Grantexcview: Validar JWT
 Grantexcview -> Grantexcview: Verificar grant_exceptional_permission
 alt Sin la funcion
   Grantexcview --> Frontend: 403
   Grantexcview -> Auditlog: emit UNAUTHORIZED ALERTA ALTA
 else
   Grantexcview -> Accessservice: grant_exceptional(target_id,\n  function_ids, expires_at,\n  justification, ticket_ref,\n  invoker)

   Accessservice -> Repo: consultar User para actualizar
   alt User invalido
     Accessservice --> Grantexcview: error
     Grantexcview --> Frontend: 404 / 400
   else OK
     Accessservice -> Accessservice: validar P-11 anti-self
     Accessservice -> Accessservice: validar payload\n  (justification, expires_at)
     Accessservice -> Repo: consultar Function WHERE id IN ...
     alt Funcion invalida
       Accessservice --> Grantexcview: error
       Grantexcview --> Frontend: 400
     else OK
       Accessservice -> Repo: consultar ExceptionalPermission\n  ACTIVE existentes
       Accessservice -> Accessservice: filtrar idempotencia
       Accessservice -> Sodvalidator: validate(effective_post_grant,\n  rules)
       alt separacion viola
         Sodvalidator --> Accessservice: SeparationRuleViolation
         Accessservice -> Auditlog: emit GRANT_FAILED ALERTA
         Grantexcview --> Frontend: 409
       else separacion OK
         group Transaccion atomica
           Accessservice -> Repo: registrar ExceptionalPermission\n  (N filas)
           Accessservice -> Internalmailbox: send obligatorio
           alt Mailbox falla
             Internalmailbox --> Accessservice: MailboxFailure
             Accessservice -> Auditlog: emit GRANT_FAILED
             Grantexcview --> Frontend: 500 (rollback)
           else Mailbox OK
             Accessservice -> Auditlog: emit\n  EXCEPTIONAL_PERMISSION_GRANTED
           end
         end
         Accessservice -> Permissioncache: invalidate(target.id) post-COMMIT
         Accessservice --> Grantexcview: result
         Grantexcview --> Frontend: 201 Created
       end
     end
   end
 end

 @enduml

