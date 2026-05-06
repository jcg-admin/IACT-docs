Ejemplo IACT — diagrama limpio sin compartimentos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicando ``hide empty members``:

.. uml::

   @startuml
   title Modelo de dominio IACT — vista compacta

   hide empty members

   class Call
   class Segment
   class ETLExecution
   class Report
   class User
   class Session
   class AuditEvent

   Call "1..*" -- "1" Segment : belongs to
   ETLExecution "1..*" -- "0..*" Call : loads
   Report "1..*" -- "0..*" Call : aggregates
   Session "1" *-- "1" User : belongs to
   User "1" --> "0..*" AuditEvent : generates
   @enduml

Las cajas son más compactas: solo aparece el nombre de
la entidad, sin compartimentos vacíos.
