8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_04 — flujo

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "RevokeExcView" as Revokeexcview
 participant "AccessService" as Accessservice
 participant "PermCache" as Permcache
 participant "InternalMailbox" as Internalmailbox
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 Invoker -> Frontend: Selecciona permission + reason
 Frontend -> Revokeexcview: DELETE .../{permission_id}/

 Revokeexcview -> Revokeexcview: Validar JWT
 Revokeexcview -> Revokeexcview: Verificar revoke_exc
 alt Sin permiso
   Revokeexcview --> Frontend: 403
   Revokeexcview -> Auditlog: emit UNAUTHORIZED
 else
   Revokeexcview -> Accessservice: revoke_exc(perm_id, reason, invoker)

   Accessservice -> Repo: consultar ExceptionalPermission
   alt No existe / EXPIRED / REVOKED
     Accessservice --> Revokeexcview: error
     Revokeexcview --> Frontend: 404 / 400 / 200 NOOP
   else ACTIVE
     Accessservice -> Accessservice: validar P-11
     Accessservice -> Accessservice: validar reason
     group Transaccion atomica
       Accessservice -> Repo: actualizar state=REVOKED
       Accessservice -> Internalmailbox: send (HARD)
       alt Mailbox falla
         Internalmailbox --> Accessservice: MailboxFailure
         Accessservice --> Revokeexcview: error 500
       else Mailbox OK
         Accessservice -> Auditlog: emit\nEXCEPTIONAL_PERMISSION_REVOKED
       end
     end
     Accessservice -> Permcache: invalidate post-COMMIT
     Accessservice --> Revokeexcview: result
     Revokeexcview --> Frontend: 200 OK
   end
 end

 @enduml

