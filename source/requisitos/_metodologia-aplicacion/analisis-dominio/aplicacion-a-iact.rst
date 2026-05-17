Aplicación a IACT
~~~~~~~~~~~~~~~~~

Aplicado al diagrama del modelo IACT consolidado (§ 7),
las descripciones precisas refuerzan la legibilidad:

.. uml::

   @startuml

   class Call
   class Segment
   class ETLExecution
   class ETLWindow
   class ETLError
   class Report
   class Filter
   class Alert
   class Supervisor
   class User
   class Session
   class Group
   class Function
   class AuditEvent

   Call "1..*" -- "1" Segment : belongs to
   ETLWindow "1" -- "*" ETLExecution : contains
   ETLExecution "*" -- "*" Call : loads
   ETLExecution "1" *-- "*" ETLError : produces
   Report "*" -- "*" Call : aggregates
   Report "1" o-- "*" Filter : applies
   Alert "*" -- "1" Supervisor : is acknowledged by
   Session "1" *-- "1" User : belongs to
   User "*" o-- "*" Group : assigned to
   Group "*" o-- "*" Function : groups
   User "1" --> "*" AuditEvent : generates
   @enduml

Notar:

- **``pertenece a``**,**``contiene``**,**``carga``**,
  **``agrega``**,**``aplica``**,**``es reconocida por``**
  — verbos precisos del dominio en lugar de ``has``
  genérico.
- **``Usuario --> EventoAuditoria : genera``** —
  asociación direccional. El ``EventoAuditoria`` no
  mantiene referencia bidireccional al usuario en
  sentido funcional; el flujo es solo "usuario genera
  evento" (CNST_025: el evento es inmutable y no se
  reasigna).
- **``Alerta -- Supervisor : es reconocida por``** —
  bidireccional, descripción válida en ambos sentidos
  con la misma frase desde el lado de la alerta.
