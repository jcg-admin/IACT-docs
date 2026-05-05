8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "request_pipeline_retry" as INVOKER
 actor "PipelineExecution" as PE <<sistema>>
 actor "EvaluatorReloader" as EE <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nSolicitar Reintento\nde Pipeline" as UC_PIP_04
   usecase "Validar reason\nobligatoria" as VALIDAR_REASON
   usecase "Verificar no hay\nejecucion en curso" as VERIFY_IDLE
   usecase "Disparar reintento\n(invocar Pipeline)" as DISPATCH
   usecase "Persistir nueva\nPipelineExecution" as PERSISTIR
   usecase "Emitir AuditEvent\nPIPELINE_RETRY_REQUESTED\n(P-39 reforzado)" as AUDIT
 }

 INVOKER --> UC_PIP_04
 UC_PIP_04 ..> VALIDAR_REASON : <<include>>
 UC_PIP_04 ..> VERIFY_IDLE : <<include>>
 UC_PIP_04 ..> DISPATCH : <<include>>
 UC_PIP_04 ..> PERSISTIR : <<include>>
 UC_PIP_04 ..> AUDIT : <<include>>

 VERIFY_IDLE --> PE
 DISPATCH --> EE
 PERSISTIR --> PE
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VERIFY_IDLE
   No hay ejecucion del Pipeline
   en curso al momento de la
   solicitud — evita races.
 end note

 note bottom of AUDIT
   Operacion sensitiva: P-39
   audit reforzado con reason +
   trimestre + invoker.
   CNST-013 + CNST-025.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   PipelineExecution (verifica IDLE + persiste retry).
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   log de eventos del nuevo run.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   componente que dispara la nueva ejecucion.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent PIPELINE_RETRY_REQUESTED (P-39).
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-013/025).
