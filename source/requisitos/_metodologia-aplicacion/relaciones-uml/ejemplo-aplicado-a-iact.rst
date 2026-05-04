Ejemplo aplicado a IACT
~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   abstract class Reporte {
     + generar()
     + exportar(formato)
   }
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance
   Reporte <|-- ReporteVolumen
   Reporte <|-- ReporteAbandono
   Reporte <|-- ReporteSoDCompliance
   @enduml

Cada subclase **mantiene** ``generar()`` y ``exportar()``
y **añade** su lógica específica de cálculo. Ningún
subtipo rompe el contrato del padre.
