9. Strategy — formato de exportación
=====================================

**Problema.** UC_RPT_04 puede entregar CSV, XLSX o JSON. El
algoritmo de serialización cambia, el resto del flujo no.

.. uml::

   @startuml
   interface FormatoExport {
     + serializar(datos) : bytes
   }
   class CSVExport
   class XLSXExport
   class JSONExport
   FormatoExport <|.. CSVExport
   FormatoExport <|.. XLSXExport
   FormatoExport <|.. JSONExport
   class ExportadorReporte {
     - formato : FormatoExport
     + ejecutar(datos)
   }
   ExportadorReporte --> FormatoExport
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.
Agregar un nuevo formato no toca ``ExportadorReporte``,
``rpt_app`` ni el facade — solo se registra una nueva
estrategia.
