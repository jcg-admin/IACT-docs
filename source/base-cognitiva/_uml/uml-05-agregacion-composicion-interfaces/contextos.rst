Contextos
=========

Cuando modele un sistema podrían producirse, con frecuencia,
agrupamientos de clases (agregaciones o composiciones). Es
necesario enfocar su atención en un agrupamiento u otro.

El **diagrama de contexto** proporciona la característica para
modelar dichos agrupamientos. Las composiciones se encuentran en
gran medida en los diagramas de contexto.

Un diagrama de contexto es como **un mapa detallado de alguna
sección de un mapa de mayores dimensiones**. Pueden ser
necesarias varias secciones para capturar toda la información
detallada — y a veces se necesita ver todo el panorama (como si
estuvieras viendo una ciudad desde un helicóptero).

Por ejemplo: un tipo de diagrama de contexto le mostrará la
camisa como un gran rectángulo de clase, con un diagrama anidado
en el interior que muestra cómo los componentes de la camisa
están relacionados entre sí. Éste es un **diagrama de contexto
de composición** (dado que la sola camisa reúne a cada
componente).

En este diagrama de contexto de composición se enfoca la
atención en la camisa y sus componentes:

.. uml::

   @startuml

   package "Camisa (composición)" {
     class Cuerpo
     class Cuello
     class Manga
     class Boton
     class Ojal
     class Puno

     Cuerpo *-- Cuello
     Cuerpo *-- "2" Manga
     Cuerpo *-- "1..*" Boton
     Cuerpo *-- "1..*" Ojal
     Manga *-- Puno
   }
   @enduml

Un componente, por sí solo, no tiene un propósito; para que lo
tenga debe tener cierto tipo de componentes — **sólo y sólo si
tiene todos los componentes, tiene propósito**. Eso es
composición.

.. note::

 El diagrama de contexto de composición enfoca la atención en
 los **componentes que pertenecen a un todo**.

A veces es necesario ampliar el ámbito. Por ejemplo: la camisa en
el contexto del guardarropa y de algún atuendo. El contexto
cambia a un todo más general, para ver cómo se relaciona en
diferentes ámbitos.

Para conocer todo el ámbito es necesario un **diagrama de
contexto del sistema**. En el ejemplo, mostrar la forma en que
la clase ``Camisa`` se conecta con las clases ``Guardarropa`` y
``Atuendo``:

.. uml::

   @startuml

   class Guardarropa
   class Atuendo
   class Camisa
   class Pantalon
   class Zapatos

   Guardarropa o-- "0..*" Camisa
   Guardarropa o-- "0..*" Pantalon
   Guardarropa o-- "0..*" Zapatos
   Atuendo "1" o-- "1" Camisa
   Atuendo "1" o-- "1" Pantalon
   Atuendo "1" o-- "1" Zapatos
   @enduml
