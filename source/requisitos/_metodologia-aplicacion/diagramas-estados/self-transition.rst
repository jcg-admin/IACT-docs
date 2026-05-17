13.3 Self-transition
--------------------

.. uml::

   @startuml

   state Procesando

   Procesando --> Procesando : siguiente lote
   @enduml
