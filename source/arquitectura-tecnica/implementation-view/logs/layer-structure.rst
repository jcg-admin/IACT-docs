.. meta::
 :artefacto: AT_IMPL_MOD_SYS_LOGS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_sys_logs:

==========================================
Implementation View — MOD_SysLogs
==========================================

Componentes y paquetes de codigo del modulo de logs del sistema.
Cubre consulta y exportacion de ``ApplicationLog``, ``InfrastructureLog``,
``SystemHealth`` y ``TechnicalMetric``.

.. uml::
 :caption: Implementation View MOD_SysLogs — componentes de logs del sistema.

 @startuml

 package "MOD_SysLogs" {
   component "ApplicationLogView\nInfrastructureLogView\nSystemHealthView\nTechnicalMetricView" as LogView <<api>>
   component "ApplicationLogSerializer\nInfrastructureLogSerializer" as LogSerializer <<serializer>>
   component "SysLogService\nconsultar logs\nexportar a CSV\nfiltrar por nivel/modulo/fecha" as LogService <<service>>
   component "ApplicationLogRepository\nInfrastructureLogRepository\nSystemHealthRepository\nTechnicalMetricRepository" as LogRepo <<repository>>
   component "ApplicationLogORM\nInfrastructureLogORM\nSystemHealthORM\nTechnicalMetricORM" as LogORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 LogView --> LogSerializer : valida
 LogView --> LogService : invoca
 LogService --> LogRepo : consulta / persiste
 LogRepo --> LogORM : mapea
 LogORM --> AlmacenDatos : SQL

 note right of LogService
   ApplicationLog{log_id, level, module, message, timestamp}.
   InfrastructureLog: recursos de infraestructura.
   SystemHealth: estado de servicios del sistema.
   TechnicalMetric: metricas de rendimiento.
   ExportJob{format:CSV} para exportacion masiva.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/application-log`
 :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`
 :doc:`/arquitectura-tecnica/domain-model/system-health`
 :doc:`/arquitectura-tecnica/domain-model/technical-metric`
