Ejemplo IACT — agrupación con ``package``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando el diagrama crece, agrupar clusters facilita la
lectura:

.. uml::

   @startuml
   title Modelo de dominio IACT — clusters

   hide empty members

   package "Auth + Sesion" {
     class Usuario
     class Sesion
   }

   package "RBAC" {
     class Grupo
     class Funcion
   }

   package "Operacional" {
     class Llamada
     class Segmento
   }

   package "Auditoria" {
     class EventoAuditoria
   }

   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   Llamada "1..*" -- "1" Segmento : pertenece a
   Usuario "1" --> "0..*" EventoAuditoria : genera
   @enduml

Los clusters se ven inmediatamente como cajas, sin
necesidad de inferirlos del nombre o la posición.
