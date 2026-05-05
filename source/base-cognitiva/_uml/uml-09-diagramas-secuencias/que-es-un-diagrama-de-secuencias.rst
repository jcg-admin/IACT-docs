Qué es un diagrama de secuencias
================================

El diagrama de secuencias consta de:

- **Objetos** representados del modo usual: rectángulos con
  nombre (subrayado).
- **Mensajes** representados por líneas continuas con una punta
  de flecha.
- **Tiempo** representado como una progresión vertical.

Los objetos se colocan en la parte superior del diagrama de
izquierda a derecha, acomodados de manera que simplifiquen el
diagrama.

La extensión que está debajo (en forma descendente) de cada
objeto es una **línea discontinua** conocida como **la línea de
vida del objeto**.

Junto con la línea se encuentra un pequeño rectángulo conocido
como **activación**, que representa la ejecución de una
operación que realiza el objeto. La longitud del rectángulo se
interpreta como la duración de la activación.

.. uml::

   @startuml

   participant Cliente as C
   participant ":Objeto" as O
   C -> O ++ : mensaje
   ... actividad ...
   return resultado
   @enduml

Un **mensaje** que va de un objeto a otro pasa de la línea de
vida de un objeto a la de otro. Un objeto puede enviarse un
mensaje a sí mismo desde su línea de vida hacia su propia línea
de vida.

El mensaje puede ser **simple**, **sincrónico** o **asincrónico**:

.. list-table::
 :widths: 22 48 30
 :header-rows: 1

 * - Tipo
   - Qué es
   - Punta de flecha
 * - **Simple**
   - Transferencia del control de un objeto a otro.
   - Formada por dos líneas (open arrow ``>``).
 * - **Sincrónico**
   - El emisor esperará la respuesta antes de continuar.
   - Está rellena (filled arrow ``▶``).
 * - **Asincrónico**
   - El emisor no esperará una respuesta antes de continuar.
   - Tiene una sola línea (half open arrow ``>``).

.. uml::

   @startuml

   participant A
   participant B
   A ->  B : mensaje simple
   A ->> B : mensaje asincrónico
   A -> B  : mensaje sincrónico
   B --> A : retorno
   @enduml

En el diagrama se representa al **tiempo** en dirección
vertical: se inicia en la parte superior y avanza hacia la parte
inferior. Un mensaje que esté más cerca de la parte superior
ocurrirá antes que uno cerca de la parte inferior.

El diagrama de secuencias tiene dos dimensiones:

- **Dimensión horizontal:** disposición de los objetos.
- **Dimensión vertical:** paso del tiempo.

.. uml::

   @startuml

   actor Actor
   participant ":ObjetoA" as A
   participant ":ObjetoB" as B
   participant ":ObjetoC" as C

   Actor -> A : iniciar
   activate A
   A -> B : operacion1()
   activate B
   B -> C : operacion2()
   activate C
   C --> B : resultado
   deactivate C
   B --> A : ok
   deactivate B
   deactivate A
   @enduml
