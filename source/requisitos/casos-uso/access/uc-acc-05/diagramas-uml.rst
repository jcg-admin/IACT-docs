.. _uc-acc-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_05 — actores y casos asociados

 @startuml
 left to right direction

 actor "view_separation_rules" as VIEWER
 actor "view_separation_rules" as MANAGER
 actor "view_audit_log" as view_audit_log
 actor "Sistema (consumidores)" as SistemaConsumidores

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar SoD" as UC05
   usecase "Listar reglas" as LST
   usecase "Crear regla" as UCCRE
   usecase "Modificar regla" as UCMOD
   usecase "Retirar regla" as UCRET
   usecase "AuditEvent" as EMI
   usecase "Invalidar cache\nde reglas" as CACHE
 }

 VIEWER --> UC05
 MANAGER --> UC05
 UC05 ..> LST : <<extend>>
 UC05 ..> UCCRE : <<extend>>
 UC05 ..> UCMOD : <<extend>>
 UC05 ..> UCRET : <<extend>>
 UCCRE ..> EMI : <<include>>
 UCMOD ..> EMI : <<include>>
 UCRET ..> EMI : <<include>>
 UCCRE ..> CACHE : <<include>>
 UCMOD ..> CACHE : <<include>>
 UCRET ..> CACHE : <<include>>
 EMI --> view_audit_log
 SistemaConsumidores ..> CACHE : <<consume>>

 note bottom of CACHE
   UC_ACC_01/04/PERM_03 cargan reglas
   ACTIVE en cache para SoD write-time
 end note

 @enduml

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

8.3 Diagrama de actividad (CRUD comun)
======================================

.. uml::
 :caption: UC_ACC_05 — actividad de operacion CRUD generica

 @startuml

 start

 :Request CRUD recibido;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (RBAC apropiado para operacion?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (Validar payload + recursos?) then (no)
   :400 / 404 / 409; stop
 else (si)
 endif

 :Iniciar transaccion atomica;
 :Aplicar operacion (INSERT, UPDATE, o
  UPDATE state=RETIRED segun caso);
 :INSERT AuditEvent SOD_RULE_X;
 :Commit transaccion;

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :SoDRuleCache.invalidate (post-COMMIT);
 :200 / 201;

 stop

 @enduml

Cada sub-flujo (LISTAR, CREAR, MODIFICAR,
RETIRAR) sigue este esqueleto comun. Las
validaciones especificas por operacion estan
en Parte 5 — Excepciones.

8.4 Diagrama de estados — SoDRule
=================================

.. uml::
 :caption: Maquina de estados de SoDRule

 @startuml

 [*] --> ACTIVE : UC_ACC_05 CREATE

 ACTIVE --> ACTIVE : UC_ACC_05 PATCH
 ACTIVE --> RETIRED : UC_ACC_05 DELETE
 RETIRED --> [*] : (terminal — historial\npreservado)

 note right of RETIRED
   retired_at, retired_by_admin_id,
   retire_reason
   No vuelve a ACTIVE
   (migracion: CREATE nueva)
 end note

 @enduml
