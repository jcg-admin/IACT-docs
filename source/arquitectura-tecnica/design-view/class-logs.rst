.. meta::
 :artefacto: AT_DESIGN_CLASS_LOGS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_logs:

============================================================
Design View — MOD_Logs: Estructura de Clases
============================================================

Modulo de **observabilidad tecnica**: logs de aplicacion,
infraestructura, ETL; metricas tecnicas (latencias, throughput).
Distinto de MOD_Audit (auditoria de negocio).

.. uml::
 :caption: MOD_Logs — clases canonicas y relaciones internas.

 @startuml

 class ApplicationLog
 class InfrastructureLog
 class TechnicalMetric
 class ColumnCatalog
 class AuditQueryService <<sistema>>
 class KpiCalculator <<sistema>>
 class AuthorizationGuard <<sistema>>

 ApplicationLog --> ColumnCatalog : describe campos
 InfrastructureLog --> ColumnCatalog
 TechnicalMetric --> ColumnCatalog

 AuditQueryService ..> ApplicationLog : query con filtros
 AuditQueryService ..> InfrastructureLog
 KpiCalculator ..> TechnicalMetric : agrega p95/p99

 AuthorizationGuard ..> AuditQueryService : verify view_logs

 note bottom of ColumnCatalog
   Catalogo dinamico de columnas
   exportables (export-job).
 end note

 @enduml

----

UCs cubiertos
==============

UC_LOG_01..07 — consultar logs sistema, ETL, infra; exportar
logs; ver estado del sistema; ver metricas tecnicas. Ver
:doc:`/arquitectura-tecnica/use-case-view/logs/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log`
 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric`
 - :doc:`/arquitectura-tecnica/domain-model/column-catalog`
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/use-case-view/logs/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-logs`
