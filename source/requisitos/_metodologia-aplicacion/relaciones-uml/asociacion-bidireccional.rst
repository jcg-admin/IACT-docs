2.3 Asociación bidireccional
----------------------------

A veces la relación funciona en ambas direcciones:

.. uml::

   @startuml

   class Operador
   class Supervisor
   Operador "1..*" -- "1..*" Supervisor : asesorado_por
   Supervisor "1..*" -- "1..*" Operador : asesora_a
   note right of Operador
     Bidireccional: un operador
     puede ser asesorado por varios
     supervisores y viceversa.
   end note
   @enduml
