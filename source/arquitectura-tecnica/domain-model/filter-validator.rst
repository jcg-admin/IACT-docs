.. meta::
 :artefacto: AT_DM_CLASS_FILTER_VALIDATOR
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

.. _dm_class_filter_validator:

===============
FilterValidator
===============

Valida un ``SavedFilter`` contra el ``Segment`` del usuario
y el ``ColumnCatalog`` del reporte destino. Detecta tres
clases de invalidez:

1. **Estructural** — clausula con operador incompatible
   con el tipo de la columna.
2. **Catálogo** — referencia a columna que no existe
   para el ``ReportType``.
3. **Autorización** — referencia a entidad fuera del
   segmento del usuario (CNST-008).

Marca el filtro como ``is_invalid`` si alguna validación
falla, con detalle por clausula.

.. uml::
 :caption: Clase FilterValidator — validación estructural
           + catálogo + autorización de SavedFilter.

 @startuml

 class FilterValidator {
   - column_catalog : ColumnCatalog
   - segment_resolver : SegmentResolver
   --
   + validate(filter : SavedFilter, user_id : UUID) : FilterValidationReport
   + validate_structure(clause : FilterClause, column_spec : ColumnSpec) : List<ValidationError>
   + validate_catalog(filter : SavedFilter) : List<ValidationError>
   + validate_authorization(filter : SavedFilter, segment : Segment) : List<ValidationError>
 }

 class FilterValidationReport {
   + ok : Boolean
   + errors_by_clause : Map<Integer, List<ValidationError>>
   --
   + has_errors() : Boolean
   + first_error() : ValidationError
 }

 class ValidationError {
   + code : ErrorCode
   + clause_index : Integer
   + message : String
 }

 enum ErrorCode {
   OPERATOR_TYPE_MISMATCH
   COLUMN_UNKNOWN
   COLUMN_NOT_APPLICABLE
   ENTITY_OUT_OF_SCOPE
   VALUE_INVALID
 }

 class ColumnCatalog
 class SegmentResolver
 class SavedFilter

 FilterValidator "1" o-- "1" ColumnCatalog : reads
 FilterValidator "1" o-- "1" SegmentResolver : reads
 FilterValidator "1" ..> "0..*" SavedFilter : validates
 FilterValidator "1" ..> "0..*" FilterValidationReport : returns
 FilterValidationReport *-- "*" ValidationError
 ValidationError "*" -- "1" ErrorCode

 note right of FilterValidator
   3 capas separadas (estructura,
   catalogo, autorizacion). Permite
   reportar errores agrupados por
   capa al UI.
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index`
  — configurar filtros (validación previa a save).

Relaciones
==========

- Agregación con ``ColumnCatalog`` y ``SegmentResolver``.
- Valida ``SavedFilter``.
- Devuelve ``FilterValidationReport``.
