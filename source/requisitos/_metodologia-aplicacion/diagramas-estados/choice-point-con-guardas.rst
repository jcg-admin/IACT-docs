13.5 Choice point con guardas
-----------------------------

.. uml::

   @startuml

   state c <<choice>>

   Publicada --> c : evaluacion completa
   c --> Reconocida : [auto-reconocible]
   c --> Escalada : [umbral critico]
   c --> Pendiente : [else]
   @enduml
