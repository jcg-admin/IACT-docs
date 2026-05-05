.. meta::
 :artefacto: AT_DM_CLASS_ALERT_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_repo:

=========
AlertRepo
=========

Repositorio de persistencia y consulta de instancias
``Alert``. Cumple dos responsabilidades complementarias:

1. **Persistir** alertas creadas por el motor cuando una
   ``AlertRule`` matchea (``save``,
   ``update_state``).
2. **Consultar** historial y alertas activas con
   filtros (``find_active``, ``query_history``,
   ``get_by_id``).

La operación de cierre del ciclo de vida (``acknowledge``,
``disable``) NO actualiza valores históricos: cada
transición se persiste como nueva versión de la entidad,
preservando el rastro auditado (CNST-025 indirectamente,
vía ``AuditService``).

.. uml::
 :caption: Clase AlertRepo — persistencia y consulta de
           Alert con state transitions versionadas.

 @startuml

 class AlertRepo {
   - storage_backend : StorageBackend
   --
   + save(alert : Alert) : UUID
   + update_state(alert_id : UUID, new_state : AlertState, \
                  actor_user_id : UUID) : Alert
   + find_active(filters : AlertFilters) : List<Alert>
   + query_history(filters : AlertFilters, \
                    period : DateRange) : QueryResult
   + get_by_id(alert_id : UUID) : Alert
   + count_active(filters : AlertFilters) : Integer
   + count_by_severity(period : DateRange) : Map<Severity, Integer>
 }

 class AlertFilters {
   + rule_id : UUID
   + scope : Scope
   + state : AlertState
   + severity : Severity
   + acknowledged_by : UUID
 }

 class DateRange {
   + from : DateTime
   + to : DateTime
 }

 class QueryResult {
   + alerts : List<Alert>
   + total : Integer
 }

 class Alert
 class AlertState
 class Severity

 AlertRepo ..> Alert : persists/queries
 AlertRepo ..> AlertFilters : queries with
 AlertRepo ..> DateRange : queries with
 AlertRepo ..> QueryResult : returns

 note right of AlertRepo
   Cada transicion de state se persiste
   versionada — preserva trazabilidad.
 end note

 @enduml

Operaciones principales
=======================

- ``save(alert)`` — persiste una nueva alerta producida
  por el evaluador. Devuelve ``alert_id``.
- ``update_state(alert_id, new_state, actor)`` — registra
  transición de estado. Internamente crea registro
  versionado.
- ``find_active(filters)`` — lista alertas en estado
  ``ACTIVE``.
- ``query_history(filters, period)`` — consulta histórica
  con filtros + rango temporal.
- ``count_by_severity(period)`` — agregación útil para el
  dashboard ``SLA`` (UC_RPT_*).

Restricciones aplicables
========================

- **CNST-025** — transiciones se auditan vía
  ``AuditService.emit()`` (responsabilidad del invocante,
  no del repositorio).
- **BR-009** — no hay operación ``delete``; los estados
  finales (``DISABLED``) preservan el registro.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-02/index` —
  ``find_active``.
- :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index` —
  ``update_state`` (acknowledge).
- :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index` —
  ``query_history``.

Relaciones
==========

- Persiste y consulta instancias de ``Alert``.
- Es usado por ``AlertEngine`` (escritura) y por las
  vistas de UI (lectura).
- No conoce a ``AlertRule`` directamente; recibe la
  ``Alert`` ya enlazada a su rule_id.
