Vínculos
========

Un **vínculo** es la **instancia de una asociación**. Conecta a
los **objetos** en lugar de las clases.

Así como un objeto es una instancia de una clase, una asociación
también cuenta con instancias.

Si imaginamos a un jugador específico que juega para un equipo
específico, la relación *"participa en"* se conocerá como
**vínculo**. El vínculo se representará como una línea que conecta
a dos objetos. Tal como tuvo que subrayar el nombre de un objeto,
deberá subrayar el nombre de un vínculo.

.. uml::

   @startuml

   object "michael : Jugador" as M
   object "bulls : Equipo" as B
   M -- B : participa en
   @enduml
