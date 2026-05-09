.. meta::
 :artefacto: AT_IMPL_SEQ_REPORTS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_reports:

============================================================
Implementation View — MOD_Reports: Patron de Interaccion
============================================================

Secuencia para "consultar reporte de centros de transferencia"
(UC_RPT_01) — el camino sincronos mas comun. Lecturas
agregadas via ``cursor.callproc`` sobre los SPs ``sp_rpt_*``.

.. uml::
 :caption: MOD_Reports impl seq — view → service → SP runner.

 @startuml

 actor User
 participant "ReportView\n(APIView)" as View <<api>>
 participant "ReportSerializer" as Serializer <<serializer>>
 participant "ReportService" as Service <<service>>
 participant "SPRunner" as SP <<service>>
 database MariaDB

 User -> View : GET /api/v1/reports/centros-transferencia/?quarter=Q02_26
 activate View

 View -> View : permission_classes\n[function_perm("view_report_X")]

 View -> Serializer : .params\n.is_valid(...)
 Serializer --> View : {quarter: "Q02_26"}

 View -> Service : centros_transferencia(quarter)
 activate Service

 Service -> SP : callproc('sp_rpt_centros_transferencia', [quarter])
 activate SP
 note right of SP
   SPRunner gestiona:
   - cursor.callproc con timeout
   - mapeo cursor.description -> dict
   - error wrapping
 end note
 SP -> MariaDB : CALL sp_rpt_centros_transferencia('Q02_26')
 MariaDB --> SP : result-set
 SP --> Service : list[dict]
 deactivate SP

 Service --> View : ReportDTO(quarter, rows)
 deactivate Service

 View --> User : HTTP 200 + JSON
 deactivate View

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/reports/api/views.py: 7 viewsets sp_rpt_*``
 * - Serializer
   - ``apps/reports/api/serializers.py: ReportQuerySerializer``
 * - Service
   - ``apps/reports/services/report_service.py``
 * - SP runner
   - ``apps/reports/services/sp_runner.py``
 * - Async export
   - ``apps/reports/services/export_service.py`` —
     ver :doc:`async-export-worker-pattern`

Invariantes de implementacion
==============================

- **I-IMPL-RPT-01:** las views de reporte son **read-only**.
  Sin ``POST/PUT/DELETE``.
- **I-IMPL-RPT-02:** ningun endpoint de reporte hace scan a
  ``tbl_historico_*``. Todos consumen ``base_ivr_*`` via
  los ``sp_rpt_*``.
- **I-IMPL-RPT-03:** el ``SPRunner`` valida que el ``quarter``
  matchea ``^Q0[1-4]_\d{2}$`` antes de ``callproc`` —
  defensa en profundidad ante un Serializer mal configurado.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`async-export-worker-pattern` — patron de export
   asincrono cuando el resultado es grande.
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/report-procedures` —
   spec de los SPs invocados.
 - :doc:`/arquitectura-tecnica/design-view/reports/async-export-flow` —
   flujo en DesignView.
