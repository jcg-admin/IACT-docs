8.3 Diagrama de secuencia (detalle)
===================================

.. uml::
 :caption: UC_USR_02 sub-flujo 3.B

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "UserDetailView" as Userdetailview
 participant "UserRepository" as UREP
 participant "AssignmentRepository" as AREP
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 Invoker -> Frontend: Click en User X
 Frontend -> Userdetailview: GET /api/users/{X}/

 Userdetailview -> Userdetailview: Validar JWT
 Userdetailview -> Userdetailview: Verificar view_users
 alt Sin permiso
   Userdetailview --> Frontend: 403 FORBIDDEN
   Userdetailview -> Auditlog: UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Userdetailview -> UREP: get(X)
   alt User no existe
     Userdetailview --> Frontend: 404
   else
     UREP --> Userdetailview: user
     Userdetailview -> AREP: list_active(user)
     AREP --> Userdetailview: assignments
     Userdetailview -> Auditlog: emit USER_DETAIL_VIEWED\n  {target_user_id: X,\n   target_state: user.state,\n   self_view: invoker == user}
     Userdetailview --> Frontend: 200 OK con detalle completo
     Frontend --> Invoker: Vista detalle
   end
 end

 @enduml

