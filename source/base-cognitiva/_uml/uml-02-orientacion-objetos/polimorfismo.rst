Polimorfismo
============

En ocasiones **una operación tiene el mismo nombre en diferentes
clases**. En la orientación a objetos, cada clase "sabe" cómo
realizar tal operación. Esto es el **polimorfismo**.

Una operación puede tener el mismo nombre en diferentes contextos
o clases. El ejemplo de ``abrir`` aplica para muchas cosas: abrir
una puerta, abrir una caja, abrir una ventana — es la misma
acción, pero no se realiza de la misma forma.

.. uml::

   @startuml

   class Puerta {
     + abrir()
   }
   class Caja {
     + abrir()
   }
   class Ventana {
     + abrir()
   }
   note bottom of Puerta : girar perilla\n+ tirar
   note bottom of Caja   : levantar tapa
   note bottom of Ventana: deslizar marco
   @enduml

Este concepto es importante para los **desarrolladores** de
software: tienen que crear el software que **implemente tales
métodos** en los programas, y deben estar conscientes de
diferencias importantes entre las operaciones que pudieran tener
el mismo nombre.

El polimorfismo también es importante para los **modeladores**:
les **permite hablar con el cliente** (quien está familiarizado
con la sección del mundo que será modelada) en las propias
palabras y terminología del cliente. Las palabras y terminología
del cliente nos conducen a **palabras de acción** (como ``abrir``)
que pueden tener más de un significado.

El polimorfismo permite al modelador mantener tal terminología
sin tener que crear palabras artificiales para sustentar una
unicidad innecesaria de los términos.

----
