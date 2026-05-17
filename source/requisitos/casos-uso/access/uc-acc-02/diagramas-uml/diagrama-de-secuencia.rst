8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_02 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "RevokeFunctionsView" as Revokefunctionsview
 participant "AccessService" as Accessservice
 participant "PermissionCache" as Permissioncache
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Selecciona funciones a revocar
 Frontend -> Frontend: Modal robusto + revoke_reason
 I -> Frontend: Confirmar
 Frontend -> Revokefunctionsview: DELETE /api/users/{id}/functions/

 Revokefunctionsview -> Revokefunctionsview: Validar JWT (CNST-009)
 Revokefunctionsview -> Revokefunctionsview: Verificar revoke_functions
 alt Sin la funcion
   Revokefunctionsview --> Frontend: 403 FORBIDDEN
   Revokefunctionsview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con la funcion
   Revokefunctionsview -> Accessservice: revoke(target_id, function_ids,\n  reason, invoker)

   Accessservice -> Repo: consultar User para actualizar
   alt No existe / ELIMINATED
     Accessservice --> Revokefunctionsview: error
     Revokefunctionsview --> Frontend: 404 / 400
   else
     Accessservice -> Accessservice: validar P-11 anti-self-revoke
     Accessservice -> Repo: consultar Assignments ACTIVE\n  WHERE user=target\n  AND function IN (...)
     Repo --> Accessservice: matched_assignments
     Accessservice -> Accessservice: separar to_revoke vs skipped
     alt to_revoke vacio (FA-01)
       Accessservice -> Auditlog: emit FUNCTIONS_REVOKE_NOOP
       Accessservice --> Revokefunctionsview: noop_result
       Revokefunctionsview --> Frontend: 200 OK informativo
     else hay revocaciones
       Accessservice -> Repo: COUNT current_active\n  - to_revoke (post-revoke set)
       Accessservice -> Accessservice: calcular warnings\n  (no_functions, critical, last_holder)
       alt strict + last_holder violado
         Accessservice -> Auditlog: emit FUNCTIONS_REVOKE_FAILED
         Accessservice --> Revokefunctionsview: LastHolderProtection
         Revokefunctionsview --> Frontend: 409
       else procede
         group Transaccion atomica
           Accessservice -> Repo: actualizar Assignment\n  state='REVOKED', revoked_at,\n  revoked_by_admin_id, revoke_reason\n  WHERE id IN (...)
           Accessservice -> Auditlog: emit FUNCTIONS_REVOKED
           opt notify
             Accessservice -> Repo: registrar InternalMessage
           end
         end
         Accessservice -> Permissioncache: invalidate(target.id)\n  (post-COMMIT)
         Accessservice --> Revokefunctionsview: result + warnings
         Revokefunctionsview --> Frontend: 200 OK
         Frontend --> I: Toast + warnings visuales
       end
     end
   end
 end

 @enduml

