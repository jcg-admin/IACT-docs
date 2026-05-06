Sintaxis PlantUML mínima
~~~~~~~~~~~~~~~~~~~~~~~~

En PlantUML, declarar dos entidades y una asociación es
casi tan simple como en Mermaid:

.. uml::

   @startuml
   class Call
   class Segment
   Call -- Segment
   @enduml

Análisis del fragmento:

- ``@startuml`` / ``@enduml`` — delimitan el bloque
  PlantUML (equivalente al ``classDiagram`` de Mermaid
  como declaración de tipo).
- ``class Llamada`` y ``class Segmento`` — declaran las
  dos entidades.
- ``Llamada -- Segmento`` — el ``--`` indica una
  **asociación** simple (sin dirección, sin
  multiplicidad explícita).

Cuando cada entidad mantiene una referencia a la otra y
ninguna es parte estructural de la otra, la relación
correcta es **asociación** — la misma noción del libro
("each entity is going to hold a reference to the
other"). El detalle completo de la asociación está en
§ 2 de :doc:`/requisitos/_metodologia-aplicacion/relaciones-uml/index`.
