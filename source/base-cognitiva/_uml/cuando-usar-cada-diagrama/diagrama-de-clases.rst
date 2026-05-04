1. Diagrama de clases
---------------------

**Propósito:** estructura estática del sistema (las cosas que
existen). Atributos + operaciones + relaciones entre clases.

**Cuándo usarlo:** cuando necesites mostrar qué clases existen
y cómo se estructuran.

**Lección completa:**
:doc:`uml-03-uso-orientacion-objetos`,
:doc:`uml-04-uso-relaciones`,
:doc:`uml-05-agregacion-composicion-interfaces`.

.. uml::

   @startuml

   class Lavadora {
     - marca : String
     - modelo : String
     - capacidad : Float
     + agregarRopa()
     + activarse()
     + sacarRopa()
   }
   @enduml

----
