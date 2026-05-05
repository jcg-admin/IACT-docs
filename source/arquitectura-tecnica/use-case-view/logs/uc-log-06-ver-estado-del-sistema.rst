.. meta::
 :artefacto: AT_UC_LOG_06_USECASE
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

.. _at_uc_log_06_ver_estado_del_sistema:

============================================================
UC_LOG_06 — Ver Estado del Sistema
============================================================

Single-pane-of-glass: agrega Servicios HTTP/DB/Queue + Dependencies +
Pipeline summary (UC_PIP_01) + Alertas count (UC_ALR_02) en un overall
green|yellow|red. ``view_system_health``. BReq-006.

.. uml::
 :caption: UC_LOG_06 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_system_health" as view_system_health
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SystemHealth" as SystemHealth <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "AlertRepo" as AlertRepo <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nVer Estado del Sistema" as UC_LOG_06
   usecase "Verificar\nview_system_health" as VERIFICAR_AGR
   usecase "Aggregar status\nde Servicios HTTP/DB/Queue" as STATUS_SVC
   usecase "Aggregar Dependencies" as STATUS_DEP
   usecase "Resumen Pipeline\n(UC_PIP_01)" as STATUS_ETL
   usecase "Count Alertas activas\n(UC_ALR_02)" as STATUS_ALR
   usecase "Calcular overall\n(green | yellow | red)" as OVERALL
 }

 view_system_health --> UC_LOG_06

 UC_LOG_06 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_06 ..> STATUS_SVC : <<include>>
 UC_LOG_06 ..> STATUS_DEP : <<include>>
 UC_LOG_06 ..> STATUS_ETL : <<include>>
 UC_LOG_06 ..> STATUS_ALR : <<include>>
 UC_LOG_06 ..> OVERALL : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 STATUS_SVC --> SystemHealth
 STATUS_DEP --> SystemHealth
 STATUS_ETL --> PipelineExecution
 STATUS_ALR --> AlertRepo
 OVERALL --> SystemHealth

 note bottom of UC_LOG_06
   BReq-006. Overall green|yellow|red
   computado de los 4 inputs.
   Auto-refresh dashboard.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/system-health` —
   estado agregado.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   summary Pipeline (UC_PIP_01).
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
   alertas activas (UC_ALR_02).
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric` —
   metricas tecnicas.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-06/index` —
   spec textual.
