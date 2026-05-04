8.3 Vista de impacto
====================

.. uml::

 @startuml
 actor "admin_sistema" as admin
 participant "SystemGroupEndpoint" as EP
 participant "PermissionsEngine" as PE
 participant "UserRepo" as UR

 admin -> EP : GET /impact/?add=codename
 EP -> UR : users_with_agr(group_id)
 UR --> EP : [user_ids]
 EP -> PE : preview_effective_set(\n  group_id, add=codename)
 PE --> EP : ImpactReport
 EP --> admin : { affected_users: N,\n  preview: [...] }
 note right : No persiste ningun cambio
 @enduml
