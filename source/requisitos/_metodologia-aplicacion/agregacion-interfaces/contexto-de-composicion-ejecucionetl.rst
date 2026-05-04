4.1 Contexto de composición — EjecucionETL
------------------------------------------

.. uml::

   @startuml
   allowmixing

   package "EjecucionETL (composición)" {
     class Scheduler
     class FilaCargada
     class ErrorETL
     class EstadoEjecucion

     Scheduler --> EstadoEjecucion : dispara
     EstadoEjecucion --> FilaCargada : produce
     EstadoEjecucion --> ErrorETL    : registra
   }
   note right of EstadoEjecucion
     Diagrama de contexto:
     muestra cómo se relacionan
     los componentes DENTRO de
     una EjecucionETL.
   end note
   @enduml
