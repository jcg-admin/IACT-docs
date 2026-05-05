4.2 ``exportar()`` polimórfico per CNST_019/020
-----------------------------------------------

.. uml::

   @startuml

   abstract class Exportador {
     - reporte : Reporte
     + exportar() : Archivo
   }

   class ExportadorCSV {
     + exportar() : Archivo
   }
   class ExportadorExcel {
     + exportar() : Archivo
   }
   class ExportadorPDF {
     + exportar() : Archivo
   }

   Exportador <|-- ExportadorCSV
   Exportador <|-- ExportadorExcel
   Exportador <|-- ExportadorPDF

   note right of Exportador
     CNST_019 — exportaciones
     asíncronas para sets > 10k filas.
     CNST_020 — throttling distinto
     por formato:
       CSV   100k/10 día
       Excel  50k/5 día
       PDF    10k/3 día
   end note
   @enduml
