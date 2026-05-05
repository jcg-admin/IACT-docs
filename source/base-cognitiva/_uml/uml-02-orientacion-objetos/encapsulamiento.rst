Encapsulamiento
===============

La esencia del encapsulamiento (o encapsulación) es que cuando un
objeto trae consigo su funcionalidad, esta última **se oculta**.

Por lo general, la mayoría de la gente que ve la televisión no
sabe o no se preocupa de la complejidad electrónica que hay
detrás de la pantalla. La televisión hace lo que tiene que hacer
sin mostrarnos el proceso necesario para ello.

.. uml::

   @startuml

   class Television {
     - circuitos : Hardware
     - antena : Antena
     - decodificador : Decoder
     --
     + encender()
     + apagar()
     + cambiarCanal(n)
     + ajustarVolumen(n)
   }
   note right of Television
     La complejidad interna
     (circuitos, decodificador,
     antena) está oculta del
     mundo exterior.
   end note
   @enduml

El encapsulamiento permite **reducir el potencial de errores** que
pudieran ocurrir.

En un sistema que consta de objetos, éstos dependen unos de otros
en diversas formas. Si uno de ellos falla y los especialistas de
software tienen que modificarlo de alguna forma, **el ocultar
sus operaciones de otros objetos significará que tal vez no será
necesario modificar los demás objetos**.

El monitor de su computadora, en cierto sentido, oculta sus
operaciones de la CPU. Si algo falla en su monitor, lo reparará o
lo reemplazará; es muy probable que no tenga que reparar o
reemplazar la CPU al mismo tiempo.

Un **objeto oculta lo que hace a otros objetos y al mundo
exterior**, por lo cual al encapsulamiento también se le conoce
como **ocultamiento de la información**.

Un objeto tiene que presentar un "rostro" al mundo exterior para
poder iniciar sus operaciones. Los botones y perillas de la
televisión y de la lavadora se conocen como **interfaces**.

.. note::

 Cuando mencionamos *rostro*, nos referimos a lo que podemos
 "tocar" o acceder para interactuar con la funcionalidad de los
 objetos. Esto es una **interfaz**.
