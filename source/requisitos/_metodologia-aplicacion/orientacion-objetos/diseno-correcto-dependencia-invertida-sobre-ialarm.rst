Diseño correcto — dependencia invertida sobre IAlarm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title Buen diseno — dependencia invertida via abstraccion

   interface IAlarm {
     + sonar()
   }

   class Controlador {
     - alarma : IAlarm
     + iniciar()
   }

   class RelojDespertador {
     + horaActual()
     + sonar()
   }

   class TemporizadorWeb {
     + sonar()
   }

   Controlador --> IAlarm : depende de
   IAlarm <|.. RelojDespertador
   IAlarm <|.. TemporizadorWeb
   note right of IAlarm
     Tanto Controlador como
     RelojDespertador dependen
     de la abstraccion IAlarm.
     Reemplazar el reloj por
     TemporizadorWeb no toca
     el Controlador (cumple OCP
     y mejora reutilizacion).
   end note
   @enduml
