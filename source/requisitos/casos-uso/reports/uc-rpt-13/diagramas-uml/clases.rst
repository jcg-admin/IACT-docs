8.3 Clases
==========

.. uml::

 @startuml
 class AbandonoReportService {
   + get(trimestre, invoker) : ReporteAbandono
 }
 class ServicioReportes {
   + llamadas_abandonadas(trimestre) : list[dict]
 }
 class SegmentResolver {
   + resolve(user_id) : list[str]
 }
 AbandonoReportService --> ServicioReportes
 AbandonoReportService --> SegmentResolver
 @enduml

