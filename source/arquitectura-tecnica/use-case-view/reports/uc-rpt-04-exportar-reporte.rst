.. meta::
 :artefacto: AT_UC_RPT_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_rpt_04_exportar_reporte:

============================================================
UC_RPT_04 — Exportar Reporte (async)
============================================================

Genera CSV de un reporte filtrado con period + filtros aplicados.
``export_csv`` async — devuelve 202 + job_id; ExportWorker procesa.
P-64 re-check permiso en worker. CNST-026 sin PII.

.. uml::
 :caption: UC_RPT_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "export_csv" as export_csv
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>
 actor "ExportWorker" as ExportWorker <<sistema>>
 actor "PIIScanner" as PIIScanner <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_04\nExportar Reporte\n(async CSV)" as UC_RPT_04
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nexport_csv" as VERIFICAR_AGR
   usecase "Crear ExportJob\n(202 + job_id)" as CREAR_JOB
   usecase "Re-check permiso\n(P-64 worker)" as RECHECK
   usecase "Stream query +\nrender CSV" as RENDER
   usecase "Sanitize PII" as SANITIZE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
 }

 export_csv --> UC_RPT_04

 UC_RPT_04 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_04 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_04 ..> CREAR_JOB : <<include>>
 CREAR_JOB ..> RECHECK : <<include>>
 RECHECK ..> RENDER : <<include>>
 RENDER ..> SANITIZE : <<include>>
 SANITIZE ..> NOTIFICAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 CREAR_JOB --> ExportJob
 RECHECK --> AuthorizationGuard
 RENDER --> ExportWorker
 SANITIZE --> PIIScanner
 NOTIFICAR --> InternalMailbox

 note bottom of RECHECK
   P-64: worker re-verifica permiso
   al ejecutar — no confiar en check
   inicial (puede haber cambiado).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   ExportJob.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   sanitize PII.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   ExportFormatStrategy + RetryPolicyStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica + re-check.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-04/index` —
   spec textual.
