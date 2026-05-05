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

 Permservice -> Repo: consultar AGR + functions actuales
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
     Permservice -> Repo: registrar AccessGroupFunction
     Permservice -> Repo: eliminar AccessGroupFunction
     Permservice -> Auditlog: emit COMPOSITION_CHANGED
   end
   Permservice -> Permcache: invalidate users_with_agr
   Permservice --> Compositionview: result
   Compositionview --> Frontend: 200 OK
 end

 @enduml
