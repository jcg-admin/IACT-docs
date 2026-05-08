1. Diagrama de clases
---------------------

**Propósito:** estructura estática del sistema (las cosas que
existen). Atributos + operaciones + relaciones entre clases.

**Cuándo usarlo:** cuando necesites mostrar qué clases existen
y cómo se estructuran.

**Lección completa:**
:doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index`,
:doc:`/base-cognitiva/_uml/uml-04-uso-relaciones/index`,
:doc:`/base-cognitiva/_uml/uml-05-agregacion-composicion-interfaces/index`.

.. uml::

   @startuml

   class WashingMachine {
     - brand : String
     - model : String
     - capacity : Float
     + addClothes()
     + activate()
     + removeClothes()
   }
   @enduml
