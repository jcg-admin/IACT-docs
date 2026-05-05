8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_audit_log" as INVOKER
 actor "AuditQueryService" as AQS <<sistema>>
 actor "AuditRepo" as AR <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nConsultar Auditoria\nGeneral" as UC_AUD_01
   usecase "Validar period\n(default last_7d)" as VALIDAR_PERIOD
   usecase "Aplicar filtros\n(module, event_type)" as FILTROS
   usecase "Cursor-based\npagination" as PAGINACION
   usecase "Construir\ntimeline + summary" as TIMELINE
   usecase "Emitir meta-audit\nGENERAL_AUDIT_QUERIED" as METAAUDIT
 }

 INVOKER --> UC_AUD_01
 UC_AUD_01 ..> VALIDAR_PERIOD : <<include>>
 UC_AUD_01 ..> FILTROS : <<include>>
 UC_AUD_01 ..> PAGINACION : <<include>>
 UC_AUD_01 ..> TIMELINE : <<include>>
 UC_AUD_01 ..> METAAUDIT : <<include>>

 FILTROS --> AQS
 TIMELINE --> AQS
 AQS --> AR
 METAAUDIT --> AS

 note bottom of UC_AUD_01
   Scope: TODOS los modulos.
   Diferencia con UC_PERM_10
   (RBAC/auth scope) — funciones
   RBAC separadas por P-15.
 end note

 note bottom of METAAUDIT
   P-44 audit del audit:
   toda consulta a la bitacora
   genera AuditEvent.
   CNST-008/009/013/025/026.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura de eventos consultados (CNST-025 inmutable).
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo append-only con read-replica para queries.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   servicio que ejecuta filtros + pagination.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor del meta-audit GENERAL_AUDIT_QUERIED (P-44).
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   componente que codifica cursor de paginacion.
