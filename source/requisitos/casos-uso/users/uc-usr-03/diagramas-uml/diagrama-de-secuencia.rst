8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_USR_03 — flujo principal

 @startuml

 actor Admin as Admin
 participant "Frontend" as Frontend
 participant "ModifyUserView" as Modifyuserview
 participant "UserService" as Userservice
 participant "SessionService" as Sessionservice
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 Admin -> Frontend: Edita campos del User
 Frontend -> Modifyuserview: PATCH /api/users/{id}/

 Modifyuserview -> Modifyuserview: Validar JWT (CNST-009)
 Modifyuserview -> Modifyuserview: Verificar modify_users (AGR-006)
 alt Sin permiso
   Modifyuserview --> Frontend: 403 FORBIDDEN
   Modifyuserview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Modifyuserview -> Userservice: modify_user(id, patch, admin)

   Userservice -> Repo: consultar User para actualizar WHERE id=?
   alt User no existe
     Userservice --> Modifyuserview: UserNotFound
     Modifyuserview --> Frontend: 404
   else User existe
     Userservice -> Userservice: validar transicion de state
     alt user_id == admin.id y patch.state
       Userservice --> Modifyuserview: SelfStateChange
       Modifyuserview --> Frontend: 400 SELF_STATE_CHANGE_FORBIDDEN
     else OK
       opt patch.email cambia
         Userservice -> Repo: consultar email
         alt email duplicado
           Userservice --> Modifyuserview: EmailExists
           Modifyuserview --> Frontend: 409 EMAIL_EXISTS
         end
       end

       group Transaccion atomica
         Userservice -> Repo: actualizar User SET (campos),\n  last_modified_at=marca_tiempo_actual,\n  last_modified_by_admin_id=admin.id
         opt state -> BLOCKED
           Userservice -> Sessionservice: close_all_active_for_user(user)
           Sessionservice -> Repo: actualizar Session\n  state='CLOSED',\n  close_reason='ADMIN_BLOCKED'
           Sessionservice -> Repo: registrar BlacklistedToken (N)
           Sessionservice --> Userservice: closed_count
         end
         opt state cambio Y notify activo
           Userservice -> Repo: registrar InternalMessage
         end
         Userservice -> Auditlog: emit USER_MODIFIED\n  {fields_changed,\n   state_transition?,\n   sessions_closed_count}
       end

       Userservice --> Modifyuserview: result
       Modifyuserview --> Frontend: 200 OK con fields_changed
       Frontend --> Admin: Toast con resumen
     end
   end
 end

 @enduml

