.. meta::
 :artefacto: AT_DM_PATTERN_STRATEGY
 :tipo: Diagrama Arquitectonico — Domain Model — Patron
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: CrossCutting
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_pattern_strategy:

============================
Patron Strategy — Catalogo
============================

.. note:: Scope (v5.6.0)

 Las strategies ``DispatchModeStrategy`` (UC_OPR_03),
 ``HoldMessageStrategy`` (UC_OPR_04) y ``DispositionPromptStrategy``
 (UC_OPR_06) corresponden a UCs de **MOD_Operator** que es modulo
 reservado open-closed (out-of-scope para esta release). Se
 documentan en este catalogo como puntos de extension para activacion
 futura, NO como strategies implementables en v5.6.0. Ver
 :doc:`/requisitos/casos-uso/operator/index`.

El patron **Strategy** encapsula algoritmos intercambiables detras de
una interfaz comun. En IACT se usa para variar comportamiento sin
cambiar el cliente: politicas de notificacion, calculos de KPI,
procedimientos de retry, formatos de export, criterios de routing.

Cada Strategy implementa la misma interfaz; el cliente selecciona la
estrategia en runtime via configuracion, contexto o feature flag.

.. uml::
 :caption: Patron Strategy — interfaz canonica + selecciones.

 @startuml

 interface Strategy<Input, Output> {
   + execute(input : Input) : Output
 }

 class Context<Input, Output> {
   - strategy : Strategy<Input, Output>
   --
   + set_strategy(strategy : Strategy<Input, Output>) : void
   + run(input : Input) : Output
 }

 Context o--> Strategy : usa

 @enduml

Catalogo de implementaciones IACT
==================================

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Strategy
   - Variabilidad
   - Proposito
 * - ``NotifyOnAssignStrategy``
   - canal: mailbox / push / log
   - Variantes de notificacion al asignar AGR (UC_ACC_04)
 * - ``NotifyOnRevokeStrategy``
   - canal: mailbox / push / log
   - Variantes de notificacion al revocar (UC_ACC_02)
 * - ``DispatchModeStrategy``
   - mode: manual / preview / auto
   - Modo de marcado de outbound calls (UC_OPR_03)
 * - ``ExportFormatStrategy``
   - format: csv / jsonl / pdf
   - Formato de export de logs y auditoria
 * - ``RetryPolicyStrategy``
   - politica: linear / exponential / fixed
   - Politica de reintento de pipeline / mailbox / export
 * - ``RoutingStrategy``
   - skill / queue / longest-idle
   - Algoritmo de routing de calls a agents
 * - ``KpiAggregationStrategy``
   - agregacion: sum / avg / p95 / p99
   - Agregacion para metricas en KpiCalculator
 * - ``HoldMessageStrategy``
   - silencio / musica / mensaje informativo
   - Audio reproducido al caller en hold (UC_OPR_04)
 * - ``CallbackOfferStrategy``
   - umbral SLA / hora pico / always
   - Cuando ofrecer callback al caller en cola (UC_CLI_03)
 * - ``DispositionPromptStrategy``
   - obligatoria / opcional / por skill
   - Variantes de captura de disposition (UC_OPR_06)

Trazabilidad a UCs
==================

Strategies consumidas por multiples UCs:

- ``NotifyOnAssignStrategy`` / ``NotifyOnRevokeStrategy`` —
  UC_ACC_01, UC_ACC_02, UC_ACC_04, UC_ACC_08, UC_PERM_03,
  UC_PERM_04 (toda escritura RBAC con notify).
- ``DispatchModeStrategy`` — UC_OPR_03.
- ``ExportFormatStrategy`` — UC_AUD_03, UC_LOG_04.
- ``RetryPolicyStrategy`` — UC_PIP_04, UC_AUD_03 (worker async).
- ``KpiAggregationStrategy`` — UC_RPT_01..04, 12-17 (todos los reports).

Relaciones
==========

- :doc:`internal-mailbox` — destino de NotifyOn*Strategy variants.
- :doc:`call` — afectada por DispatchMode + Routing + HoldMessage.
- :doc:`export-job` — usa ExportFormatStrategy + RetryPolicyStrategy.
- :doc:`metric` / :doc:`bucket` — agregadas via KpiAggregationStrategy.
- :doc:`kpi-calculator` — orquesta KpiAggregationStrategy.
