2. Diagrama de objetos
----------------------

**Propósito:** instancias específicas de clases (casos
concretos, no categorías).

  - **Clase** = molde genérico
  - **Objeto** = instancia específica del molde

**Cuándo usarlo:** cuando quieres mostrar un caso específico
o un ejemplo de cómo funciona una clase en la práctica.

**Lección completa:**
:doc:`uml-03-uso-orientacion-objetos`.

.. uml::

   @startuml

   object "miLavadora : Lavadora" as ml {
     marca = "Laundatorium"
     modelo = "Washmeister"
     numero_serie = "GL57774"
     capacidad = 7.0
   }
   @enduml

----
