.. _uc-aud-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "search_audit_log" as search_audit_log
 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar" as UC02
   usecase "UC_PERM_09\nMeta-audit" as UcPerm09
 }
 search_audit_log --> UC02
 UC02 ..> UcPerm09 : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST search;
 :JWT + RBAC;
 :Validar query + range ≤ 90;
 :Throttle check;
 :FTS search;
 :Sanitize results;
 :Meta-audit;
 :200;
 stop
 @enduml

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

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "FTS" as Fts
 participant "AuditSvc" as Auditsvc
 User -> Endpoint: POST search
 Endpoint -> Endpoint: JWT + RBAC + validar
 Endpoint -> Fts: search query
 Fts --> Endpoint: hits
 Endpoint -> Auditsvc: emit AUDIT_SEARCH_QUERIED
 Endpoint --> User: 200
 @enduml
