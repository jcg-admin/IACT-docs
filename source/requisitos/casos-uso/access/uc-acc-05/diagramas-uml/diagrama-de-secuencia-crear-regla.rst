8.2 Diagrama de secuencia (crear regla)
=======================================

.. uml::
 :caption: UC_ACC_05 sub-flujo 3.B

 @startuml

 actor Manager as Manager
 participant "Frontend" as Frontend
 participant "CreateSeparationRuleView" as Createseparationruleview
 participant "AccessService" as Accessservice
 participant "FunctionRepo" as Functionrepo
 participant "SeparationRuleRepo" as Separationrulerepo
 participant "SeparationRuleCache" as Separationrulecache
 participant "AuditLog" as Auditlog

 Manager -> Frontend: Define regla con functions
 Frontend -> Createseparationruleview: POST /api/access/separation-rules/

 Createseparationruleview -> Createseparationruleview: Validar JWT + view_separation_rules
 alt Sin permiso
   Createseparationruleview --> Frontend: 403
   Createseparationruleview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Createseparationruleview -> Accessservice: create_separation_rule(payload, invoker)
   Accessservice -> Functionrepo: validate_functions(payload.function_ids)
   alt Funciones invalidas
     Accessservice --> Createseparationruleview: error
     Createseparationruleview --> Frontend: 400
   else OK
     Accessservice -> Separationrulerepo: find_active_with_same_functions(...)
     alt Duplicada
       Accessservice --> Createseparationruleview: SeparationRuleDuplicate
       Createseparationruleview --> Frontend: 409
     else No duplicada
       group Transaccion atomica
         Accessservice -> Separationrulerepo: insert(payload, invoker)
         Accessservice -> Auditlog: emit SEPARATION_RULE_CREATED
       end
       Accessservice -> Separationrulecache: invalidate() (post-COMMIT)
       Accessservice --> Createseparationruleview: rule
       Createseparationruleview --> Frontend: 201 Created
     end
   end
 end

 @enduml

