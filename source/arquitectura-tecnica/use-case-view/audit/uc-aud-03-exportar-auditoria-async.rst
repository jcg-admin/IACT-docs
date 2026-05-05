.. meta::
 :artefacto: AT_UC_AUD_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_aud_03_exportar_auditoria_async:

==========================================
UC_AUD_03 — Exportar Auditoria (async)
==========================================

Genera archivo (CSV/JSON) con AuditEvents para entrega a auditores
externos. Soporta ``include_archive`` (acceso > 90 dias via cold
storage). Operacion async — devuelve 202 + job_id; worker procesa
streaming + sanitize + storage + mailbox notify. P-39 audit
reforzado con hash del archivo.

.. uml::
 :caption: UC_AUD_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "export_audit_log" as export_audit_log
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>
 actor "ExportWorker" as ExportWorker <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "PIIScanner" as PIIScanner <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Auditoria\n(async)\n.. extension points ..\nIncludeArchive\nCancelarJob" as UC_AUD_03
   usecase "Verificar\nexport_audit_log" as VERIFICAR_AGR
   usecase "Validar formato\n(csv | json)" as VALIDAR_FORMATO
   usecase "Validar estimacion\n≤ 5M filas" as VALIDAR_ROWS
   usecase "Validar limite\n5 jobs simultaneos" as VALIDAR_JOBS
   usecase "Crear ExportJob\n(state=queued)" as CREAR_JOB
   usecase "Encolar para Worker" as ENCOLAR
   usecase "Re-check permiso\n(P-64 worker)" as RECHECK_PERMISO
   usecase "Stream query AuditRepo" as STREAM_QUERY
   usecase "Sanitize PII\n(CNST-026)" as SANITIZE
   usecase "Escribir archivo\n+ upload storage" as ESCRIBIR_ARCHIVO
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "Emitir AuditEvent\nAUDIT_EXPORTED + hash\n(P-39 reforzado)" as AUDITAR
   usecase "Cold storage query\n(>90 dias)" as INCLUDE_ARCHIVE
   usecase "Cancelar job\nen queued" as CANCELAR
   usecase "Status check\ndel job" as STATUS_CHECK
 }

 export_audit_log --> UC_AUD_03

 UC_AUD_03 ..> VERIFICAR_AGR : <<include>>
 UC_AUD_03 ..> VALIDAR_FORMATO : <<include>>
 UC_AUD_03 ..> VALIDAR_ROWS : <<include>>
 UC_AUD_03 ..> VALIDAR_JOBS : <<include>>
 UC_AUD_03 ..> CREAR_JOB : <<include>>
 UC_AUD_03 ..> ENCOLAR : <<include>>
 ENCOLAR ..> RECHECK_PERMISO : <<include>>
 RECHECK_PERMISO ..> STREAM_QUERY : <<include>>
 STREAM_QUERY ..> SANITIZE : <<include>>
 SANITIZE ..> ESCRIBIR_ARCHIVO : <<include>>
 ESCRIBIR_ARCHIVO ..> NOTIFICAR : <<include>>
 ESCRIBIR_ARCHIVO ..> AUDITAR : <<include>>
 INCLUDE_ARCHIVE ..> UC_AUD_03 : <<extend>> (IncludeArchive)
 CANCELAR ..> UC_AUD_03 : <<extend>> (CancelarJob)
 STATUS_CHECK ..> UC_AUD_03 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 RECHECK_PERMISO --> AuthorizationGuard
 CREAR_JOB --> ExportJob
 ENCOLAR --> ExportWorker
 STREAM_QUERY --> AuditRepo
 SANITIZE --> PIIScanner
 SANITIZE --> Sanitizer
 NOTIFICAR --> InternalMailbox
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_AUD_03
   Async — devuelve 202 + job_id.
   Cliente consulta resultado via
   InternalMailbox cuando worker termina.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno
   obligatorio. CNST-026 sin PII
   (PIIScanner + Sanitizer).
 end note

 note bottom of AUDITAR
   P-39 audit reforzado: archivo
   exportado se trata como evento
   sensible. AUDIT_EXPORTED incluye
   hash del archivo (integridad).
 end note

 note right of RECHECK_PERMISO
   P-64: el worker re-verifica
   permiso al ejecutar — no
   confiar en check inicial.
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura de eventos exportados.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo con read-replica usado por ExportWorker (streaming).
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   ExportJob con state, format, period, archive flag.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async que genera el archivo.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector de PII.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   sanitizador que reemplaza PII detectada.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon donde se notifica completacion.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item con link al archivo + hash.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica export_audit_log (inicial + re-check P-64).
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AUDIT_EXPORTED (P-39 reforzado).
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   ExportFormatStrategy (csv/json) + RetryPolicyStrategy.

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/audit/uc-aud-03/index` — Parte 1-12.
