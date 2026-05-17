Ejemplo Streamy completo con multiplicidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reproducción del modelo cerrado del libro:

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

   Title "1..*" -- "1..*" Genre : is associated with
   Title "1" *-- "0..*" Season : has
   Title "1" *-- "0..*" Review : has
   Title "1..*" o-- "0..*" Actor : has
   Season "1" *-- "0..*" Review : has
   Season "1" *-- "1..*" Episode : has
   Episode "1" *-- "0..*" Review : has
   Viewer "0..*" --> "0..*" Title : watches

   TVShow --|> Title : implements
   Short --|> Title : implements
   Film --|> Title : implements
   @enduml

Cada cardinalidad refleja una decisión de modelado
explícita: un título tiene **al menos un** género, puede
tener **0 a muchas** temporadas,**al menos un** actor;
una temporada tiene **al menos un** episodio (no existe
temporada vacía); los espectadores y títulos se
relacionan **muchos a muchos**.
