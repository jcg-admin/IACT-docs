.. meta::
 :artefacto: AT_DM_CLASS_CAMPAIGN_REPORT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_campaign_report_service:

======================
CampaignReportService
======================

Servicio de aplicacion que genera reportes de performance
de campaigns (asistencia, conversion, abandono, etc.). Sigue
el patron arquitectonico de los otros ``*ReportService`` del
BC Reports — extiende ``BaseReportService`` heredando
filtrado por ``SegmentScope``, paginacion, y emision de
audit-event.

Es invocado desde ``uc-rpt-14`` por usuarios con codename
``view_reports``. Lee agregaciones diarias de
``CampaignDailyStatRepo`` y compone metricas con
``KPICalculator``.

.. uml::
 :caption: CampaignReportService — generacion de reporte
           de performance de campaigns.

 @startuml

 class CampaignReportService {
   --
   + list(filters : CampaignFilters, \
           period : DateRange, \
           actor_scope : SegmentScope) : List<CampaignReportRow>
   + detail(campaign_id : UUID, \
             actor_scope : SegmentScope) : CampaignDetail
 }

 class BaseReportService
 class CampaignDailyStatRepo
 class KPICalculator
 class SegmentResolver
 class CampaignReportRow
 class CampaignDetail

 CampaignReportService --|> BaseReportService
 CampaignReportService --> CampaignDailyStatRepo : reads
 CampaignReportService --> KPICalculator : computes
 CampaignReportService --> SegmentResolver : filters by scope
 CampaignReportService ..> CampaignReportRow : returns
 CampaignReportService ..> CampaignDetail : returns

 @enduml

Operaciones principales
=======================

- ``list(filters, period, actor_scope)`` — devuelve la lista
  paginada de campaigns con metricas agregadas en el periodo.
- ``detail(campaign_id, actor_scope)`` — devuelve el detalle
  completo (timeseries diarias, breakdown por agente, etc.)
  de una campaign especifica.

Restricciones aplicables
========================

- **CNST-018** — todos los resultados se filtran por el
  ``SegmentScope`` del usuario.
- **CNST-025** — cada query se audita.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index` —
  reporte de performance de campaigns.

Relaciones
==========

- Hereda de ``BaseReportService``.
- Lee de ``CampaignDailyStatRepo`` (agregaciones diarias).
- Computa con ``KPICalculator``.
- Filtra con ``SegmentResolver``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/base-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/campaign-daily-stat-repo`
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
