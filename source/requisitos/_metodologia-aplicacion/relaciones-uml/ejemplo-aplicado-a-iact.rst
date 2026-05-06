Ejemplo aplicado a IACT
~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   abstract class Report {
     + generate()
     + export(format)
   }
   class VolumeReport
   class AbandonmentReport
   class SoDComplianceReport
   Report <|-- VolumeReport
   Report <|-- AbandonmentReport
   Report <|-- SoDComplianceReport
   @enduml

Cada subclase **mantiene** ``generar()`` y ``exportar()``
y **añade** su lógica específica de cálculo. Ningún
subtipo rompe el contrato del padre.
