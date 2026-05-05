8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_01 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "AssignFunctionsView" as Assignfunctionsview
 participant "AccessService" as Accessservice
 participant "SoDValidator" as Sodvalidator
 participant "PermissionCache" as Permissioncache
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Selecciona funciones + expires_at
 Frontend -> Assignfunctionsview: POST /api/users/{id}/functions/

 Assignfunctionsview -> Assignfunctionsview: Validar JWT (CNST-009)
 Assignfunctionsview -> Assignfunctionsview: Verificar assign_functions
 alt Sin la funcion
   Assignfunctionsview --> Frontend: 403 FORBIDDEN
   Assignfunctionsview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con la funcion
   Assignfunctionsview -> Accessservice: assign(target_id, function_ids,\n  expires_at, invoker)

   Accessservice -> Repo: consultar User para actualizar
   alt User no existe / estado invalido
     Accessservice --> Assignfunctionsview: error
     Assignfunctionsview --> Frontend: 404 / 400
   else User valido
     Accessservice -> Accessservice: validar P-11 (no self-assign)

     Accessservice -> Repo: consultar Function WHERE id IN (...)
     alt Alguna no existe / inactiva
       Accessservice --> Assignfunctionsview: error
       Assignfunctionsview --> Frontend: 400
     else Funciones validas
       Accessservice -> Repo: consultar Assignment activos del User
       Accessservice -> Accessservice: separar new_ids vs already_ids
       alt new_ids vacio (FA-01)
         Accessservice -> Auditlog: emit FUNCTIONS_ASSIGN_NOOP
         Assignfunctionsview --> Frontend: 200 OK informativo
       else hay funciones nuevas
         Accessservice -> Sodvalidator: validate(target,\n  current_functions ∪ new_function_ids)
         Sodvalidator -> Repo: consultar SoDRule WHERE state='ACTIVE'
         alt SoD viola
           Sodvalidator --> Accessservice: SoDViolation(rule_id, pair)
           Accessservice -> Auditlog: emit FUNCTIONS_ASSIGN_FAILED\n  {reason:'sod_violation'}
           Assignfunctionsview --> Frontend: 409 SOD_VIOLATION
         else SoD OK
           group Transaccion atomica
             Accessservice -> Repo: registrar Assignment (N filas)
             Accessservice -> Auditlog: emit FUNCTIONS_ASSIGNED
             opt notify activo
               Accessservice -> Repo: registrar InternalMessage
             end
           end
           Accessservice -> Permissioncache: invalidate(target.id)\n  (post-COMMIT)
           Accessservice --> Assignfunctionsview: result
           Assignfunctionsview --> Frontend: 201 Created
           Frontend --> I: Toast con resumen
         end
       end
     end
   end
 end

 @enduml

