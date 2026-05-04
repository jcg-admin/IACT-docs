.. _uc-acc-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_04 — actores y casos asociados

 @startuml
 left to right direction

 actor "assign_function_groups" as INVOKER
 actor "User destino" as TARGET <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR" as UC04
   usecase "Validar AGR\nexiste + ACTIVE" as VAGR
   usecase "Expandir funciones\ndel AGR" as EXP
   usecase "Validar SoD\n(set efectivo)" as SOD
   usecase "INSERT Assignment\n(target=AGR)" as INS
   usecase "Invalidar cache" as CACHE
   usecase "AuditEvent\nAGR_ASSIGNED" as EMI
 }

 INVOKER --> UC04
 UC04 ..> VAGR : <<include>>
 UC04 ..> EXP : <<include>>
 UC04 ..> SOD : <<include>>
 UC04 ..> INS : <<include>>
 UC04 ..> CACHE : <<include>>
 UC04 ..> EMI : <<include>>
 EMI --> view_audit_log

 note bottom of SOD
   SoD se evalua sobre FUNCIONES,
   no sobre AGRs como entidad
 end note

 @enduml

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
 participant "SoDValidator" as Sodvalidator
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

   Accessservice -> Repo: SELECT User FOR UPDATE
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
       Accessservice -> Repo: SELECT Assignment\n  WHERE user=target\n  AND target_type='AccessGroup'\n  AND target_id=agr.id\n  AND state='ACTIVE'
       alt Ya asignado (FA-01)
         Accessservice -> Auditlog: emit AGR_ASSIGN_NOOP
         Assignagrview --> Frontend: 200 OK informativo
       else No asignado
         Accessservice -> Agrrepository: list_functions(agr_id)
         Agrrepository --> Accessservice: agr_functions
         Accessservice -> Accessservice: build effective_post_assign\n  = current_effective ∪ agr_functions
         Accessservice -> Sodvalidator: validate(effective_post_assign,\n  rules)
         alt SoD viola
           Sodvalidator --> Accessservice: SoDViolation
           Accessservice -> Auditlog: emit AGR_ASSIGN_FAILED
           Assignagrview --> Frontend: 409
         else SoD OK
           group Transaccion atomica
             Accessservice -> Repo: INSERT Assignment\n  (target_type='AccessGroup',\n   target_id=agr.id, ...)
             Accessservice -> Auditlog: emit AGR_ASSIGNED
             opt notify
               Accessservice -> Repo: INSERT InternalMessage
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

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_04 — actividad

 @startuml

 start

 :POST /api/users/{id}/access-groups/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene assign_function_groups?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 if (User state OK?) then (no)
   :400 INVALID_USER_STATE; stop
 else (si)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_ASSIGN_FORBIDDEN;
   :Audit ALERTA;
   stop
 else (no)
 endif

 if (AGR existe + ACTIVE?) then (no)
   :400 ACCESS_GROUP_NOT_FOUND/INACTIVE; stop
 else (si)
 endif

 if (Ya asignado?) then (si)
   :Audit AGR_ASSIGN_NOOP;
   :200 OK informativo;
   stop
 else (no)
 endif

 :Expandir funciones del AGR;
 :Construir effective_post_assign
  = current ∪ agr_functions;
 :Evaluar SoDRules;

 if (SoD viola?) then (si)
   :409 SOD_VIOLATION;
   :Audit AGR_ASSIGN_FAILED;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :INSERT Assignment (target=AGR);
   :INSERT AuditEvent AGR_ASSIGNED;
   if (notify activo?) then (si)
     :INSERT InternalMessage;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :PermissionCache.invalidate (post-COMMIT);
 :201 Created con resumen;

 stop

 @enduml

8.4 Diagrama AGR como agregacion
================================

.. uml::
 :caption: AGR contiene funciones — UC_ACC_04 asigna el AGR

 @startuml

 class User {
   id, username
 }

 class Assignment {
   id, user_id
   target_type: AccessGroup
   target_id: int (= agr.id)
   state, granted_at,
   expires_at?
 }

 class AccessGroup {
   id, code, display_name
   state
 }

 class AccessGroupFunction {
   access_group_id
   function_id
 }

 class Function {
   id, code, display_name
 }

 User "1" --> "*" Assignment
 Assignment "*" --> "1" AccessGroup : (target=AGR)
 AccessGroup "1" -- "*" AccessGroupFunction
 AccessGroupFunction "*" -- "1" Function

 note right of Assignment
   UC_ACC_04 crea ESTE Assignment
   con target_type='AccessGroup'
 end note

 note right of AccessGroupFunction
   UC_PERM_06 manipula esta tabla
   (composicion del AGR)
 end note

 @enduml
