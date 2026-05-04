8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_USR_04 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "DeleteUserView" as Deleteuserview
 participant "UserService" as Userservice
 participant "SessionService" as Sessionservice
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 Invoker -> Frontend: Click "Eliminar" en User X
 Frontend -> Frontend: Modal robusto + doble confirmacion
 Invoker -> Frontend: Escribe "ELIMINAR" + Confirmar
 Frontend -> Deleteuserview: DELETE /api/users/{X}/

 Deleteuserview -> Deleteuserview: Validar JWT (CNST-009)
 Deleteuserview -> Deleteuserview: Verificar funcion deactivate_users
 alt Sin la funcion
   Deleteuserview --> Frontend: 403 FORBIDDEN
   Deleteuserview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con la funcion
   Deleteuserview -> Userservice: eliminate_user(X, invoker)

   Userservice -> Repo: consultar User para actualizar WHERE id=X
   alt User no existe
     Userservice --> Deleteuserview: UserNotFound
     Deleteuserview --> Frontend: 404
   else User existe
     alt User.state == ELIMINATED
       opt politica strict
         Userservice --> Deleteuserview: AlreadyEliminated
         Deleteuserview --> Frontend: 409
       end
       opt politica idempotente (default)
         Userservice -> Auditlog: emit USER_ELIMINATE_NOOP
         Userservice --> Deleteuserview: noop_result
         Deleteuserview --> Frontend: 200 OK informativo
       end
     else state != ELIMINATED
       alt invoker.id == X
         Userservice --> Deleteuserview: SelfElimination
         Deleteuserview --> Frontend: 400
         Deleteuserview -> Auditlog: emit USER_ELIMINATE_FAILED ALERTA
       else
         group Transaccion atomica
           Userservice -> Repo: actualizar User\n  state='ELIMINATED',\n  eliminated_at=marca_tiempo_actual,\n  eliminated_by=invoker.id
           Userservice -> Repo: actualizar Assignment\n  state='REVOKED'\n  WHERE user=X AND state='ACTIVE'
           Userservice -> Sessionservice: close_all_active(X, invoker,\n  reason='USER_ELIMINATED')
           Sessionservice -> Repo: actualizar Session... CLOSED
           Sessionservice -> Repo: registrar BlacklistedToken (N)
           Sessionservice --> Userservice: closed_count
           opt notify activo
             Userservice -> Repo: registrar InternalMessage
             alt mailbox falla
               Userservice -> Userservice: mailbox_failed=true (no abort)
             end
           end
           Userservice -> Auditlog: emit USER_ELIMINATED\n  {target, prior_state,\n   sessions_closed_count,\n   assignments_revoked_count,\n   user_notified, mailbox_failed}
         end

         Userservice --> Deleteuserview: result
         Deleteuserview --> Frontend: 200 OK con resumen
         Frontend --> Invoker: Toast con resumen + refresh lista
       end
     end
   end
 end

 @enduml

