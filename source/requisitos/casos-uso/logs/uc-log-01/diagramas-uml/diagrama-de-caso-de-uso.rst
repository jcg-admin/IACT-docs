8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_application_logs" as INVOKER
 actor "ApplicationLog" as LOG <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nConsultar Logs\ndel Sistema" as UC_LOG_01
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por level\n(warn | error | ...)" as FILTRAR_LEVEL
   usecase "Filtrar por service" as FILTRAR_SERVICE
   usecase "Devolver entries\n(ts + level + msg + ctx)" as DEVOLVER
 }

 INVOKER --> UC_LOG_01
 UC_LOG_01 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_01 ..> FILTRAR_LEVEL : <<include>>
 UC_LOG_01 ..> FILTRAR_SERVICE : <<include>>
 UC_LOG_01 ..> DEVOLVER : <<include>>

 FILTRAR_LEVEL --> LOG
 FILTRAR_SERVICE --> LOG
 DEVOLVER --> LOG

 note bottom of UC_LOG_01
   Diferencia AuditEvent: logs son
   eventos operacionales mutables a
   nivel storage (compactacion,
   retention corta). CNST-009.
   CNST-026 sin PII.
 end note

 note right of LOG
   ApplicationLog: Loki / Elasticsearch /
   CloudWatch / similar.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   entidad ApplicationLog (eventos operacionales).
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   sanitizador de PII en log entries antes de persist.
