Ejemplo canónico — figuras geométricas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml

   abstract class Figura {
     - color : String
     - posicionX : int
     - posicionY : int
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   class Circulo {
     - radio : double
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   class Rectangulo {
     - base : double
     - altura : double
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   Figura <|-- Circulo
   Figura <|-- Rectangulo

   note left of Figura : Clase base
   note right of Circulo : Especializacion completa
   note right of Rectangulo : Especializacion completa
   @enduml

``Circulo`` y ``Rectangulo`` **implementan todas** las
operaciones de ``Figura`` (``calcularArea``,
``calcularPerimetro``, ``dibujar``, ``mover``); ninguna
queda sin implementar ni se desactiva. La especialización
añade los atributos propios (``radio``; ``base``,
``altura``) sin romper el contrato.
