.. meta::
 :artefacto: AT_UC_LOG_01_USECASE
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

.. _at_uc_log_01_consultar_logs_del_sistema:

============================================================
UC_LOG_01 — Consultar Logs Sistema
============================================================

List de ApplicationLog con filtros (period, level, service).
``view_application_logs``. Diferencia con AuditEvent: logs son
eventos operacionales mutables (compactacion, retention corta).

.. uml::
 :caption: UC_LOG_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_application_logs" as view_application_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ApplicationLog" as ApplicationLog <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nConsultar Logs\ndel Sistema" as UC_LOG_01
   usecase "Verificar\nview_application_logs" as VERIFICAR_AGR
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por level\n(warn | error | ...)" as FILTRAR_LEVEL
   usecase "Filtrar por service" as FILTRAR_SERVICE
   usecase "Devolver entries\n(ts + level + msg + ctx)" as DEVOLVER
 }

 view_application_logs --> UC_LOG_01

 UC_LOG_01 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_01 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_01 ..> FILTRAR_LEVEL : <<include>>
 UC_LOG_01 ..> FILTRAR_SERVICE : <<include>>
 UC_LOG_01 ..> DEVOLVER : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR_LEVEL --> ApplicationLog
 FILTRAR_SERVICE --> ApplicationLog
 DEVOLVER --> ApplicationLog

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   eventos operacionales.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   PII en log entries.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-01/index` —
   spec textual.
