8.3 Componente FTS
==================

.. uml::

 @startuml
 component "AuditEvent BD" as AuditeventBd
 component "Sync trigger" as SyncTrigger
 component "FTS Index" as FtsIndex
 component "Search service" as SearchService
 AuditeventBd --> SyncTrigger
 SyncTrigger --> FtsIndex
 SearchService --> FtsIndex
 @enduml

