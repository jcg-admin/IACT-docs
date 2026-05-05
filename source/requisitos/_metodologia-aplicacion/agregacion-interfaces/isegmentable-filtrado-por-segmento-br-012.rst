5.3 ``ISegmentable`` — filtrado por segmento (BR_012)
-----------------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface ISegmentable <<interface>> {
     + aplicarFiltroSegmento(s : SegmentoDatos)
     + perteneceA(s : SegmentoDatos) : Boolean
   }

   class Llamada
   class Reporte
   class Alerta
   class EventoAuditoria

   Llamada ..|> ISegmentable
   Reporte ..|> ISegmentable
   Alerta ..|> ISegmentable
   EventoAuditoria ..|> ISegmentable

   note right of ISegmentable
     Toda entidad consultada por
     un usuario operativo debe
     filtrarse por su segmento
     (BR_012). El contrato lo
     uniforma.
   end note
   @enduml
