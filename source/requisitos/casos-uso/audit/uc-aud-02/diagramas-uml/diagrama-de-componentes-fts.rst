.. _uc-aud-02-parte-08-diagrama-componentes-fts:

8.3 Diagrama de componentes — FTS Audit
=========================================

.. uml::
 :caption: UC_AUD_02 — arquitectura FTS para audit search.

 @startuml

 component "AuditEvent BD" as AuditEventBd
 component "Sync trigger\n(post-INSERT)" as SyncTrigger
 component "FTS Index" as FtsIndex
 component "Search Service" as SearchService

 AuditEventBd --> SyncTrigger : emite eventos\nnuevos
 SyncTrigger --> FtsIndex : actualiza indice
 SearchService --> FtsIndex : query
 SearchService --> AuditEventBd : detalle por id

 note bottom of SyncTrigger
   El trigger asegura consistency
   eventual entre la BD canonica
   y el indice FTS.
 end note

 note bottom of FtsIndex
   Indice optimizado para busqueda
   full-text con ranking de
   relevancia. Implementacion
   concreta en arquitectura-tecnica/.
 end note

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event`.
