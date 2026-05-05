Asociaciones
============

Otro acontecimiento común es que **los objetos se relacionan
entre sí de alguna forma**.

La asociación "encendido" es en **una sola dirección (una vía)**:
usted enciende la televisión.

.. uml::

   @startuml

   class Persona
   class Television
   Persona --> Television : enciende
   @enduml

Hay otras asociaciones que son en **dos direcciones**, como
"casamiento".

En ocasiones, un objeto podría asociarse con otro en más de una
forma. Si usted y su colaborador son amigos, ello servirá de
ejemplo. Usted tendría una asociación "es amigo de", así como
"es colaborador de".

.. uml::

   @startuml

   class Persona
   Persona "1" -- "1" Persona : es amigo de
   Persona "1" -- "1" Persona : es colaborador de
   @enduml

**Una clase se puede asociar con más de una clase distinta.** Una
persona puede viajar en automóvil, pero también puede hacerlo en
autobús.

.. uml::

   @startuml

   class Persona
   class Automovil
   class Autobus
   Persona -- Automovil : viaja en
   Persona -- Autobus   : viaja en
   @enduml
