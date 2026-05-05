4.1 Contexto de composición — EjecucionETL
------------------------------------------

.. uml::

   @startuml
   allowmixing

   package "EjecucionETL (composición)" {
     class Scheduler
     class FilaCargada
     class ErrorETL
     class ExecutionStatus

     Scheduler --> ExecutionStatus : dispara
     ExecutionStatus --> FilaCargada : produce
     ExecutionStatus --> ErrorETL    : registra
   }
   note right of ExecutionStatus
     Diagrama de contexto:
     muestra cómo se relacionan
     los componentes DENTRO de
     una EjecucionETL.
   end note
   @enduml
