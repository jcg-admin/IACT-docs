3. Factory — ReporteFactory
===========================

**Problema.** UC_RPT_* abarca varios tipos (volumen,
abandono, SoD compliance). Cada tipo tiene su propio
agregador, pero comparte la interfaz ``IReporte``.

.. uml::

   @startuml
   interface IReporte {
     + generar() : Resultado
   }
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance
   class ReporteFactory {
     + {static} crear(tipo : str, params) : IReporte
   }
   IReporte <|.. ReporteVolumen
   IReporte <|.. ReporteAbandono
   IReporte <|.. ReporteSoDCompliance
   ReporteFactory ..> IReporte : crea
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.
