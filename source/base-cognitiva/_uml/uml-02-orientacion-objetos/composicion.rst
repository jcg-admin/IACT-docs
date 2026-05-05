Composición
-----------

Un tipo de agregación **trae consigo una estrecha relación entre
un objeto agregado y sus objetos componentes**. A esto se le
conoce como **composición**.

.. warning::

 **Composición**

 Un objeto más complejo (llamado **compuesto**) se compone de uno
 o más objetos más pequeños (**componentes**). La composición es
 una relación fuerte, en la que los **componentes no tienen
 sentido** por sí solos sin el objeto compuesto. Los componentes
 **dependen completamente** del objeto compuesto. No pueden
 existir de manera independiente fuera de este.

El punto central de la composición es que el componente se
considera como tal sólo como parte del objeto compuesto. El
concepto clave: **la vida del componente está ligada a la vida
del objeto compuesto**.

Por ejemplo: una camisa está compuesta de cuerpo, cuello, mangas,
botones, ojales y puños. Suprima la camisa y el cuello será
inútil.

En ocasiones, un objeto compuesto no tiene el mismo tiempo de
vida que sus propios componentes. Las hojas de un árbol pueden
morir antes que el árbol; si destruye al árbol, también las
hojas morirán.

.. uml::

   @startuml

   class Camisa
   class Cuerpo
   class Cuello
   class Manga
   class Boton
   class Ojal
   class Puno

   Camisa *-- Cuerpo
   Camisa *-- Cuello
   Camisa *-- "2" Manga
   Camisa *-- "1..*" Boton
   Camisa *-- "1..*" Ojal
   Camisa *-- "2" Puno

   class Arbol
   class Hoja
   Arbol *-- "0..*" Hoja
   note right of Hoja
     Las hojas pueden morir
     antes que el árbol;
     si el árbol muere, también
     mueren las hojas.
   end note
   @enduml
