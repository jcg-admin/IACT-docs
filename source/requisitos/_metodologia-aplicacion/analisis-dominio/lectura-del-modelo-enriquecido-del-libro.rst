Lectura del modelo enriquecido del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El ejemplo Streamy completo con descripciones e
inheritance + Viewer:

.. uml::

   @startuml

   class Title
   class Genre
   class Season
   class Episode
   class Review
   class Actor
   class Viewer
   class TVShow
   class Short
   class Film

   Title -- Genre : is associated with
   Title *-- Season : has
   Title *-- Review : has
   Title o-- Actor : features
   Season *-- Review : has
   Season *-- Episode : contains
   Episode *-- Review : has
   Viewer --> Title : watches

   TVShow --|> Title : implements
   Short --|> Title : implements
   Film --|> Title : implements
   @enduml

Análisis de las decisiones del modelo:

- **``Title -- Genre : is associated with``** —
  asociación bidireccional. La descripción debe ser
  válida en ambos sentidos: un título *está asociado
  con* un género y un género *está asociado con*
  títulos.
- **``Viewer --> Title : watches``** —
  asociación **direccional**. ``Viewer`` mantiene
  referencia a ``Title``; ``Title`` no necesita
  referencia inversa al espectador. Por eso el
  ``-->`` en lugar del ``--`` bidireccional.
- **``Title *-- Season : has``**,
  **``Title *-- Review : has``**,
  **``Season *-- Episode : contains``** — composición
  con etiqueta descriptiva desde el padre. ``contains``
  es más preciso que ``has`` en este caso.
- **``Title o-- Actor : features``** — agregación con
  etiqueta más rica que ``has``: un título no
  simplemente "tiene" actores; los **presenta**.
- **``TVShow --|> Title : implements``** — generalización
  con etiqueta. ``implements`` o ``extends`` clarifican
  para lectores no familiarizados con la flecha de
  herencia que se trata de una jerarquía.
