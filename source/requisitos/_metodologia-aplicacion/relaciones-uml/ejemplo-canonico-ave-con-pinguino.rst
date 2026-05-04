Ejemplo canónico — ``Ave`` con ``Pinguino``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una clase base ``Ave`` con el método ``volar()``. Si
``Pinguino`` hereda de ``Ave`` pero no puede implementar
``volar()`` apropiadamente, hay herencia por limitación —
el pingüino limita una capacidad que se supone debería
tener por ser un ``Ave``.

Diseño incorrecto:

.. uml::

   @startuml
   title Diseno incorrecto — herencia por limitacion

   class Ave {
     # nombre : String
     # peso : Double
     + volar()
     + comer()
     + getNombre()
     + getPeso()
   }

   class Pinguino {
     - velocidadNado : Double
     + volar()
     + nadar()
     + getVelocidadNado()
   }

   Ave <|-- Pinguino
   note right of Pinguino
     volar() no puede
     implementarse correctamente.
     Viola el principio LSP.
   end note
   @enduml

Diseño correcto — interfaces para separar comportamientos:

.. uml::

   @startuml
   title Diseno correcto — interfaces

   class Ave {
     # nombre : String
     # peso : Double
     + comer()
     + getNombre()
     + getPeso()
   }

   interface IAveVoladora {
     + volar()
   }

   interface IAveNadadora {
     + nadar()
   }

   class Aguila {
     - altitudMaxima : Double
     + volar()
     + getAltitudMaxima()
   }

   class Pinguino {
     - velocidadNado : Double
     + nadar()
     + getVelocidadNado()
   }

   Ave <|-- Aguila
   Ave <|-- Pinguino
   IAveVoladora <|.. Aguila
   IAveNadadora <|.. Pinguino

   note left of Ave : Comportamientos comunes
   note right of IAveVoladora : Define vuelo
   note right of IAveNadadora : Define nado
   @enduml

Lectura del diseño correcto:

- ``Ave`` queda con los comportamientos **comunes a todas
  las aves** (``comer``, atributos, getters).
- Las interfaces ``IAveVoladora`` e ``IAveNadadora``
  declaran capacidades específicas.
- ``Aguila`` hereda ``Ave`` **e implementa**
  ``IAveVoladora``.
- ``Pinguino`` hereda ``Ave`` **e implementa**
  ``IAveNadadora``.
- Cada clase implementa **solo las interfaces que tienen
  sentido** para su comportamiento natural.

Ventajas:

- Respeta LSP — ninguna clase oculta operaciones
  heredadas.
- Más flexible — agregar nuevas capacidades mediante
  interfaces.
- Más mantenible — cambios en "volar" solo afectan a
  quienes realmente lo implementan.
- Más extensible — fácil agregar aves con diferentes
  combinaciones de capacidades.
