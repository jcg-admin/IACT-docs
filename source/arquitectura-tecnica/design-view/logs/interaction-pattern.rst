.. meta::
 :artefacto: AT_DESIGN_SEQ_LOGS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: logs
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_logs:

============================================================
Design View — MOD_Logs: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Logs: consulta de
``ApplicationLog`` con filtros y paginacion. Verifica permiso,
delega a ``AuditQueryService`` (reutilizado de MOD_Audit).

.. uml::
 :caption: MOD_Logs — query con filtros via AuditQueryService.

 @startuml

 actor "view_application_logs" as view_application_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "FilterValidator" as FilterValidator <<sistema>>
 actor "ApplicationLog" as ApplicationLog <<sistema>>
 actor "ColumnCatalog" as ColumnCatalog <<sistema>>

 view_application_logs -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> view_application_logs : OK
 deactivate AuthorizationGuard

 view_application_logs -> AuditQueryService : query_logs(filters)
 activate AuditQueryService

 AuditQueryService -> FilterValidator : validate(filters)
 FilterValidator --> AuditQueryService : OK

 AuditQueryService -> ColumnCatalog : describe(target=application_log)
 activate ColumnCatalog
 ColumnCatalog --> AuditQueryService : columnas exportables
 deactivate ColumnCatalog

 AuditQueryService -> ApplicationLog : query(filters)
 activate ApplicationLog
 ApplicationLog --> AuditQueryService : List<ApplicationLog>
 deactivate ApplicationLog

 AuditQueryService --> view_application_logs : {logs, columnas}
 deactivate AuditQueryService

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/logs/bounded-context`
 - :doc:`/arquitectura-tecnica/use-case-view/logs/index`
 - :doc:`/arquitectura-tecnica/domain-model/application-log`
 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`
 - :doc:`/arquitectura-tecnica/domain-model/column-catalog`
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
