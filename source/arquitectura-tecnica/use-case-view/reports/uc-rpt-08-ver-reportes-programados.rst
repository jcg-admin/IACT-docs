.. meta::
 :artefacto: AT_UC_RPT_08_USECASE
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

.. _at_uc_rpt_08_ver_reportes_programados:

==============================================
UC_RPT_08 — Ver Reportes Programados
==============================================

Lista ScheduledReport del User con estado, proximo run, ultimo run,
historial de ejecuciones. ``view_reports`` (lectura).

.. uml::
 :caption: UC_RPT_08 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ScheduledReportListService" as ScheduledReportListService <<sistema>>
 actor "ScheduledReportRepo" as ScheduledReportRepo <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_08\nVer Reportes Programados" as UC_RPT_08
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Listar ScheduledReport\ndel User" as LISTAR
   usecase "Mostrar proximo run\n+ ultimo run" as RUNS
   usecase "Historial ExportJob" as HISTORIAL
 }

 view_reports --> UC_RPT_08

 UC_RPT_08 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_08 ..> LISTAR : <<include>>
 UC_RPT_08 ..> RUNS : <<include>>
 UC_RPT_08 ..> HISTORIAL : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 LISTAR --> ScheduledReportListService
 ScheduledReportListService --> ScheduledReportRepo
 HISTORIAL --> ExportJob

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report` —
   entity listada.
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report-list-service` —
   servicio de listado.
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   historial.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-08/index` —
   spec textual.
