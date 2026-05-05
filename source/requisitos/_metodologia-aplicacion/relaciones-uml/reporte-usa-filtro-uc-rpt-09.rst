10.2 Reporte usa Filtro (UC_RPT_09)
-----------------------------------

.. uml::

   @startuml

   class Reporte {
     + generar(filtros : Filtro) : Reporte
   }
   class Filtro

   Reporte ..> Filtro : <<usa>>
   note right of Reporte
     Reporte recibe Filtro como
     parámetro de generar(). Es
     dependencia, no composición:
     el Filtro existe
     independientemente del
     Reporte.
   end note
   @enduml
