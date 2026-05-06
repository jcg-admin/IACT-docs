3. Factory — ReporteFactory
===========================

**Problema.** UC_RPT_* abarca varios tipos (volumen,
abandono, SoD compliance). Cada tipo tiene su propio
agregador, pero comparte la interfaz ``IReporte``.

.. uml::

   @startuml
   interface IReport {
     + generate() : Result
   }
   class VolumeReport
   class AbandonmentReport
   class SoDComplianceReport
   class ReportFactory {
     + {static} create(type : str, params) : IReport
   }
   IReport <|.. VolumeReport
   IReport <|.. AbandonmentReport
   IReport <|.. SoDComplianceReport
   ReportFactory ..> IReport : creates
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.
