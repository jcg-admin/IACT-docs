.. _uc-rpt-10-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_10 — clases SavedView + ColumnCatalog.

 @startuml

 class SavedView {
   + view_id : UUID
   + name : String
   + report_type : String
   + filters_snapshot : Map
   + columns : List
   + chart_config : Map
   + state : SavedViewState
   + owner_user_id : UUID
 }

 class ColumnCatalog {
   + list_for(report_type) : List
   + exists(col_id, report_type) : Boolean
 }

 SavedView "*" -- "1" ColumnCatalog : validates_against

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-view`.
 - :doc:`/arquitectura-tecnica/domain-model/column-catalog`.
