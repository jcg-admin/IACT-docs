Diseño deficiente — dependencia directa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title Mal diseno — dependencia directa concreta

   class Controlador {
     - reloj : RelojDespertador
     + iniciar()
   }

   class RelojDespertador {
     + horaActual()
     + sonarAlarma()
   }

   Controlador --> RelojDespertador
   note right of Controlador
     - Cambios en RelojDespertador
       afectan al Controlador.
     - Difícil sustituir por otra
       alarma (viola OCP).
     - Reloj acumula responsabilidades
       (viola SRP).
   end note
   @enduml
