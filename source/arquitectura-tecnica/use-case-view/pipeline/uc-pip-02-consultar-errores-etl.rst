.. meta::
 :artefacto: AT_UC_PIP_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_pip_02_consultar_errores_etl:

============================================================
UC_PIP_02 — Consultar Errores Pipeline
============================================================

Diagnostica pipelines failed: stack trace, error code, payload muestra
(sin PII), correlation_id para tracing. ``view_pipeline_errors``.
CNST-026: stack traces sanitizados via PIIScanner + Sanitizer.

.. uml::
 :caption: UC_PIP_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_pipeline_errors" as view_pipeline_errors
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "PipelineLog" as PipelineLog <<sistema>>
 actor "PIIScanner" as PIIScanner <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nConsultar Errores\ndel Pipeline" as UC_PIP_02
   usecase "Verificar\nview_pipeline_errors" as VERIFICAR_AGR
   usecase "Filtrar ejecuciones\nfailed" as FILTRAR
   usecase "Cargar stack trace\n+ error_code" as CARGAR_TRACE
   usecase "Sanitizar payload\n(sin PII)" as SANITIZAR
   usecase "Devolver correlation_id" as CORRELATION
 }

 view_pipeline_errors --> UC_PIP_02

 UC_PIP_02 ..> VERIFICAR_AGR : <<include>>
 UC_PIP_02 ..> FILTRAR : <<include>>
 UC_PIP_02 ..> CARGAR_TRACE : <<include>>
 UC_PIP_02 ..> SANITIZAR : <<include>>
 UC_PIP_02 ..> CORRELATION : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR --> PipelineExecution
 CARGAR_TRACE --> PipelineLog
 SANITIZAR --> PIIScanner
 SANITIZAR --> Sanitizer

 note bottom of SANITIZAR
   Stack traces pueden contener PII
   (CNST-026). PIIScanner detecta,
   Sanitizer reemplaza.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   PipelineExecution failed.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   stack traces detallados.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   reemplaza PII.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index` —
   spec textual.
