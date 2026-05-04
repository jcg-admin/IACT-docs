.. _uc-acc-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_assignments" as INVOKER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_03\nConsultar Permisos" as UC03
   usecase "Cargar Assignments\ndirectos" as DIR
   usecase "Expandir AGRs\nen funciones" as AGR
   usecase "Cargar permisos\nexcepcionales" as EXC
   usecase "Consolidar\n+ metadata origen" as CONS
   usecase "Detectar SoD\ninformativo" as SOD
   usecase "Audit selectivo\nP-16" as AUDS
 }

 INVOKER --> UC03
 UC03 ..> DIR : <<include>>
 UC03 ..> AGR : <<include>>
 UC03 ..> EXC : <<include>>
 UC03 ..> CONS : <<include>>
 UC03 ..> SOD : <<include>>
 UC03 ..> AUDS : <<include>>
 Sistema --> AUDS
 AUDS --> view_audit_log

 note bottom of CONS
   3 fuentes: direct + AGR + excepcional
   deduplicacion + metadata por funcion
 end note
 note bottom of SOD
   INFORMATIVO no bloqueo
   (UC_ACC_01 valida write-time)
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_03 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "ViewPermsView" as Viewpermsview
 participant "AccessService" as Accessservice
 participant "AssignmentRepo" as Assignmentrepo
 participant "AGRRepo" as Agrrepo
 participant "ExcPermRepo" as Excpermrepo
 participant "SoDValidator" as Sodvalidator
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Click "Ver permisos del User"
 Frontend -> Viewpermsview: GET /api/users/{id}/\n  effective-permissions/

 Viewpermsview -> Viewpermsview: Validar JWT (CNST-009)
 Viewpermsview -> Viewpermsview: Verificar view_assignments\n  o self-view

 alt Sin permiso y no self
   Viewpermsview --> Frontend: 403 FORBIDDEN
   Viewpermsview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Permitido
   Viewpermsview -> Accessservice: get_effective_permissions(\n  target, invoker)

   Accessservice -> Repo: SELECT User
   alt User no existe
     Accessservice --> Viewpermsview: UserNotFound
     Viewpermsview --> Frontend: 404
   else User existe
     Accessservice -> Assignmentrepo: list_active_assignments(target)
     Assignmentrepo --> Accessservice: direct_assignments
     Accessservice -> Assignmentrepo: list_agr_assignments(target)
     Assignmentrepo --> Accessservice: agr_assignments
     Accessservice -> Agrrepo: expand_functions_for_agrs(\n  agr_ids)
     Agrrepo --> Accessservice: agr_functions
     Accessservice -> Excpermrepo: list_active_for_user(\n  target, NOW())
     Excpermrepo --> Accessservice: exceptional_perms
     Accessservice -> Accessservice: consolidar effective set\n  con metadata de origen
     Accessservice -> Accessservice: detectar expired_pending_purge
     Accessservice -> Sodvalidator: detect_violations(set, rules)
     Sodvalidator --> Accessservice: sod_violations (info)

     Accessservice -> Auditlog: emit EFFECTIVE_PERMISSIONS_VIEWED\n  {target_user_id, self_view, counts}

     Accessservice --> Viewpermsview: result
     Viewpermsview --> Frontend: 200 OK con vista consolidada
     Frontend --> I: Tabla con badges de origen
   end
 end

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_03 — actividad

 @startuml

 start

 :GET /api/users/{id}/effective-permissions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (tiene view_assignments\no es self-view?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 :Cargar Assignments directos ACTIVE;
 :Cargar AGR Assignments ACTIVE;
 :Expandir funciones de cada AGR;
 :Cargar ExceptionalPermissions ACTIVE;

 :Consolidar set efectivo
  + metadata origen por funcion;
 :Detectar Assignments con expires_at < NOW()
  (expired_pending_purge);
 :Evaluar SoDRules informativamente
  (sod_violations_detected);

 :Audit EFFECTIVE_PERMISSIONS_VIEWED (P-16);

 :200 OK con vista consolidada;
 :Frontend renderiza tabla con badges;

 stop

 @enduml

8.4 Diagrama de clases — fuentes de permisos
============================================

.. uml::
 :caption: 3 fuentes que UC_ACC_03 consolida

 @startuml

 class User {
   id: int
   username: string
   state: enum
 }

 class Assignment {
   id: int
   user_id: int
   target_type: enum {Function, AccessGroup}
   target_id: int
   state: enum {ACTIVE, REVOKED, EXPIRED}
   granted_at: timestamp
   expires_at: opt[timestamp]
 }

 class AccessGroup {
   id: int
   code: string
   display_name: string
   state: enum
 }

 class Function {
   id: int
   code: string
   display_name: string
   state: enum
 }

 class AccessGroupFunction {
   access_group_id: int
   function_id: int
 }

 class ExceptionalPermission {
   id: int
   user_id: int
   function_id: int
   state: enum
   expires_at: timestamp
   granted_reason: string
 }

 User "1" -- "*" Assignment
 Assignment "*" -- "1" AccessGroup : (target_type=AGR)
 Assignment "*" -- "1" Function : (target_type=Function)
 AccessGroup "1" -- "*" AccessGroupFunction
 AccessGroupFunction "*" -- "1" Function
 User "1" -- "*" ExceptionalPermission
 ExceptionalPermission "*" -- "1" Function

 note right of Assignment
   3 fuentes de Function efectiva:
   1) Assignment (target=Function): direct
   2) Assignment (target=AGR) -> AGR.functions: via_agr
   3) ExceptionalPermission: exceptional
 end note

 @enduml
