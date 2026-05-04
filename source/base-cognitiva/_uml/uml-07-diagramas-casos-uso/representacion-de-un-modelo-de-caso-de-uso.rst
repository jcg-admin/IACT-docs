Representación de un modelo de caso de uso
==========================================

Un actor es quien **inicia** un caso de uso, y otro actor
(posiblemente el que inició, pero no necesariamente) es quien
**recibe** algo de valor de él. La representación gráfica es
directa: una **elipse** representa a un caso de uso y una
**figura agregada** (stick figure) representa a un actor.

El actor que **inicia** se encuentra a la izquierda del caso de
uso, y el que **recibe** a la derecha. El nombre del actor
aparece justo debajo de él; el nombre del caso de uso aparecerá
ya sea dentro de la elipse o justo debajo de ella.

En UML una **línea asociativa** conecta a un actor con el caso
de uso, y representa la comunicación entre ambos.

Al analizar los casos de uso se mostrará los **confines** entre
el sistema y el mundo exterior. Generalmente, los actores están
**fuera** del sistema, mientras que los casos de uso están
**dentro** de él.

Se utiliza un **rectángulo** (con el nombre del sistema dentro)
para representar el confín del sistema; el rectángulo envuelve a
los casos de uso. Los actores, casos de uso y líneas de
interconexión componen un **modelo de caso de uso**.

.. uml::

   @startuml

   left to right direction
   actor "ActorIniciador" as A
   actor "ActorBeneficiario" as B
   rectangle "Sistema" {
     usecase "Caso de uso" as UC
   }
   A --> UC
   UC --> B
   @enduml

----
