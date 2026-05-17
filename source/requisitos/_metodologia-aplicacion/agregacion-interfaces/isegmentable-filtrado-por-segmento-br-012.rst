5.3 ``ISegmentable`` — filtrado por segmento (BR_012)
-----------------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface ISegmentable <<interface>> {
     + applySegmentFilter(s : DataSegment)
     + belongsTo(s : DataSegment) : Boolean
   }

   class Call
   class Report
   class Alert
   class AuditEvent

   Call ..|> ISegmentable
   Report ..|> ISegmentable
   Alert ..|> ISegmentable
   AuditEvent ..|> ISegmentable

   note right of ISegmentable
     Toda entidad consultada por
     un usuario operativo debe
     filtrarse por su segmento
     (BR_012). El contrato lo
     uniforma.
   end note
   @enduml
