.. _uc-usr-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_users" as INVOKER
 actor "User consultado" as TARGET <<pasivo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Users" {
   usecase "UC_USR_02\nConsultar Usuarios" as UC02
   usecase "Listar (paginado)" as LST
   usecase "Ver detalle" as DET
   usecase "Audit selectivo\n(P-16)" as AUDS
 }

 INVOKER --> UC02
 UC02 ..> LST : <<extend>>
 UC02 ..> DET : <<extend>>
 LST ..> AUDS : <<extend (filter user_id)>>
 DET ..> AUDS : <<include>>
 AUDS --> view_audit_log

 note bottom of LST
   list_users (RBAC)
 end note
 note bottom of DET
   view_users (RBAC distinto)
 end note

 @enduml

8.2 Diagrama de secuencia (listado)
===================================

.. uml::
 :caption: UC_USR_02 sub-flujo 3.A

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "ListUsersView" as Listusersview
 participant "UserRepository" as Userrepository
 participant "AuditLog" as Auditlog
 database "Repo Users" as RepoUsers

 Invoker -> Frontend: Navega a "Usuarios" + filtros
 Frontend -> Listusersview: GET /api/users/?...

 Listusersview -> Listusersview: Validar JWT (CNST-009)
 Listusersview -> Listusersview: Verificar list_users (AGR)
 alt Sin permiso
   Listusersview --> Frontend: 403 FORBIDDEN
   Listusersview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Listusersview -> Listusersview: Construir query (whitelist filters)
   Listusersview -> Userrepository: list(filters, page, page_size)
   Userrepository -> RepoUsers: SELECT ... LIMIT ... OFFSET ...
   RepoUsers --> Userrepository: rows
   Userrepository --> Listusersview: results + count
   Listusersview -> Listusersview: Restringir campos PII (CNST-026)
   opt filter user_id presente
     Listusersview -> Auditlog: emit USERS_VIEWED_FOR_USER\n  {target_user_id}
   end
   Listusersview --> Frontend: 200 OK con lista paginada
   Frontend --> Invoker: Tabla renderizada
 end

 @enduml

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

8.4 Diagrama de actividad
=========================

.. uml::
 :caption: UC_USR_02 — actividad combinada

 @startuml

 start

 if (Sub-flujo?) then (listar)
   :GET /api/users/?filtros;
   if (JWT valido?) then (no)
     :401; stop
   else (si)
   endif
   if (list_users?) then (no)
     :403; :Audit UNAUTHORIZED;
     stop
   else (si)
   endif
   if (Filtros validos?) then (no)
     :400 BAD_FILTER; stop
   else (si)
   endif
   :Query con paginacion;
   :Restringir campos PII;
   if (filter user_id?) then (si)
     :Audit USERS_VIEWED_FOR_USER;
   else (no)
   endif
   :200 OK lista;
   stop
 else (detalle)
   :GET /api/users/{id}/;
   if (JWT valido?) then (no)
     :401; stop
   else (si)
   endif
   if (view_users?) then (no)
     :403; :Audit UNAUTHORIZED;
     stop
   else (si)
   endif
   if (User existe?) then (no)
     :404; stop
   else (si)
   endif
   :Cargar Assignments + AGRs;
   :Audit USER_DETAIL_VIEWED;
   :200 OK detalle;
   stop
 endif

 @enduml
