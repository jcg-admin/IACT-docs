.. meta::
 :artefacto: AT_DM_CLASS_COLUMN_CATALOG
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_column_catalog:

=============
ColumnCatalog
=============

Catálogo determinístico de columnas disponibles por tipo
de reporte (``ReportType``). Es la fuente de verdad para
``SavedView`` y ``FilterValidator`` al verificar que una
columna referenciada existe y es aplicable al reporte
solicitado.

Catalog-driven: las definiciones de columnas viven en
configuración, no en código. Esto permite agregar
columnas sin redeploy.

.. uml::
 :caption: Clase ColumnCatalog — catálogo de columnas
           disponibles indexado por ReportType.

 @startuml

 class ColumnCatalog {
   - columns_by_report : Map<ReportType, List<ColumnSpec>>
   --
   + list_for(report_type : ReportType) : List<ColumnSpec>
   + exists(column_id : String, report_type : ReportType) : Boolean
   + get(column_id : String, report_type : ReportType) : ColumnSpec
   + reload() : void
 }

 class ColumnSpec {
   + column_id : String
   + display_name : String
   + data_type : ColumnDataType
   + is_filterable : Boolean
   + is_groupable : Boolean
   + is_sortable : Boolean
   + default_visible : Boolean
 }

 enum ColumnDataType {
   STRING
   INTEGER
   DOUBLE
   DATETIME
   BOOLEAN
   PERCENTAGE
   DURATION
 }

 enum ReportType {
   DASHBOARD
   REALTIME
   HISTORICAL
   AGENT
   QUEUE
   CAMPAIGN
   TRANSFER
   IVR
   UNIQUE_CLIENTS
 }

 ColumnCatalog ..> ColumnSpec : returns
 ColumnSpec -- ColumnDataType
 ColumnCatalog -- ReportType

 note right of ColumnCatalog
   reload() permite recargar catalogo
   sin reiniciar el proceso (hot
   config update).
 end note

 @enduml

Trazabilidad a UCs
==================

Consumido indirectamente por todos los UCs que listan o
exportan reportes:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-04/index` —
  exportación valida columnas.
- :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index` —
  filtros validan columnas referenciadas.
- :doc:`/requisitos/casos-uso/reports/uc-rpt-10/index` —
  guardar vista valida columnas.

Relaciones
==========

- Devuelve ``ColumnSpec`` (consultas).
- Asociado con ``ReportType`` (clave del catálogo).
