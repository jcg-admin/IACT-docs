Diagrama de casos de uso
========================

Un **caso de uso** es una descripción de las acciones de un
sistema desde el punto de vista del usuario; es una técnica de
aciertos y errores para obtener los requerimientos del sistema
desde el punto de vista del usuario.

A la figura correspondiente al *Usuario de la lavadora* se le
conoce como **actor**. La elipse representa el caso de uso. El
actor (la entidad que inicia el caso de uso) puede ser una persona
u otro sistema.

.. uml::

   @startuml

   left to right direction
   actor "Usuario de la lavadora" as Usuario
   rectangle "Lavadora" {
     usecase "Lavar ropa" as UC1
     usecase "Agregar detergente" as UC2
     usecase "Sacar ropa" as UC3
   }
   Usuario --> UC1
   Usuario --> UC2
   Usuario --> UC3
   @enduml

----
