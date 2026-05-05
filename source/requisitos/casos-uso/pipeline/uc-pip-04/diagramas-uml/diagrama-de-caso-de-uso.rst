8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "request_pipeline_retry" as INVOKER
 actor "PipelineDispatcher" as DISPATCHER <<sistema>>
 actor "PipelineExecutionRepo" as REPO <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nSolicitar Reintento\nde Pipeline" as UC_PIP_04
   usecase "Validar reason\nobligatoria" as VALIDAR_REASON
   usecase "Verificar no hay\nejecucion en curso" as VERIFY_IDLE
   usecase "Disparar reintento\n(invocar Pipeline)" as DISPATCH
   usecase "Persistir nueva\nejecucion" as PERSISTIR
   usecase "AuditEvent\nPIPELINE_RETRY_REQUESTED\n(P-39 reforzado)" as AUDIT
 }

 INVOKER --> UC_PIP_04
 UC_PIP_04 ..> VALIDAR_REASON : <<include>>
 UC_PIP_04 ..> VERIFY_IDLE : <<include>>
 UC_PIP_04 ..> DISPATCH : <<include>>
 UC_PIP_04 ..> PERSISTIR : <<include>>
 UC_PIP_04 ..> AUDIT : <<include>>

 DISPATCH --> DISPATCHER
 PERSISTIR --> REPO
 Sistema --> AUDIT
 AUDIT --> view_audit_log

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
