2.2 Posicionamiento
-------------------

El **actor que inicia** se ubica a la izquierda; el **caso
de uso** en el centro o a la derecha; el **actor que se
beneficia** a la derecha (puede ser el mismo).

.. uml::

   @startuml

   left to right direction
   actor "Actor\niniciador" as Actor
   actor "Actor\nbeneficiario" as Actor

   rectangle "Sistema" {
     usecase "Caso de uso" as CasoDeUso
   }

   Actor --> CasoDeUso : inicia
   CasoDeUso --> Actor : se beneficia
   @enduml
