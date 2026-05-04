Diagrama de estados
===================

En cualquier momento, un objeto se encuentra en un **estado en
particular**.

Una lavadora podrá estar en la fase de *remojo*, *lavado*,
*enjuague*, *centrifugado* o *apagada*.

El símbolo que está en la parte superior de la figura representa
el **estado inicial** y el de la parte inferior el **estado
final**.

.. uml::

   @startuml

   [*] --> Remojo
   Remojo --> Lavado
   Lavado --> Enjuague
   Enjuague --> Centrifugado
   Centrifugado --> Apagada
   Apagada --> [*]
   @enduml

.. warning::

 **Nota:** Los diagramas de clases y los de objetos representan
 información **estática**. Los diagramas de estados, secuencias,
 actividades y colaboraciones representan información **dinámica**
 (cambio progresivo en el tiempo).

----
