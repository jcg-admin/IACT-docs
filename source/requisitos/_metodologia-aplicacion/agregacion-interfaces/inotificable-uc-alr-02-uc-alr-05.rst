5.2 ``INotificable`` — UC_ALR_02 / UC_ALR_05
--------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface INotificable <<interface>> {
     + entregar(usuario : Usuario, mensaje : Mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   class BuzonInterno {
     + entregar(usuario, mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   class NotificacionPush {
     + entregar(usuario, mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   BuzonInterno ..|> INotificable
   NotificacionPush ..|> INotificable

   note right of INotificable
     CNST_001 prohíbe email →
     IACT NO implementa NotificacionEmail.
     Las únicas implementaciones válidas son
     buzón interno y notificación push interna.
   end note
   @enduml
