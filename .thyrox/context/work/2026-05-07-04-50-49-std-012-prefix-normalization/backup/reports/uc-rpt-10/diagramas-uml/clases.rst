8.3 Clases
==========

.. uml::

 @startuml
 class SavedView {
   id, name, report_type,
   filters, columns, chart_config
 }
 class ColumnCatalog {
   list_for(report_type)
   exists(col_id, report_type)
 }
 SavedView -- ColumnCatalog
 @enduml

