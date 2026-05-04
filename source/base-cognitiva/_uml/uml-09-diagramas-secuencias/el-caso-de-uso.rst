El caso de uso
--------------

¿Qué es exactamente lo que representa un diagrama de secuencias?

Muestra las interacciones de objetos que se realizan durante un
escenario sencillo. Este escenario podría ser parte de un caso
de uso llamado *"Ejecutar la opresión de una tecla"*.

Representar gráficamente las interacciones del sistema en el
caso de uso, el diagrama de secuencias **delineará** el caso de
uso dentro del sistema.

.. uml::

   @startuml

   left to right direction
   actor Usuario
   rectangle "Sistema" {
     usecase "Ejecutar la opresión\nde una tecla" as UC
   }
   Usuario --> UC
   @enduml

----
