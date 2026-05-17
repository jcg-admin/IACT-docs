.. meta::
 :artefacto: AT_UC_PIP_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_pip_04_solicitar_reintento_de_pipeline:

==============================================
UC_PIP_04 — Solicitar Reintento de Pipeline
==============================================

Operador / data engineer solicita reintento de un Pipeline failed sin
esperar siguiente schedule. ``request_pipeline_retry`` con reason
obligatoria + verify_idle (no race con run en curso). P-39 audit
reforzado. Importante para recovery de errores transitorios.

.. uml::
 :caption: UC_PIP_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "request_pipeline_retry" as request_pipeline_retry
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "PipelineExecutionRepo" as PipelineExecutionRepo <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nSolicitar Reintento\nde Pipeline" as UC_PIP_04
   usecase "Verificar\nrequest_pipeline_retry" as VERIFICAR_AGR
   usecase "Validar reason\nobligatoria" as VALIDAR_REASON
   usecase "Verificar no hay\nejecucion en curso" as VERIFY_IDLE
   usecase "Disparar reintento" as DISPATCH
   usecase "Persistir nueva\nPipelineExecution" as PERSISTIR
   usecase "Invalidar MetricsCache\n(datasets afectados)" as INVALIDAR_CACHE
   usecase "Emitir AuditEvent\nPIPELINE_RETRY_REQUESTED\n(P-39)" as AUDITAR
 }

 request_pipeline_retry --> UC_PIP_04

 UC_PIP_04 ..> VERIFICAR_AGR : <<include>>
 UC_PIP_04 ..> VALIDAR_REASON : <<include>>
 UC_PIP_04 ..> VERIFY_IDLE : <<include>>
 UC_PIP_04 ..> DISPATCH : <<include>>
 UC_PIP_04 ..> PERSISTIR : <<include>>
 UC_PIP_04 ..> INVALIDAR_CACHE : <<include>>
 UC_PIP_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VERIFY_IDLE --> PipelineExecutionRepo
 DISPATCH --> EvaluatorReloader
 PERSISTIR --> PipelineExecution
 INVALIDAR_CACHE --> MetricsCache
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFY_IDLE
   Bloquea retry si hay run en curso
   (PipelineExecutionRepo.verify_idle).
   Evita race conditions.
 end note

 note bottom of AUDITAR
   P-39 audit reforzado:
   reason + invoker + trimestre.
   CNST-013 + CNST-025.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   nueva ejecucion.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo` —
   verify_idle + create.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   logs del nuevo run.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   dispara nueva ejecucion.
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
   invalidada para datasets.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   RetryPolicyStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (P-39).
 - :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
   spec textual.
