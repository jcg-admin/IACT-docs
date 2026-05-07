8.3 Clases
==========

.. uml::

 @startuml
 class AbandonmentReportService {
   + get(trimestre, invoker) : ReporteAbandono
 }
 class SegmentResolver {
   + resolve(user_id) : list[str]
 }
 AbandonmentReportService --> SegmentResolver
 @enduml

