Ejemplo canónico — figuras geométricas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml

   abstract class Shape {
     - color : String
     - positionX : int
     - positionY : int
     + calculateArea()
     + calculatePerimeter()
     + draw()
     + move()
   }

   class Circle {
     - radius : double
     + calculateArea()
     + calculatePerimeter()
     + draw()
     + move()
   }

   class Rectangle {
     - base : double
     - height : double
     + calculateArea()
     + calculatePerimeter()
     + draw()
     + move()
   }

   Shape <|-- Circle
   Shape <|-- Rectangle

   note left of Shape : Clase base
   note right of Circle : Especializacion completa
   note right of Rectangle : Especializacion completa
   @enduml

``Circulo`` y ``Rectangulo`` **implementan todas** las
operaciones de ``Figura`` (``calcularArea``,
``calcularPerimetro``, ``dibujar``, ``mover``); ninguna
queda sin implementar ni se desactiva. La especialización
añade los atributos propios (``radio``; ``base``,
``altura``) sin romper el contrato.
