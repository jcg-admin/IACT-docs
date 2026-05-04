Composiciones
=============

La **composición** es un tipo muy representativo de una
agregación. Cada componente dentro de una composición puede
pertenecer **tan sólo a un todo**.

.. note::

 En comparación con la agregación, los componentes de la
 composición **pertenecen a sólo un todo**.

Por ejemplo: los componentes de una **mesa de café** (la
superficie de la mesa y las patas) establecen una composición.

El símbolo es el mismo que el de una agregación, **excepto que el
rombo está relleno**.

.. uml::

   @startuml

   class MesaCafe
   class Superficie
   class Pata

   MesaCafe *-- "1" Superficie
   MesaCafe *-- "4" Pata
   @enduml

----
