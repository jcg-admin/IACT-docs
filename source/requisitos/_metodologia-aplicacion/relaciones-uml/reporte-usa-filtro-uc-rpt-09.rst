10.2 Reporte usa Filtro (UC_RPT_09)
-----------------------------------

.. uml::

   @startuml

   class Report {
     + generate(filters : Filter) : Report
   }
   class Filter

   Report ..> Filter : <<uses>>
   note right of Report
     Report recibe Filter como
     parámetro de generate(). Es
     dependencia, no composición:
     el Filter existe
     independientemente del
     Report.
   end note
   @enduml
