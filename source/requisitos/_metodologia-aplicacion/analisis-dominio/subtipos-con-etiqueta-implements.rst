Subtipos con etiqueta ``implements``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado al cluster de reportes IACT
(:doc:`/requisitos/_metodologia-aplicacion/relaciones-uml/index` § 14.1):

.. uml::

   @startuml

   abstract class Reporte
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance

   ReporteVolumen --|> Reporte : implements
   ReporteAbandono --|> Reporte : implements
   ReporteSoDCompliance --|> Reporte : implements
   @enduml

La etiqueta ``implements`` (o ``extends``) hace
explícito para lectores no familiarizados con la
flecha que estamos ante una jerarquía donde ``Reporte``
es el tipo abstracto y los demás son variantes
concretas.
