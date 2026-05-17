8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "export_logs" as INVOKER
 actor "ExportWorker" as WORKER <<sistema>>
 actor "ExportJob" as JOB <<sistema>>
 actor "InternalMailbox" as MB <<sistema>>
 actor "ApplicationLog" as LOG <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs (async)" as UC_LOG_04
   usecase "Validar formato\n(jsonl | csv)" as VALIDAR_FORMATO
   usecase "Verificar\ninclude_archive" as VERIFY_ARCHIVE
   usecase "Crear ExportJob\n(202 + job_id)" as CREATE_JOB
   usecase "Generar archivo" as GENERAR
   usecase "Persistir archivo" as PERSIST_FILE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
 }

 INVOKER --> UC_LOG_04
 UC_LOG_04 ..> VALIDAR_FORMATO : <<include>>
 UC_LOG_04 ..> VERIFY_ARCHIVE : <<include>>
 UC_LOG_04 ..> CREATE_JOB : <<include>>
 CREATE_JOB ..> GENERAR : <<include>>
 GENERAR ..> PERSIST_FILE : <<include>>
 GENERAR ..> NOTIFICAR : <<include>>

 CREATE_JOB --> JOB
 GENERAR --> WORKER
 GENERAR --> LOG
 NOTIFICAR --> MB

 note bottom of UC_LOG_04
   Async — devuelve 202 + job_id.
   Reusa P-57/P-64/P-65/P-72.
   Patron consistente con UC_AUD_03.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-026 sin PII.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   fuente de los logs exportados.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   ExportJob con format + archive flag + period.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async que genera el archivo.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon donde se notifica completacion.
