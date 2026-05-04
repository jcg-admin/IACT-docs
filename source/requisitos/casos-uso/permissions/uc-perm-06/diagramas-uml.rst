.. _uc-perm-06-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_06 — composicion AGR

 @startuml
 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "Users con AGR" as USERS
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_06\nComposicion AGR" as UC06
   usecase "Validar SoD\ncascade" as VSOD
   usecase "INSERT add" as INS
   usecase "DELETE remove" as DEL
   usecase "Audit COMPOSITION_CHANGED" as EMI
 }

 assign_functions_to_group --> UC06
 UC06 ..> VSOD : <<include>>
 UC06 ..> INS : <<include>>
 UC06 ..> DEL : <<include>>
 UC06 ..> EMI : <<include>>
 UC06 ..> USERS : cascade
 EMI --> view_audit_log

 note bottom of UC06
   Cambios en composicion afectan
   a todos los Users con el AGR
 end note

 @enduml

8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_06 — actividad

 @startuml

 start

 :POST functions/ con add + remove + reason;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (assign_functions_to_group?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (AGR existe + ACTIVE + custom?) then (no)
   :404 / 400; stop
 else (si)
 endif

 if (Functions validas?) then (no)
   :400; stop
 else (si)
 endif

 if (change_reason ≥ 20?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 :Filtrar idempotencia;
 :Calcular cascade_affected_user_count;
 :Validar SoD para cada User con AGR
  con set efectivo post-cambio;

 if (Cascade SoD violation?) then (si)
   if (politica strict?) then (si)
     :409 CASCADE_SOD_VIOLATION;
     :Audit COMPOSITION_FAILED;
     stop
   else (permissive)
     :continuar con warning;
   endif
 else (no)
 endif

 :Iniciar transaccion atomica;
 :INSERT AccessGroupFunction (add);
 :DELETE AccessGroupFunction (remove);
 :INSERT AuditEvent
  COMPOSITION_CHANGED;
 :Commit;

 :PermissionCache.invalidate
  para Users con AGR (post-COMMIT);
 :200 OK con resumen + cascade;

 stop

 @enduml

8.3 Diagrama de cascade
=======================

.. uml::
 :caption: Cascade — un cambio en AGR
           afecta N Users

 @startuml

 class AccessGroup {
   id, code, state
 }

 class AccessGroupFunction {
   access_group_id
   function_id
 }

 class Function {
   id, code
 }

 class Assignment {
   user_id
   target_type=AccessGroup
   target_id
 }

 class User {
   id, username
 }

 AccessGroup "1" -- "*" AccessGroupFunction : composicion
 AccessGroupFunction "*" -- "1" Function
 AccessGroup "1" -- "*" Assignment
 Assignment "*" -- "1" User

 note right of AccessGroupFunction
   UC_PERM_06 modifica esta tabla.
   Effect cascade sobre todos los Users
   con AGR via Assignment.
 end note

 @enduml

8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_06 — flujo

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "CompositionView" as Compositionview
 participant "PermService" as Permservice
 participant "SoDValidator" as Sodvalidator
 participant "PermCache" as Permcache
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 Invoker -> Frontend: Define add + remove + reason
 Frontend -> Compositionview: POST .../functions/

 Compositionview -> Compositionview: JWT + RBAC + payload
 Compositionview -> Permservice: change_composition

 Permservice -> Repo: SELECT AGR + functions actuales
 Permservice -> Permservice: filtrar idempotencia
 Permservice -> Repo: Users con AGR + sus effective sets
 Permservice -> Sodvalidator: cascade_validate
 alt cascade SoD violation strict
   Sodvalidator --> Permservice: violations
   Permservice -> Auditlog: emit COMPOSITION_FAILED
   Permservice --> Compositionview: SoDViolation
   Compositionview --> Frontend: 409
 else OK
   group Transaccion atomica
     Permservice -> Repo: INSERT AccessGroupFunction
     Permservice -> Repo: DELETE AccessGroupFunction
     Permservice -> Auditlog: emit COMPOSITION_CHANGED
   end
   Permservice -> Permcache: invalidate users_with_agr
   Permservice --> Compositionview: result
   Compositionview --> Frontend: 200 OK
 end

 @enduml
