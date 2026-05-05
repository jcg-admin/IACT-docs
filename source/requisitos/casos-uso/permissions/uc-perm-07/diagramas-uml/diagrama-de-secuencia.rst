8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_07 — flujo cache miss

 @startuml

 participant "Caller" as Caller
 participant "PermService" as Permservice
 participant "PermCache" as Permcache
 database "Repos" as Repos

 Caller -> Permservice: check(user_id, function_code)
 Permservice -> Permcache: get(key)
 Permcache --> Permservice: miss

 Permservice -> Repos: query agregada
 Repos --> Permservice: revoked? grant? agr_codes
 Permservice -> Permservice: aplicar precedencia
 Permservice -> Permcache: set(key, result, ttl)
 Permservice --> Caller: result

 note right of Permservice
   Sin audit por invocacion.
   Fail-closed ante BD timeout.
 end note

 @enduml
