13.4 Junction point
-------------------

.. uml::

   @startuml

   state j <<choice>>

   Inicializada --> j
   PreCargada --> j
   Reanudada --> j
   j --> Procesando : empezar batch
   @enduml
