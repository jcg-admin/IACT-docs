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
 participant "SeparationRuleValidator" as Sodvalidator
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

   Accessservice -> Repo: consultar User
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
     Accessservice -> Excpermrepo: list_active_for_user(\n  target, marca_tiempo_actual)
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

