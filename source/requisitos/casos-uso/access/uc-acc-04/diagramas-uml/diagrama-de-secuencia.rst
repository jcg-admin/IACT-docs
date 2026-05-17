8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_04 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "AssignAGRView" as Assignagrview
 participant "AccessService" as Accessservice
 participant "AGRRepository" as Agrrepository
 participant "SeparationRuleValidator" as Sodvalidator
 participant "PermissionCache" as Permissioncache
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Selecciona Agrrepository + User
 Frontend -> Assignagrview: POST /api/users/{id}/access-groups/

 Assignagrview -> Assignagrview: Validar JWT (CNST-009)
 Assignagrview -> Assignagrview: Verificar assign_function_groups
 alt Sin la funcion
   Assignagrview --> Frontend: 403
   Assignagrview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else
   Assignagrview -> Accessservice: assign_agr(target_id, agr_id,\n  expires_at, invoker)

   Accessservice -> Repo: consultar User para actualizar
   alt User no existe / state invalido
     Accessservice --> Assignagrview: error
     Assignagrview --> Frontend: 404 / 400
   else User OK
     Accessservice -> Accessservice: validar P-11
     Accessservice -> Agrrepository: get(agr_id)
     alt Agrrepository no existe / inactivo
       Accessservice --> Assignagrview: error
       Assignagrview --> Frontend: 400
     else Agrrepository OK
       Accessservice -> Repo: consultar Assignment\n  WHERE user=target\n  AND target_type='AccessGroup'\n  AND target_id=agr.id\n  AND state='ACTIVE'
       alt Ya asignado (FA-01)
         Accessservice -> Auditlog: emit AGR_ASSIGN_NOOP
         Assignagrview --> Frontend: 200 OK informativo
       else No asignado
         Accessservice -> Agrrepository: list_functions(agr_id)
         Agrrepository --> Accessservice: agr_functions
         Accessservice -> Accessservice: build effective_post_assign\n  = current_effective ∪ agr_functions
         Accessservice -> Sodvalidator: validate(effective_post_assign,\n  rules)
         alt separacion viola
           Sodvalidator --> Accessservice: SeparationRuleViolation
           Accessservice -> Auditlog: emit AGR_ASSIGN_FAILED
           Assignagrview --> Frontend: 409
         else separacion OK
           group Transaccion atomica
             Accessservice -> Repo: registrar Assignment\n  (target_type='AccessGroup',\n   target_id=agr.id, ...)
             Accessservice -> Auditlog: emit AGR_ASSIGNED
             opt notify
               Accessservice -> Repo: registrar InternalMessage
             end
           end
           Accessservice -> Permissioncache: invalidate(target.id)
           Accessservice --> Assignagrview: result
           Assignagrview --> Frontend: 201 Created
           Frontend --> I: Toast con resumen
         end
       end
     end
   end
 end

 @enduml

