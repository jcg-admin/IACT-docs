.. meta::
 :artefacto: AT_UC_LOG_02_USECASE
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

.. _at_uc_log_02_consultar_logs_del_etl:

============================================================
UC_LOG_02 — Consultar Logs Pipeline
============================================================

Variante de UC_LOG_01 con scope Pipeline (rename CNST-033 §8.2).
Funcion separada P-15: ``view_pipeline_logs`` para data engineers
(ven Pipeline sin acceso al sistema general).

.. uml::
 :caption: UC_LOG_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_pipeline_logs" as view_pipeline_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PipelineLog" as PipelineLog <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs\ndel Pipeline" as UC_LOG_02
   usecase "Verificar\nview_pipeline_logs" as VERIFICAR_AGR
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Forzar service ∈\n{etl-runner, etl-validator,\netl-transformer}" as FORZAR_SERVICE
   usecase "Filtrar por\npipeline_id" as FILTRAR_PIP
   usecase "Devolver entries" as DEVOLVER
 }

 view_pipeline_logs --> UC_LOG_02

 UC_LOG_02 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_02 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_02 ..> FORZAR_SERVICE : <<include>>
 UC_LOG_02 ..> FILTRAR_PIP : <<include>>
 UC_LOG_02 ..> DEVOLVER : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FORZAR_SERVICE --> PipelineLog
 FILTRAR_PIP --> PipelineLog
 DEVOLVER --> PipelineLog

 note bottom of UC_LOG_02
   Variante de UC_LOG_01 con scope
   Pipeline forzado. Funcion separada
   P-15: data engineers acceso a
   Pipeline sin sistema general.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   PipelineLog especificos.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   referenciada por pipeline_id.
 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   storage compartido.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-02/index` —
   spec textual.
