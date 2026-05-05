.. meta::
 :artefacto: AT_UC_LOG_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_log_05_ver_logs_de_infraestructura:

============================================================
UC_LOG_05 — Ver Logs de Infraestructura
============================================================

Logs a nivel host: agregadores de infraestructura (node-exporter,
fluent-bit, etc.). ``view_infrastructure_logs``. Filter por host.

.. uml::
 :caption: UC_LOG_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_infrastructure_logs" as view_infrastructure_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "InfrastructureLog" as InfrastructureLog <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nVer Logs de Infraestructura" as UC_LOG_05
   usecase "Verificar\nview_infrastructure_logs" as VERIFICAR_AGR
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por host" as FILTRAR_HOST
   usecase "Devolver entries" as DEVOLVER
 }

 view_infrastructure_logs --> UC_LOG_05

 UC_LOG_05 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_05 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_05 ..> FILTRAR_HOST : <<include>>
 UC_LOG_05 ..> DEVOLVER : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR_HOST --> InfrastructureLog
 DEVOLVER --> InfrastructureLog

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log` —
   InfrastructureLog (host-level).
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-05/index` —
   spec textual.
