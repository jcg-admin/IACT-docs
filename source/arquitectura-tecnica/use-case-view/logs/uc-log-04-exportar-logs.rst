.. meta::
 :artefacto: AT_UC_LOG_04_USECASE
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

.. _at_uc_log_04_exportar_logs:

============================================================
UC_LOG_04 — Exportar Logs (async)
============================================================

Genera archivo (jsonl/csv) con ApplicationLogs para entrega via mailbox.
``export_logs`` async — devuelve 202 + job_id; worker procesa.
Patron consistente con UC_AUD_03.

.. uml::
 :caption: UC_LOG_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "export_logs" as export_logs
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>
 actor "ExportWorker" as ExportWorker <<sistema>>
 actor "ApplicationLog" as ApplicationLog <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs (async)" as UC_LOG_04
   usecase "Verificar\nexport_logs" as VERIFICAR_AGR
   usecase "Validar formato\n(jsonl | csv)" as VALIDAR_FORMATO
   usecase "Verificar\ninclude_archive" as VERIFY_ARCHIVE
   usecase "Crear ExportJob\n(202 + job_id)" as CREAR_JOB
   usecase "Generar archivo" as GENERAR
   usecase "Persistir + upload" as PERSIST_FILE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
 }

 export_logs --> UC_LOG_04

 UC_LOG_04 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_04 ..> VALIDAR_FORMATO : <<include>>
 UC_LOG_04 ..> VERIFY_ARCHIVE : <<include>>
 UC_LOG_04 ..> CREAR_JOB : <<include>>
 CREAR_JOB ..> GENERAR : <<include>>
 GENERAR ..> PERSIST_FILE : <<include>>
 GENERAR ..> NOTIFICAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 CREAR_JOB --> ExportJob
 GENERAR --> ExportWorker
 GENERAR --> ApplicationLog
 NOTIFICAR --> InternalMailbox

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   fuente exportada.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   ExportJob con format + archive flag.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica completacion.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   ExportFormatStrategy + RetryPolicyStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-04/index` —
   spec textual.
