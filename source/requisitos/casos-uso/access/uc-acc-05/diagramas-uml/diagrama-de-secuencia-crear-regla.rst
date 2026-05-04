8.2 Diagrama de secuencia (crear regla)
=======================================

.. uml::
 :caption: UC_ACC_05 sub-flujo 3.B

 @startuml

 actor Manager as Manager
 participant "Frontend" as Frontend
 participant "CreateSoDRuleView" as Createsodruleview
 participant "AccessService" as Accessservice
 participant "FunctionRepo" as Functionrepo
 participant "SoDRuleRepo" as Sodrulerepo
 participant "SoDRuleCache" as Sodrulecache
 participant "AuditLog" as Auditlog

 Manager -> Frontend: Define regla con functions
 Frontend -> Createsodruleview: POST /api/access/sod-rules/

 Createsodruleview -> Createsodruleview: Validar JWT + view_separation_rules
 alt Sin permiso
   Createsodruleview --> Frontend: 403
   Createsodruleview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Createsodruleview -> Accessservice: create_sod_rule(payload, invoker)
   Accessservice -> Functionrepo: validate_functions(payload.function_ids)
   alt Funciones invalidas
     Accessservice --> Createsodruleview: error
     Createsodruleview --> Frontend: 400
   else OK
     Accessservice -> Sodrulerepo: find_active_with_same_functions(...)
     alt Duplicada
       Accessservice --> Createsodruleview: SoDRuleDuplicate
       Createsodruleview --> Frontend: 409
     else No duplicada
       group Transaccion atomica
         Accessservice -> Sodrulerepo: insert(payload, invoker)
         Accessservice -> Auditlog: emit SOD_RULE_CREATED
       end
       Accessservice -> Sodrulecache: invalidate() (post-COMMIT)
       Accessservice --> Createsodruleview: rule
       Createsodruleview --> Frontend: 201 Created
     end
   end
 end

 @enduml

