.. meta::
 :artefacto: AT_DM_CLASS_ALERT_HISTORY_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_history_service:

====================
AlertHistoryService
====================

Servicio de aplicacion que consulta el historial de alertas
disparadas con agregaciones y percentiles. Distinto de
``AlertService`` (gestion del catalogo de reglas) y de
``AlertRepo`` (persistencia raw): este servicio agrega y
calcula timings consumibles por la UI.

Es invocado desde ``uc-alr-04`` por usuarios con codename
``view_alerts``. Combina lectura de ``AlertRepo`` con
calculo de percentiles via ``TimingCalculator``, y devuelve
un ``AlertHistorySummary`` listo para render.

.. uml::
 :caption: AlertHistoryService — consulta agregada del
           historial de alertas con TTAR/TTAK percentiles.

 @startuml

 class AlertHistoryService {
   --
   + query(filters : AlertFilters, \
            period : DateRange, \
            actor_scope : SegmentScope) : AlertHistorySummary
 }

 class AlertHistorySummary
 class AlertRepo
 class TimingCalculator
 class AuditService

 AlertHistoryService --> AlertRepo : reads raw history
 AlertHistoryService --> TimingCalculator : computes percentiles
 AlertHistoryService --> AlertHistorySummary : returns
 AlertHistoryService --> AuditService : emits read event

 @enduml

Operaciones principales
=======================

- ``query(filters, period, actor_scope)`` — pipeline:

  1. Lee filas crudas de ``AlertRepo.query_history`` con
     filtros + periodo.
  2. Filtra por ``actor_scope`` para respetar el alcance del
     usuario (CNST-018).
  3. Computa percentiles TTAR (Time To Acknowledge) y TTAK
     (Time To Resolve) via ``TimingCalculator``.
  4. Empaqueta en ``AlertHistorySummary``.
  5. Emite evento de auditoria de lectura.

Restricciones aplicables
========================

- **CNST-018** — el resultado siempre se filtra por el
  ``SegmentScope`` del usuario antes de devolverse.
- **CNST-025** — la consulta historica se audita.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index` —
  consulta de historial.

Relaciones
==========

- Lee de ``AlertRepo``.
- Computa con ``TimingCalculator``.
- Devuelve ``AlertHistorySummary``.
- Emite via ``AuditService``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-history-summary`
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
