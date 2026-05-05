8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "export_audit_log" as INVOKER
 actor "ExportWorker" as WORKER <<sistema>>
 actor "ExportJob" as JOB <<sistema>>
 actor "InternalMailbox" as MB <<sistema>>
 actor "PIIScanner" as PII <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Auditoria\n(async)" as UC_AUD_03
   usecase "Validar formato\n(csv|json)" as VALIDAR_FORMATO
   usecase "Verificar\ninclude_archive (>90d)" as VERIFY_ARCHIVE
   usecase "Crear ExportJob\n(202 + job_id)" as CREATE_JOB
   usecase "Generar archivo\n(workers)" as GENERAR
   usecase "Escanear PII\nantes de write" as ESCANEAR_PII
   usecase "Persistir archivo\nen storage" as PERSIST_FILE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "Emitir AuditEvent\nAUDIT_EXPORTED (P-39)" as AUDIT
 }

 INVOKER --> UC_AUD_03
 UC_AUD_03 ..> VALIDAR_FORMATO : <<include>>
 UC_AUD_03 ..> VERIFY_ARCHIVE : <<include>>
 UC_AUD_03 ..> CREATE_JOB : <<include>>
 CREATE_JOB ..> GENERAR : <<include>>
 GENERAR ..> ESCANEAR_PII : <<include>>
 GENERAR ..> PERSIST_FILE : <<include>>
 GENERAR ..> NOTIFICAR : <<include>>
 GENERAR ..> AUDIT : <<include>>

 CREATE_JOB --> JOB
 GENERAR --> WORKER
 ESCANEAR_PII --> PII
 NOTIFICAR --> MB
 AUDIT --> AS

 note bottom of UC_AUD_03
   Async — devuelve 202 + job_id.
   Cliente consulta resultado via
   InternalMailbox cuando worker termina.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-026 sin PII en archivos.
 end note

 note bottom of AUDIT
   P-39 audit reforzado: archivo
   exportado se trata como evento
   sensible. Meta-audit del export
   incluye hash del archivo.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura de eventos exportados.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo con read-replica usado por ExportWorker.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   entidad ExportJob (state, format, period, archive flag).
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async que genera el archivo.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   componente que detecta PII antes de write a archivo.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon interno donde se notifica completacion.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent AUDIT_EXPORTED (P-39 reforzado).
