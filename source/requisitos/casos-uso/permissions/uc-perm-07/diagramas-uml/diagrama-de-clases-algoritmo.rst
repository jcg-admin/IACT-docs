8.3 Diagrama de clases (algoritmo)
==================================

.. uml::
 :caption: Estructura del servicio

 @startuml

 class PermissionService {
   check(user_id, function_code, ctx)
   check_bulk(user_id, codes, ctx)
 }

 class PermissionCache {
   get(key)
   set(key, value, ttl)
   invalidate(user_id)
 }

 class ExceptionalPermissionRepo {
   find_active_revoke(user, fn)
   find_active_grant(user, fn)
 }

 class AssignmentRepo {
   find_active_agrs_with_function(
     user, fn)
 }

 PermissionService --> PermissionCache
 PermissionService --> ExceptionalPermissionRepo
 PermissionService --> AssignmentRepo

 note right of PermissionService
   Funcion pura: dado el set de datos
   leidos, el resultado es deterministico.
 end note

 @enduml

