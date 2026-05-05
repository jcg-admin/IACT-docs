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
   Userrepository -> RepoUsers: consultar ... LIMIT ... OFFSET ...
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

