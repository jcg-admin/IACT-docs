.. meta::
 :artefacto: AT_UC_RPT_07_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_rpt_07_programar_reporte:

==============================
UC_RPT_07 — Programar Reporte
==============================

Crea ScheduledReport recurrente (diario, semanal, mensual). Cada run
del Planificador ejecuta export con filtros guardados y entrega
via mailbox.
``schedule_report``.

.. uml::
 :caption: UC_RPT_07 — actores y casos asociados.

 @startuml

 left to right direction

 actor "schedule_report" as schedule_report
 actor "Planificador" as Planificador <<sistema>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ScheduledReportRepo" as ScheduledReportRepo <<sistema>>
 actor "ScheduledReport" as ScheduledReport <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_07\nProgramar Reporte" as UC_RPT_07
   usecase "Verificar\nschedule_report" as VERIFICAR_AGR
   usecase "Validar period\n+ filtros + format" as VALIDAR
   usecase "Persistir ScheduledReport" as PERSISTIR
   usecase "Run programado\n(crear ExportJob)" as RUN_CRON
 }

 schedule_report --> UC_RPT_07
 Planificador --> RUN_CRON

 UC_RPT_07 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_07 ..> VALIDAR : <<include>>
 UC_RPT_07 ..> PERSISTIR : <<include>>
 RUN_CRON ..> UC_RPT_07 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 PERSISTIR --> ScheduledReportRepo
 PERSISTIR --> ScheduledReport
 RUN_CRON --> ExportJob

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report` —
   ScheduledReport persistido.
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   creado por cada run.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-07/index` —
   spec textual.
