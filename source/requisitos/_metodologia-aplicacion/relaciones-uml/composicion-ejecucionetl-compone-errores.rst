7.2 Composición — EjecucionETL compone Errores
----------------------------------------------

.. uml::

   @startuml

   class EjecucionETL
   class ErrorETL
   class FilaCargada
   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone
   note right of EjecucionETL
     Composición:
     si la EjecucionETL se purga,
     sus ErrorETL y FilaCargada
     pierden sentido — dependen
     completamente de la ejecución.
   end note
   @enduml
