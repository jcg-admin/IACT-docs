Aplicación a IACT — abstracción del bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En el snapshot pre-refactor de § 17.1,
``ExportarReporteFacade`` dependía del ``Bus``
singleton concreto. Eso producía:

- Acoplamiento al singleton — testing requería
  mockear el state global.
- Imposibilidad de cambiar el bus sin tocar el
  facade.
- Violación de DIP.

Refactor: introducir ``IBus`` y mover el
``Bus`` concreto a un implementador.

.. uml::

   @startuml
   title Snapshot post-refactor — IBus

   interface IBus {
     + publicar(evento : Evento)
     + suscribir(observer : Observer)
   }

   class BusEnMemoria {
     - _observers : List<Observer>
     --
     + publicar(evento : Evento)
     + suscribir(observer : Observer)
   }

   class ExportarReporteFacade {
     - _bus : IBus
     --
     + ejecutar(user : Usuario, cfg : ConfigExport) : TareaId
   }

   BusEnMemoria ..|> IBus : implementa
   ExportarReporteFacade ..> IBus : depende de
   @enduml
