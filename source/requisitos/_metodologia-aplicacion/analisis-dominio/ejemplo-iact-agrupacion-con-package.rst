Ejemplo IACT — agrupación con ``package``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando el diagrama crece, agrupar clusters facilita la
lectura:

.. uml::

   @startuml
   title Modelo de dominio IACT — clusters

   hide empty members

   package "Auth + Sesion" {
     class User
     class Session
   }

   package "RBAC" {
     class Group
     class Function
   }

   package "Operacional" {
     class Call
     class Segment
   }

   package "Auditoria" {
     class AuditEvent
   }

   Session "1" *-- "1" User : belongs to
   User "0..*" o-- "0..*" Group : assigned to
   Group "1..*" o-- "0..*" Function : groups
   Call "1..*" -- "1" Segment : belongs to
   User "1" --> "0..*" AuditEvent : generates
   @enduml

Los clusters se ven inmediatamente como cajas, sin
necesidad de inferirlos del nombre o la posición.
