Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Title o-- Actor

Diferencias visuales con composición:

- Composición — diamante **relleno** (``*--``).
- Agregación — diamante **vacío** (``o--``).

Aplicado al ejemplo Streamy completo:

.. uml::

   @startuml
   class Title
   class Genre
   class Season
   class Episode
   class Review
   class Actor

   Title -- Genre
   Title *-- Season
   Title *-- Review
   Title o-- Actor
   Season *-- Episode
   @enduml
