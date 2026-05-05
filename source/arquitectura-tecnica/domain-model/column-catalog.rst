.. meta::
 :artefacto: AT_DM_CLASS_COLUMN_CATALOG
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_column_catalog:

=============
ColumnCatalog
=============

Catalogo de columnas disponibles por tipo de reporte.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ColumnCatalog — stub pendiente de desarrollo.

 @startuml

 class ColumnCatalog {
  + list_for(report_type)
  + exists(col_id, report_type)
 }

 @enduml
