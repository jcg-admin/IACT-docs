Notas adjuntas
==============

Por encima y debajo de los atributos, operaciones,
responsabilidades y restricciones, puede **agregar mayor
información a una clase en la figura de notas adjuntas**. Una
nota puede contener tanto una imagen como texto.

Estas notas deben servir solo para algo específico, y no para
dar detalle de lo que hace la clase. Un ejemplo: que se tengan
ciertas reglas ya establecidas para la creación de un atributo.

.. uml::

   @startuml

   class Lavadora {
     numeroSerie : String
     marca : String
     capacidad : Float
   }
   note right of Lavadora
     Para la generación de números de serie,
     consulte la **norma gubernamental
     NOM-XXX-2026** que define el formato
     y el procedimiento de asignación.
   end note
   @enduml
