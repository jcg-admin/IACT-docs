Qué es un diagrama de colaboraciones
====================================

Mientras que en un diagrama de objetos se muestran a los objetos
como tales y sus relaciones, el diagrama de colaboraciones
**muestra los mensajes** que se envían los objetos entre sí. Es
una **extensión** del diagrama de objetos.

Para representar un mensaje, dibujará una **flecha** cerca de la
línea de asociación entre dos objetos; esta flecha apunta al
objeto receptor. El tipo de mensaje se mostrará en una etiqueta
cerca de la flecha; **el mensaje le indicará al objeto receptor
que ejecute una de sus operaciones**. El mensaje finalizará con
un par de paréntesis, dentro de los cuales colocará los
parámetros (en caso de haber alguno).

Se podrá representar la información de secuencia agregando una
**cifra** a la etiqueta del mensaje, correspondiente a la
secuencia propia del mensaje. La cifra y el mensaje se separan
mediante dos puntos (``:``).

.. uml::

   @startuml
   allowmixing

   actor Actor
   object ":ObjetoA" as A
   object ":ObjetoB" as B
   Actor -> A : iniciar
   A -> B   : "1: operacion(parametro)"
   B -> A   : "2: respuesta()"
   @enduml

----
