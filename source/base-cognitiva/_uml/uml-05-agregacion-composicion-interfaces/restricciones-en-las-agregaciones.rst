Restricciones en las agregaciones
---------------------------------

El conjunto de componentes posibles en una agregación se
establece dentro de una **relación O**: el componente *u otro*
es parte del todo.

Por ejemplo: una comida consta de **sopa o ensalada**, el plato
fuerte y el postre. Para modelar esto, utilizaría **una
restricción**: la palabra ``O`` dentro de llaves ``{O}`` con una
línea discontinua que conecte las dos líneas que conforman al
todo.

.. uml::

   @startuml

   class Comida
   class Sopa
   class Ensalada
   class PlatoFuerte
   class Postre

   Comida o-- Sopa
   Comida o-- Ensalada
   Comida o-- PlatoFuerte
   Comida o-- Postre

   Sopa ..> Ensalada : <<{O}>>
   @enduml

----
