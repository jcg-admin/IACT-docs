8.3 Vista de impacto
====================

.. uml::

 @startuml
 actor "system_admin" as admin
 participant "SystemGroupEndpoint" as ENDPOINT_GRUPOS_SISTEMA
 participant "PermissionsEngine" as MODULO_ETL
 participant "UserRepo" as REPOSITORIO_USUARIO

 admin -> ENDPOINT_GRUPOS_SISTEMA : GET /impact/?add=codename
 ENDPOINT_GRUPOS_SISTEMA -> REPOSITORIO_USUARIO : users_with_agr(group_id)
 REPOSITORIO_USUARIO --> ENDPOINT_GRUPOS_SISTEMA : [user_ids]
 ENDPOINT_GRUPOS_SISTEMA -> MODULO_ETL : preview_effective_set(\n  group_id, add=codename)
 MODULO_ETL --> ENDPOINT_GRUPOS_SISTEMA : ImpactReport
 ENDPOINT_GRUPOS_SISTEMA --> admin : { affected_users: N,\n  preview: [...] }
 note right : No persiste ningun cambio
 @enduml
