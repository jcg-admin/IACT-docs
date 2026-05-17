2.3 Asociación bidireccional
----------------------------

A veces la relación funciona en ambas direcciones:

.. uml::

   @startuml

   class Operator
   class Supervisor
   Operator "1..*" -- "1..*" Supervisor : advised_by
   Supervisor "1..*" -- "1..*" Operator : advises
   note right of Operator
     Bidireccional: un operador
     puede ser asesorado por varios
     supervisores y viceversa.
   end note
   @enduml
